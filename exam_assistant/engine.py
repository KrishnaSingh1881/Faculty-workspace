"""Small interface for grounded, two-model local question comparison."""

import hashlib
import json
import os

from .comparison_agents import run_helper, run_judge
from .comparison_tools import ComparisonToolbox, requirement_is_grounded
from .knowledge import topic_context
from .model_runtime import (
    HELPER_MODEL,
    JUDGE_MODEL,
    MODEL,
    MODEL_URL,
    ModelUnavailable,
    chat_json,
    classifier_model_status,
    classifier_models_ready,
    model_json,
    model_session,
    unload_model,
)
from .question_analysis import ANALYSIS_PROMPT_VERSION, analyze_questions, bind_profile, validate_analysis


PROMPT_VERSION = "comparison-agents-v4"
TOOL_VERSION = "comparison-tools-v3"
DECISION_VERSION = "assessed-requirements-v4"


def _tools_succeeded(trace: list[dict], required: set[str]) -> bool:
    succeeded = {
        item.get("name")
        for item in trace
        if item.get("name") in required
        and isinstance(item.get("result"), dict)
        and "error" not in item["result"]
    }
    return required.issubset(succeeded)


def _comparison_calls_match(trace: list[dict], requirements_a: list[dict], requirements_b: list[dict], pairs: set[tuple[str, str]]) -> bool:
    by_a = {item["id"]: item for item in requirements_a}
    by_b = {item["id"]: item for item in requirements_b}
    verified = set()
    for item in trace:
        result = item.get("result")
        if item.get("name") != "compare_requirements" or not isinstance(result, dict) or "error" in result:
            continue
        args = item.get("arguments")
        if not isinstance(args, dict):
            continue
        left, right = args.get("requirement_a"), args.get("requirement_b")
        if not isinstance(left, dict) or not isinstance(right, dict):
            continue
        pair = (left.get("id"), right.get("id"))
        if not all(isinstance(value, str) for value in pair):
            continue
        if pair in pairs and left == by_a.get(pair[0]) and right == by_b.get(pair[1]):
            verified.add(pair)
        reverse = (right.get("id"), left.get("id"))
        if reverse in pairs and right == by_a.get(reverse[0]) and left == by_b.get(reverse[1]):
            verified.add(reverse)
    return verified == pairs


def _signal_matrix_call_matches(trace: list[dict], requirements_a: list[dict], requirements_b: list[dict], mapping: list[dict]) -> bool:
    expected_a = {item["id"]: item for item in requirements_a}
    expected_b = {item["id"]: item for item in requirements_b}
    expected_pairs = {(item["a_id"], item["b_id"]) for item in mapping}
    for item in trace:
        result = item.get("result")
        args = item.get("arguments")
        if item.get("name") != "build_signal_matrix" or not isinstance(result, dict) or "error" in result or not isinstance(args, dict):
            continue
        if not all(isinstance(args.get(key), list) for key in ("requirements_a", "requirements_b", "mapping")):
            continue
        actual_a = {entry.get("id"): entry for entry in args["requirements_a"] if isinstance(entry, dict)}
        actual_b = {entry.get("id"): entry for entry in args["requirements_b"] if isinstance(entry, dict)}
        pairs = args.get("mapping")
        rows = result.get("rows")
        if not isinstance(pairs, list) or not isinstance(rows, list):
            continue
        actual_pairs = {(pair.get("a_id"), pair.get("b_id")) for pair in pairs if isinstance(pair, dict)}
        row_pairs = {(row.get("a_id"), row.get("b_id")) for row in rows if isinstance(row, dict)}
        if (
            actual_a == expected_a and actual_b == expected_b
            and len(actual_pairs) == len(pairs) and actual_pairs == expected_pairs
            and len(row_pairs) == len(rows) and row_pairs == expected_pairs
            and result.get("unmatched_a") == sorted(set(expected_a) - {pair[0] for pair in expected_pairs})
            and result.get("unmatched_b") == sorted(set(expected_b) - {pair[1] for pair in expected_pairs})
        ):
            return True
    return False


def _compound_call_matches(trace: list[dict], profile_a: dict, profile_b: dict, mapping: list[dict]) -> bool:
    requirements_a, requirements_b = profile_a["requirements"], profile_b["requirements"]
    expected_mapping = {(item["a_id"], item["b_id"]) for item in mapping}
    expected_a = {item["id"]: item for item in requirements_a}
    expected_b = {item["id"]: item for item in requirements_b}
    for item in trace:
        result = item.get("result")
        if item.get("name") != "check_compound_alignment" or not isinstance(result, dict) or "error" in result:
            continue
        args = item.get("arguments")
        if not isinstance(args, dict) or not isinstance(args.get("requirements_a"), list) or not isinstance(args.get("requirements_b"), list):
            continue
        actual_a = {entry.get("id"): entry for entry in args["requirements_a"] if isinstance(entry, dict)}
        actual_b = {entry.get("id"): entry for entry in args["requirements_b"] if isinstance(entry, dict)}
        if len(actual_a) != len(args["requirements_a"]) or len(actual_b) != len(args["requirements_b"]):
            continue
        actual_mapping = set()
        for entry in args.get("mapping", []):
            if not isinstance(entry, dict) or not isinstance(entry.get("a_id"), str) or not isinstance(entry.get("b_id"), str):
                actual_mapping = set()
                break
            actual_mapping.add((entry["a_id"], entry["b_id"]))
        if (
            actual_a == expected_a
            and actual_b == expected_b
            and actual_mapping == expected_mapping
            and args.get("parts_a") == profile_a["parts"]
            and args.get("parts_b") == profile_b["parts"]
            and args.get("choice_rule_a") == profile_a.get("choice_rule")
            and args.get("choice_rule_b") == profile_b.get("choice_rule")
            and result.get("invalid_pairs") == []
            and result.get("duplicate_mapping") is False
            and result.get("parts_reference_valid") is True
            and result.get("parts_a") == profile_a["parts"]
            and result.get("parts_b") == profile_b["parts"]
            and result.get("choice_rule_a") == profile_a.get("choice_rule")
            and result.get("choice_rule_b") == profile_b.get("choice_rule")
            and set(result.get("requirement_ids_a", [])) == set(expected_a)
            and set(result.get("requirement_ids_b", [])) == set(expected_b)
        ):
            return True
    return False


def pair_key(a, b, tree_version: int) -> str:
    """Invalidate cached outcomes whenever source or local decision config changes."""
    payload = {
        "questions": [(a.id, a.revision), (b.id, b.revision)],
        "comparison_units": [a.unit, b.unit],
        "tree_version": tree_version,
        "judge_model": JUDGE_MODEL,
        "helper_model": HELPER_MODEL,
        "prompt_version": PROMPT_VERSION,
        "analysis_prompt_version": ANALYSIS_PROMPT_VERSION,
        "max_output_tokens": os.getenv("MODEL_MAX_OUTPUT_TOKENS", "2048"),
        "comparison_context_tokens": os.getenv("COMPARISON_CONTEXT_TOKENS", "8192"),
        "thinking": os.getenv("MODEL_THINKING", "auto"),
        "tool_version": TOOL_VERSION,
        "decision_version": DECISION_VERSION,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def evidence_bundle(a, b, tree: dict) -> list[dict]:
    evidence = [
        {"id": "q1", "source": "base question", "text": a.text, "marks": a.marks, "unit": a.unit},
        {"id": "q2", "source": "comparison question", "text": b.text, "marks": b.marks, "unit": b.unit},
    ]
    topic_ids = list(dict.fromkeys((a.topic_ids or []) + (b.topic_ids or [])))
    for index, node in enumerate(topic_context(tree, topic_ids), start=1):
        evidence.append({"id": f"s{index}", "source": "active syllabus tree", "topic_id": node["id"], "text": node})
    return evidence


def _part_signature(profile: dict) -> list[tuple[str, int]]:
    return [(part["kind"], len(part["requirement_ids"])) for part in profile["parts"]]


def _validate_helper(result: dict, a, b, requirements_a: list[dict], requirements_b: list[dict]) -> tuple[list[dict], dict]:
    alignments = result.get("alignments")
    mapping = result.get("compound_mapping")
    concerns = result.get("concerns")
    if not all(isinstance(value, list) for value in (alignments, mapping, concerns)):
        raise ValueError("Helper response is missing a required list")
    if not requirements_a or not requirements_b:
        raise ValueError("Helper did not extract assessed requirements from both questions")

    def validate_requirements(items, question, source_id, prefix):
        seen = set()
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                raise ValueError("Helper requirement has no stable ID")
            rid = item["id"]
            if not rid.startswith(prefix) or rid in seen:
                raise ValueError("Helper requirement IDs must be unique and question-scoped")
            seen.add(rid)
            if not requirement_is_grounded(item, question.text, source_id):
                raise ValueError(f"Helper requirement {rid} is not grounded in its question text")
        return seen

    ids_a = validate_requirements(requirements_a, a, "q1", "q1_")
    ids_b = validate_requirements(requirements_b, b, "q2", "q2_")
    allowed_relations = {"equivalent", "overlap", "distinct"}
    for alignment in alignments:
        if not isinstance(alignment, dict) or not isinstance(alignment.get("a_id"), str) or not isinstance(alignment.get("b_id"), str) or alignment.get("a_id") not in ids_a or alignment.get("b_id") not in ids_b:
            raise ValueError("Helper alignment references an unknown requirement")
        if alignment.get("relation") not in allowed_relations:
            raise ValueError("Helper alignment has an invalid relation")
    if any(not isinstance(item, dict) or not isinstance(item.get("a_id"), str) or not isinstance(item.get("b_id"), str) for item in mapping):
        raise ValueError("Helper compound mapping contains invalid or duplicate entries")
    mapping_pairs = {(item["a_id"], item["b_id"]) for item in mapping}
    if len(mapping_pairs) != len(mapping):
        raise ValueError("Helper compound mapping contains duplicate entries")
    if any(a_id not in ids_a or b_id not in ids_b for a_id, b_id in mapping_pairs):
        raise ValueError("Helper compound mapping references an unknown requirement")
    alignment_pairs = {(item["a_id"], item["b_id"]) for item in alignments}
    if alignment_pairs != mapping_pairs:
        raise ValueError("Helper alignment and compound mapping disagree")
    # Run the same one-to-one coverage rule locally, independent of model-reported tool output.
    covered_a = {pair[0] for pair in mapping_pairs}
    covered_b = {pair[1] for pair in mapping_pairs}
    coverage = {
        "unmatched_a": sorted(ids_a - covered_a),
        "unmatched_b": sorted(ids_b - covered_b),
        "full_coverage_both_directions": bool(ids_a and ids_b and covered_a == ids_a and covered_b == ids_b and len(covered_a) == len(mapping_pairs) and len(covered_b) == len(mapping_pairs)),
    }
    return [{"requirements_a": requirements_a, "requirements_b": requirements_b, "alignments": alignments, "compound_mapping": mapping, "concerns": concerns}], coverage


def _review(reason: str, evidence: list[dict], helper_trace: list[dict], judge_trace: list[dict]) -> dict:
    trace = evidence + [
        {
            **item,
            "id": "helper_analysis" if item.get("name") == "helper_final" else f"helper_tool_{item['id']}",
            "source": "independent helper model" if item.get("name") == "helper_final" else "helper callable tool",
        }
        for item in helper_trace
    ] + [
        {
            **item,
            "id": "judge_response" if item.get("name") == "judge_final" else f"judge_tool_{item['id']}",
            "source": "local judge model response" if item.get("name") == "judge_final" else "judge callable tool",
        }
        for item in judge_trace
    ]
    trace.append({"id": "decision", "source": "deterministic validation", "label": "review", "reason": reason, "cited": False})
    return {
        "label": "review",
        "reason": reason,
        "evidence": trace,
        "source": "local judge/helper; validation abstained",
        "model": f"judge={JUDGE_MODEL}; helper={HELPER_MODEL}",
    }


def _decision_reason(label: str, helper_data: dict, coverage: dict, choice_logic_equivalent: bool) -> str:
    """Phrase the accepted verdict from validated requirement IDs, never model prose."""
    alignments = helper_data["alignments"]
    pairs = ", ".join(f"{item['a_id']} ↔ {item['b_id']}" for item in alignments[:5])
    if len(alignments) > 5:
        pairs += f", and {len(alignments) - 5} more"
    if label == "A":
        return f"All {len(alignments)} assessed ask pair(s) align in both directions ({pairs}); no additional asks or choice-rule differences were accepted."
    if label == "B":
        differences = []
        if overlap := [f"{item['a_id']} ↔ {item['b_id']}" for item in alignments if item["relation"] == "overlap"]:
            differences.append("partial alignment: " + ", ".join(overlap[:5]))
        if coverage["unmatched_a"]:
            differences.append("additional target asks: " + ", ".join(coverage["unmatched_a"][:5]))
        if coverage["unmatched_b"]:
            differences.append("additional reference asks: " + ", ".join(coverage["unmatched_b"][:5]))
        if not choice_logic_equivalent:
            differences.append("choice rules differ")
        if not differences:
            differences.append("part structure differs")
        return f"The questions share assessed asks ({pairs}) but differ in " + "; ".join(differences) + "."
    if label == "C":
        return f"The {len(alignments)} checked ask pair(s) ({pairs}) showed no material assessed overlap; both questions remain in the same syllabus unit."
    raise ValueError(f"Cannot phrase unsupported verdict {label!r}")


async def judge_pair(a, b, tree: dict, profiles: tuple[dict, dict] | None = None, on_event=None) -> dict:
    """Compare one confirmed pair; return review whenever model evidence fails validation."""
    if a.unit != b.unit:
        raise ValueError("Cross-unit comparison is forbidden")
    if not classifier_models_ready():
        raise ModelUnavailable("Configure local JUDGE_MODEL_NAME and HELPER_MODEL_NAME values before comparing")

    if profiles is None:
        profile_a, profile_b = await analyze_questions([a, b])
    else:
        profile_a, profile_b = (validate_analysis(profile, question) for profile, question in zip(profiles, (a, b)))
    bound_profile_a = bind_profile(profile_a, "q1")
    bound_profile_b = bind_profile(profile_b, "q2")
    requirements_a = bound_profile_a["requirements"]
    requirements_b = bound_profile_b["requirements"]
    analysis_concerns = list(profile_a.get("concerns", [])) + list(profile_b.get("concerns", []))

    evidence = evidence_bundle(a, b, tree)
    evidence_by_id = {item["id"]: item for item in evidence}
    toolbox = ComparisonToolbox(a, b, tree)
    registry = {name: lambda args, n=name: toolbox.call(n, args) for name in (
        "lookup_syllabus_topics", "get_topic_neighbors", "get_topic_relation", "compare_requirements", "evaluate_subsumption", "check_transformation",
        "build_signal_matrix", "check_compound_alignment", "find_question_evidence"
    )}
    required_tools = {"compare_requirements", "check_compound_alignment", "build_signal_matrix"}
    helper_trace = []
    async with model_session():
        payload = {
            "evidence": evidence, "questions": {"q1": a.text, "q2": b.text},
            "requirements_a": requirements_a, "requirements_b": requirements_b,
            "parts_a": bound_profile_a["parts"], "parts_b": bound_profile_b["parts"],
            "choice_rule_a": bound_profile_a.get("choice_rule"), "choice_rule_b": bound_profile_b.get("choice_rule"),
        }
        judge_result, judge_trace, judge_tools = await run_judge(JUDGE_MODEL, payload, registry, on_event=on_event)
        judge_trace.append({"id": "decision", "name": "judge_final", "arguments": {}, "result": judge_result})
        try:
            helper_records, coverage = _validate_helper(judge_result, a, b, requirements_a, requirements_b)
            helper_data = helper_records[0]
            mapped_pairs = {(item["a_id"], item["b_id"]) for item in helper_data["compound_mapping"]}
            direct_valid = (not judge_result.get("needs_helper") and judge_result.get("label") != "review"
                and not helper_data["concerns"] and not analysis_concerns
                and required_tools.issubset(set(judge_tools)) and _tools_succeeded(judge_trace, required_tools)
                and _comparison_calls_match(judge_trace, requirements_a, requirements_b, mapped_pairs)
                and _compound_call_matches(judge_trace, bound_profile_a, bound_profile_b, helper_data["compound_mapping"])
                and _signal_matrix_call_matches(judge_trace, requirements_a, requirements_b, helper_data["compound_mapping"]))
        except (ValueError, TypeError, KeyError):
            direct_valid = False
        if not direct_valid:
            if on_event:
                on_event({"agent": "system", "event": "helper_requested", "payload": {"reason": "The judge needs an independent check for this pair."}})
            if JUDGE_MODEL != HELPER_MODEL:
                await unload_model(JUDGE_MODEL)
            try:
                helper_result, helper_trace, helper_tools = await run_helper(HELPER_MODEL, evidence, a.text, b.text, bound_profile_a, bound_profile_b, registry, on_event=on_event)
            finally:
                if JUDGE_MODEL != HELPER_MODEL:
                    await unload_model(HELPER_MODEL)
            helper_trace.append({"id": "analysis", "name": "helper_final", "arguments": {}, "result": helper_result})
            required_tools = {"compare_requirements", "check_compound_alignment", "build_signal_matrix"}
            if not required_tools.issubset(set(helper_tools)) or not _tools_succeeded(helper_trace, required_tools):
                return _review("Helper did not complete the required requirement and compound checks.", evidence, helper_trace, [])
            try:
                helper_records, coverage = _validate_helper(helper_result, a, b, requirements_a, requirements_b)
            except ValueError as exc:
                return _review(f"Helper findings could not be validated: {exc}", evidence, helper_trace, [])
            helper_data = helper_records[0]
            helper_data.update({
                "parts_a": bound_profile_a["parts"],
                "parts_b": bound_profile_b["parts"],
                "choice_rule_a": bound_profile_a.get("choice_rule"),
                "choice_rule_b": bound_profile_b.get("choice_rule"),
            })
            helper_data["coverage_check"] = coverage
            helper_data["analysis_concerns"] = analysis_concerns
            mapped_pairs = {(item["a_id"], item["b_id"]) for item in helper_data["compound_mapping"]}
            if not _comparison_calls_match(helper_trace, helper_data["requirements_a"], helper_data["requirements_b"], mapped_pairs):
                return _review("Helper did not compare each requirement pair it aligned.", evidence, helper_trace, [])
            if not _compound_call_matches(helper_trace, bound_profile_a, bound_profile_b, helper_data["compound_mapping"]):
                return _review("Helper did not validate its final compound mapping with the tool.", evidence, helper_trace, [])
            if not _signal_matrix_call_matches(helper_trace, requirements_a, requirements_b, helper_data["compound_mapping"]):
                return _review("Helper did not produce a complete signal matrix for its final mapping.", evidence, helper_trace, [])
            helper_evidence_id = "helper_analysis"
            evidence_by_id[helper_evidence_id] = {
                "id": helper_evidence_id,
                "source": "independent helper analysis",
                "text": helper_data,
            }
            judge_result, judge_trace, judge_tools = await run_judge(
                    JUDGE_MODEL,
                    {
                        "evidence": evidence + [evidence_by_id[helper_evidence_id]],
                        "helper_analysis": helper_data,
                        "questions": {"q1": a.text, "q2": b.text},
                        "requirements_a": requirements_a,
                        "requirements_b": requirements_b,
                        "parts_a": bound_profile_a["parts"],
                        "parts_b": bound_profile_b["parts"],
                        "choice_rule_a": bound_profile_a.get("choice_rule"),
                        "choice_rule_b": bound_profile_b.get("choice_rule"),
                        "required_tool_checks": ["compare_requirements", "check_compound_alignment", "build_signal_matrix"],
                    },
                    registry,
                    on_event=on_event,
                )
            judge_trace.append({"id": "decision", "name": "judge_final", "arguments": {}, "result": judge_result})

        else:
            helper_data.update({"parts_a": bound_profile_a["parts"], "parts_b": bound_profile_b["parts"],
                "choice_rule_a": bound_profile_a.get("choice_rule"), "choice_rule_b": bound_profile_b.get("choice_rule"),
                "coverage_check": coverage, "analysis_concerns": analysis_concerns})

    if not required_tools.issubset(set(judge_tools)) or not _tools_succeeded(judge_trace, required_tools):
        return _review("Judge did not independently complete the required comparison and compound checks.", evidence, helper_trace, judge_trace)
    if not _comparison_calls_match(judge_trace, helper_data["requirements_a"], helper_data["requirements_b"], mapped_pairs):
        return _review("Judge did not independently check each helper-aligned requirement pair.", evidence, helper_trace, judge_trace)
    if not _compound_call_matches(judge_trace, bound_profile_a, bound_profile_b, helper_data["compound_mapping"]):
        return _review("Judge did not independently validate the helper's compound mapping.", evidence, helper_trace, judge_trace)
    if not _signal_matrix_call_matches(judge_trace, requirements_a, requirements_b, helper_data["compound_mapping"]):
        return _review("Judge did not independently produce a complete signal matrix for the helper mapping.", evidence, helper_trace, judge_trace)

    label = judge_result.get("label")
    reason = judge_result.get("reason")
    citations = judge_result.get("evidence_ids")
    if not isinstance(label, str) or label not in {"A", "B", "C", "review"} or not isinstance(reason, str) or not reason.strip():
        return _review("Judge response did not satisfy the classification contract.", evidence, helper_trace, judge_trace)
    if not isinstance(citations, list) or any(not isinstance(item, str) for item in citations) or not {"q1", "q2"}.issubset(set(citations)) or any(item not in evidence_by_id for item in citations):
        return _review("Judge cited missing or invalid evidence; no label was accepted.", evidence, helper_trace, judge_trace)
    missed = judge_result.get("missed_requirements")
    shared = judge_result.get("shared_requirements")
    differences = judge_result.get("differences")
    choice_logic_equivalent = judge_result.get("choice_logic_equivalent")
    confidence = judge_result.get("confidence")
    if not isinstance(missed, list) or not isinstance(shared, list) or not isinstance(differences, list) or not isinstance(choice_logic_equivalent, bool) or isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        return _review("Judge omitted its completeness audit or confidence field.", evidence, helper_trace, judge_trace)
    if missed:
        return _review("Judge identified a potentially missed assessed requirement.", evidence, helper_trace, judge_trace)
    if label == "review":
        return _review("Judge left the pair unresolved after its required checks.", evidence, helper_trace, judge_trace)

    helper_alignments = helper_data["alignments"]
    relations = {item["relation"] for item in helper_alignments}
    if label in {"A", "B", "C"} and (helper_data["concerns"] or analysis_concerns):
        return _review("A local analysis or helper identified unresolved question requirements.", evidence, helper_trace, judge_trace)
    if label == "A" and (
        not coverage["full_coverage_both_directions"]
        or relations - {"equivalent"}
        or _part_signature(bound_profile_a) != _part_signature(bound_profile_b)
        or not choice_logic_equivalent
    ):
        return _review("A requires complete two-way compound coverage and no helper-identified differences or concerns.", evidence, helper_trace, judge_trace)
    if label == "B" and not relations.intersection({"equivalent", "overlap"}):
        return _review("B requires evidence of at least one materially shared assessed requirement.", evidence, helper_trace, judge_trace)
    if label == "B" and (not shared or not differences):
        return _review("B requires both a stated shared requirement and a concrete difference.", evidence, helper_trace, judge_trace)
    if label == "B" and not (coverage["unmatched_a"] or coverage["unmatched_b"] or "overlap" in relations or not choice_logic_equivalent or _part_signature(bound_profile_a) != _part_signature(bound_profile_b)):
        return _review("B has no validated extra ask, partial alignment, or structural difference.", evidence, helper_trace, judge_trace)
    if label == "B":
        difference_record = json.dumps(differences, ensure_ascii=False)
        unmatched = coverage["unmatched_a"] + coverage["unmatched_b"]
        if any(requirement_id not in difference_record for requirement_id in unmatched):
            return _review("B omitted an unmatched assessed requirement from its recorded differences.", evidence, helper_trace, judge_trace)
    if label == "A" and (not shared or differences):
        return _review("A requires shared requirements and no additional assessed differences.", evidence, helper_trace, judge_trace)
    if label == "C" and (relations.intersection({"equivalent", "overlap"}) or helper_data["concerns"] or not coverage["full_coverage_both_directions"]):
        return _review("C conflicts with helper evidence of overlap or unresolved concerns.", evidence, helper_trace, judge_trace)
    if label == "C" and shared:
        return _review("C conflicts with the judge's stated shared requirements.", evidence, helper_trace, judge_trace)

    public_reason = _decision_reason(label, helper_data, coverage, choice_logic_equivalent)
    trace = list(evidence_by_id.values())
    trace.extend({**item, "id": f"helper_tool_{item['id']}", "source": "helper callable tool", "cited": False} for item in helper_trace if item.get("name") != "helper_final")
    trace.extend({**item, "id": f"judge_tool_{item['id']}", "source": "judge callable tool", "cited": False} for item in judge_trace if item.get("name") != "judge_final")
    trace.append({
        "id": "decision",
        "source": "deterministic validation of judge/helper findings",
        "label": label,
        "reason": public_reason,
        "judge_explanation": reason.strip(),
        "shared_requirements": shared,
        "differences": differences,
        "alignment_relations": [{"target_requirement_id": item["a_id"], "reference_requirement_id": item["b_id"], "relation": item["relation"]} for item in helper_alignments],
        "unmatched_target_requirements": coverage["unmatched_a"],
        "unmatched_reference_requirements": coverage["unmatched_b"],
        "choice_logic_equivalent": choice_logic_equivalent,
        "what_would_change": {
            "A": "A new unmatched ask, partial alignment, or changed choice rule would require a fresh verdict.",
            "B": "Complete two-way equivalence could support A; loss of material shared asks could support C.",
            "C": "Evidence of a materially shared assessed ask would require re-examination.",
        }[label],
        "confidence": confidence,
        "confidence_source": "judge model self-report; uncalibrated",
        "cited": True,
    })
    return {
        "label": label,
        "reason": public_reason,
        "evidence": [{**item, "cited": item.get("id") in citations or item.get("id") == "decision"} for item in trace],
        "source": "local judge with optional helper; provisional pending labeled evaluation",
        "model": f"judge={JUDGE_MODEL}; helper={HELPER_MODEL}",
    }


__all__ = [
    "HELPER_MODEL", "JUDGE_MODEL", "MODEL", "MODEL_URL", "PROMPT_VERSION",
    "ModelUnavailable", "classifier_model_status", "classifier_models_ready",
    "judge_pair", "model_json", "pair_key",
]
