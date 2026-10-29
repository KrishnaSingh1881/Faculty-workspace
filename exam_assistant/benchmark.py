"""Run a labeled OS/IoT pair set; no synthetic questions are generated here."""
import argparse
import asyncio
import json
import hashlib
import time
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from sqlalchemy import select

from .db import Session, Subject, initialize
from .engine import JUDGE_MODEL, HELPER_MODEL, classifier_models_ready, judge_pair


def validate_cases(cases: list[dict]) -> None:
    if not cases:
        raise ValueError("Benchmark has no labeled pairs")
    seen_ids = set()
    for index, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            raise ValueError(f"Case {index} must be an object")
        if case.get("label") not in ("A", "B", "C"):
            raise ValueError(f"Case {index} needs a ground-truth A/B/C label")
        if not isinstance(case.get("family"), str) or not case["family"].strip():
            raise ValueError(f"Case {index} needs a question-family ID for held-out splitting")
        if "category" in case and not isinstance(case["category"], str):
            raise ValueError(f"Case {index} category must be text")
        case_id = str(case.get("id", index))
        if case_id in seen_ids:
            raise ValueError(f"Case ID {case_id} is duplicated")
        seen_ids.add(case_id)
        questions = case.get("questions", [])
        if not isinstance(questions, list) or len(questions) != 2 or any(not isinstance(q, dict) or not q.get("text") or q.get("unit") not in range(1, 6) for q in questions):
            raise ValueError(f"Case {index} needs two questions with text and units 1–5")
        if questions[0]["unit"] != questions[1]["unit"]:
            raise ValueError(f"Case {index} crosses units")


def family_split(family: str, seed: str = "exam-assistant-v1") -> str:
    digest = hashlib.sha256(f"{seed}:{family}".encode()).digest()
    return "held_out" if int.from_bytes(digest[:4], "big") % 5 == 0 else "development"


def _decision_confidence(result: dict) -> float | None:
    for item in result.get("evidence", []):
        if item.get("id") == "decision" and isinstance(item.get("confidence"), (int, float)):
            return float(item["confidence"])
    return None


async def evaluate(path: Path, *, split: str = "all", seed: str = "exam-assistant-v1") -> dict:
    if not classifier_models_ready():
        raise RuntimeError("Set local JUDGE_MODEL_NAME and HELPER_MODEL_NAME values before benchmarking")
    cases = json.loads(path.read_text())
    validate_cases(cases)
    if split not in {"all", "development", "held_out"}:
        raise ValueError("split must be all, development or held_out")
    cases = [case for case in cases if split == "all" or family_split(str(case["family"]), seed) == split]
    if not cases:
        raise ValueError(f"No cases assigned to the {split} split")
    initialize()
    counts = Counter()
    details = []
    with Session() as db:
        subjects = {s.code: s for s in db.scalars(select(Subject))}
        for index, case in enumerate(cases, 1):
            subject = subjects.get(case.get("subject_code"))
            if not subject:
                raise ValueError(f"Case {index} has unknown subject_code")
            questions = [SimpleNamespace(id=index * 2 + i, text=q["text"], unit=q["unit"], marks=q.get("marks"), topic_ids=q.get("topic_ids", [])) for i, q in enumerate(case["questions"])]
            started = time.perf_counter()
            result = await judge_pair(*questions, subject.tree)
            elapsed = round(time.perf_counter() - started, 2)
            counts[(case["label"], result["label"])] += 1
            confidence = _decision_confidence(result)
            details.append({"id": case.get("id", index), "family": case["family"], "family_split": family_split(str(case["family"]), seed), "category": case.get("category", "unspecified"), "subject": subject.code, "truth": case["label"], "predicted": result["label"], "confidence": confidence, "tool_calls": sum(item.get("source") in ("helper callable tool", "judge callable tool") for item in result.get("evidence", [])), "seconds": elapsed, "reason": result["reason"]})
    matrix = {truth: {pred: counts[(truth, pred)] for pred in ("A", "B", "C", "review")} for truth in ("A", "B", "C")}
    scores = {}
    for label in ("A", "B", "C"):
        tp = counts[(label, label)]
        predicted = sum(counts[(truth, label)] for truth in ("A", "B", "C"))
        actual = sum(counts[(label, pred)] for pred in ("A", "B", "C", "review"))
        scores[label] = {"precision": round(tp / predicted, 4) if predicted else None, "recall": round(tp / actual, 4) if actual else None}
    bins = [{"range": f"{start / 10:.1f}-{(start + 1) / 10:.1f}", "count": 0, "mean_confidence": None, "accuracy": None} for start in range(10)]
    for detail in details:
        confidence = detail["confidence"]
        if confidence is None or detail["predicted"] == "review":
            continue
        bucket = bins[min(9, int(confidence * 10))]
        bucket["count"] += 1
        bucket["_confidence_sum"] = bucket.get("_confidence_sum", 0.0) + confidence
        bucket["_correct"] = bucket.get("_correct", 0) + int(detail["predicted"] == detail["truth"])
    for bucket in bins:
        if bucket["count"]:
            bucket["mean_confidence"] = round(bucket.pop("_confidence_sum") / bucket["count"], 4)
            bucket["accuracy"] = round(bucket.pop("_correct") / bucket["count"], 4)
        else:
            bucket.pop("_confidence_sum", None)
            bucket.pop("_correct", None)
    by_category = {}
    for detail in details:
        item = by_category.setdefault(detail["category"], {"cases": 0, "correct": 0, "review": 0})
        item["cases"] += 1
        item["correct"] += int(detail["predicted"] == detail["truth"])
        item["review"] += int(detail["predicted"] == "review")
    for item in by_category.values():
        item["accuracy"] = round(item["correct"] / item["cases"], 4)
        item["review_rate"] = round(item["review"] / item["cases"], 4)
    correct = sum(counts[(label, label)] for label in ("A", "B", "C"))
    return {"judge_model": JUDGE_MODEL, "helper_model": HELPER_MODEL, "split": split, "split_seed": seed, "family_split_rule": "SHA-256(seed:family) modulo 5; all cases from a family stay together", "cases": len(cases), "families": len({str(case["family"]) for case in cases}), "matrix": matrix, "scores": scores, "accuracy": round(correct / len(cases), 4), "review_rate": round(sum(d["predicted"] == "review" for d in details) / len(details), 4), "confidence_bins_non_review_only": bins, "by_category": by_category, "mean_seconds": round(sum(d["seconds"] for d in details) / len(details), 2), "mean_tool_calls": round(sum(d["tool_calls"] for d in details) / len(details), 2), "details": details}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cases", type=Path)
    parser.add_argument("--out", type=Path, default=Path("benchmark-result.json"))
    parser.add_argument("--split", choices=("all", "development", "held_out"), default="all")
    parser.add_argument("--seed", default="exam-assistant-v1")
    args = parser.parse_args()
    result = asyncio.run(evaluate(args.cases, split=args.split, seed=args.seed))
    args.out.write_text(json.dumps(result, indent=2))
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
