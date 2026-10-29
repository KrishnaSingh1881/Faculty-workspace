"""Deterministic, source-grounded tools available to local comparison models."""

import re
from difflib import SequenceMatcher
from typing import Any

from .knowledge import topic_context


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_syllabus_topics",
            "description": "Return exact syllabus nodes, ancestor paths, and same-unit distinction notes for supplied topic IDs.",
            "parameters": {"type": "object", "required": ["topic_ids"], "properties": {"topic_ids": {"type": "array", "items": {"type": "string"}}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_topic_neighbors",
            "description": "Find nearby ordered topics under the same parent and unit. Neighbourhood is candidate context only and never proves overlap.",
            "parameters": {"type": "object", "required": ["topic_ids"], "properties": {"topic_ids": {"type": "array", "items": {"type": "string"}, "maxItems": 12}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_topic_relation",
            "description": "Describe exact identity, explicit distinction, parent-path relation, sibling relation or same-unit-only relation between syllabus topics. Never infer semantic overlap from adjacency.",
            "parameters": {"type": "object", "required": ["topic_id_a", "topic_id_b"], "properties": {"topic_id_a": {"type": "string"}, "topic_id_b": {"type": "string"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_requirements",
            "description": "Compare two extracted atomic asks field by field. This returns signals, not a final label.",
            "parameters": {"type": "object", "required": ["requirement_a", "requirement_b"], "properties": {"requirement_a": {"type": "object"}, "requirement_b": {"type": "object"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "evaluate_subsumption",
            "description": "Inspect whether one atomic ask appears narrower or broader than another across assessed dimensions. Lexical containment is a diagnostic signal, not a semantic verdict.",
            "parameters": {"type": "object", "required": ["requirement_a", "requirement_b"], "properties": {"requirement_a": {"type": "object"}, "requirement_b": {"type": "object"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_transformation",
            "description": "Check whether a scenario or wording change appears to preserve action, scope, output, depth, conditions and negation; return changed dimensions explicitly.",
            "parameters": {"type": "object", "required": ["requirement_a", "requirement_b"], "properties": {"requirement_a": {"type": "object"}, "requirement_b": {"type": "object"}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_compound_alignment",
            "description": "Validate a proposed one-to-one mapping of atomic asks and report unmatched asks in both directions.",
            "parameters": {"type": "object", "required": ["requirements_a", "requirements_b", "mapping"], "properties": {"requirements_a": {"type": "array", "items": {"type": "object"}}, "requirements_b": {"type": "array", "items": {"type": "object"}}, "mapping": {"type": "array", "items": {"type": "object", "required": ["a_id", "b_id"], "properties": {"a_id": {"type": "string"}, "b_id": {"type": "string"}}}}, "parts_a": {"type": "array", "items": {"type": "object"}}, "parts_b": {"type": "array", "items": {"type": "object"}}, "choice_rule_a": {"type": ["string", "null"]}, "choice_rule_b": {"type": ["string", "null"]}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "build_signal_matrix",
            "description": "Return an inspectable field-by-field signal matrix for a proposed list of atomic requirement alignments.",
            "parameters": {"type": "object", "required": ["requirements_a", "requirements_b", "mapping"], "properties": {"requirements_a": {"type": "array", "items": {"type": "object"}}, "requirements_b": {"type": "array", "items": {"type": "object"}}, "mapping": {"type": "array", "items": {"type": "object", "required": ["a_id", "b_id"], "properties": {"a_id": {"type": "string"}, "b_id": {"type": "string"}}}}}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_question_evidence",
            "description": "Search the supplied questions and syllabus records for shared query terms and return the matching source ID and full excerpt.",
            "parameters": {"type": "object", "required": ["query"], "properties": {"query": {"type": "string"}}},
        },
    },
]

def _normal(value: Any) -> str:
    return " ".join(re.findall(r"[\w]+", str(value or "").casefold()))


def _tokens(value: Any) -> set[str]:
    return set(_normal(value).split())


def _compare_requirements(args: dict) -> dict:
    left, right = args["requirement_a"], args["requirement_b"]
    fields = ("concept", "action", "object", "scope", "depth", "output", "conditions", "negation")
    comparisons = {}
    for field in fields:
        a, b = left.get(field), right.get(field)
        if a is None or b is None:
            comparisons[field] = {"values": [a, b], "relation": "missing"}
            continue
        na, nb = _normal(a), _normal(b)
        score = round(SequenceMatcher(a=na, b=nb).ratio(), 3) if na and nb else 0.0
        comparisons[field] = {
            "values": [a, b],
            "relation": "same wording" if na == nb and na else "different wording",
            "lexical_similarity": score,
        }
    return {"requirement_ids": [left.get("id"), right.get("id")], "fields": comparisons, "warning": "Lexical similarity is only a signal; it does not establish semantic equivalence."}


def _subsumption(args: dict) -> dict:
    left, right = args["requirement_a"], args["requirement_b"]
    dimensions = ("concept", "action", "object", "scope", "depth", "output", "conditions", "negation")
    containment = {}
    for field in dimensions:
        a, b = _normal(left.get(field)), _normal(right.get(field))
        containment[field] = "missing" if not a or not b else "same" if a == b else "a_contains_b" if b in a else "b_contains_a" if a in b else "different"
    narrower_a = [field for field, relation in containment.items() if relation == "b_contains_a"]
    narrower_b = [field for field, relation in containment.items() if relation == "a_contains_b"]
    return {"requirement_ids": [left.get("id"), right.get("id")], "field_containment": containment, "possible_narrower_a": narrower_a, "possible_narrower_b": narrower_b, "warning": "String containment does not establish semantic subsumption."}


def _transformation(args: dict) -> dict:
    left, right = args["requirement_a"], args["requirement_b"]
    dimensions = ("concept", "action", "object", "scope", "depth", "output", "conditions", "negation")
    signals = {}
    for field in dimensions:
        a, b = _normal(left.get(field)), _normal(right.get(field))
        ratio = round(SequenceMatcher(a=a, b=b).ratio(), 3) if a and b else None
        signals[field] = {"preserved_wording": bool(a and a == b), "lexical_similarity": ratio, "status": "missing" if not a or not b else "same wording" if a == b else "wording changed"}
    return {"requirement_ids": [left.get("id"), right.get("id")], "dimensions": signals, "warning": "Lexical preservation is not proof that a scenario transformation preserves the assessed task."}


def _signal_matrix(args: dict) -> dict:
    requirements_a, requirements_b, mapping = args["requirements_a"], args["requirements_b"], args["mapping"]
    if not all(isinstance(value, list) for value in (requirements_a, requirements_b, mapping)):
        raise ValueError("requirements_a, requirements_b and mapping must be arrays")
    left = {item.get("id"): item for item in requirements_a if isinstance(item, dict)}
    right = {item.get("id"): item for item in requirements_b if isinstance(item, dict)}
    rows = []
    for pair in mapping:
        if not isinstance(pair, dict) or pair.get("a_id") not in left or pair.get("b_id") not in right:
            raise ValueError("Every signal-matrix pair must reference supplied requirement IDs")
        compared = _compare_requirements({"requirement_a": left[pair["a_id"]], "requirement_b": right[pair["b_id"]]})
        rows.append({"a_id": pair["a_id"], "b_id": pair["b_id"], "signals": compared["fields"]})
    matched_a = {row.get("a_id") for row in rows}
    matched_b = {row.get("b_id") for row in rows}
    return {
        "rows": rows,
        "unmatched_a": sorted(set(left) - matched_a),
        "unmatched_b": sorted(set(right) - matched_b),
        "warning": "Matrix entries are diagnostic signals and cannot decide A/B/C.",
    }


def _check_compound(args: dict) -> dict:
    if not isinstance(args.get("requirements_a"), list) or not isinstance(args.get("requirements_b"), list) or not isinstance(args.get("mapping"), list):
        raise ValueError("Compound requirements and mapping must be lists")
    if any(not isinstance(item, dict) or not isinstance(item.get("id"), str) for item in args["requirements_a"] + args["requirements_b"]):
        raise ValueError("Every compound requirement must have a string ID")
    ids_a = [item["id"] for item in args["requirements_a"]]
    ids_b = [item["id"] for item in args["requirements_b"]]
    if len(ids_a) != len(set(ids_a)) or len(ids_b) != len(set(ids_b)):
        raise ValueError("Compound requirement IDs must be unique within each question")
    if any(not isinstance(item, dict) or not isinstance(item.get("a_id"), str) or not isinstance(item.get("b_id"), str) for item in args["mapping"]):
        raise ValueError("Every compound mapping entry must have string a_id and b_id")
    parts_a, parts_b = args.get("parts_a", []), args.get("parts_b", [])
    if not isinstance(parts_a, list) or not isinstance(parts_b, list):
        raise ValueError("Question parts must be lists")
    for part in parts_a + parts_b:
        if not isinstance(part, dict) or not isinstance(part.get("part_id"), str) or not isinstance(part.get("requirement_ids"), list):
            raise ValueError("Each question part needs an ID and requirement list")
    choice_a, choice_b = args.get("choice_rule_a"), args.get("choice_rule_b")
    if choice_a is not None and not isinstance(choice_a, str) or choice_b is not None and not isinstance(choice_b, str):
        raise ValueError("Choice rules must be text or null")
    left = {item.get("id") for item in args["requirements_a"] if isinstance(item, dict) and item.get("id")}
    right = {item.get("id") for item in args["requirements_b"] if isinstance(item, dict) and item.get("id")}
    parts_valid = all(all(isinstance(req_id, str) and req_id in left for req_id in part["requirement_ids"]) for part in parts_a) and all(all(isinstance(req_id, str) and req_id in right for req_id in part["requirement_ids"]) for part in parts_b)
    mapping = args["mapping"]
    a_ids = [item.get("a_id") for item in mapping]
    b_ids = [item.get("b_id") for item in mapping]
    invalid = [item for item in mapping if not isinstance(item, dict) or item.get("a_id") not in left or item.get("b_id") not in right]
    duplicates = len(a_ids) != len(set(a_ids)) or len(b_ids) != len(set(b_ids))
    matched_a, matched_b = set(a_ids) & left, set(b_ids) & right
    return {
        "mapping": mapping,
        "parts_a": parts_a,
        "parts_b": parts_b,
        "choice_rule_a": choice_a,
        "choice_rule_b": choice_b,
        "parts_reference_valid": parts_valid,
        "requirement_ids_a": sorted(left),
        "requirement_ids_b": sorted(right),
        "unmatched_a": sorted(left - matched_a),
        "unmatched_b": sorted(right - matched_b),
        "invalid_pairs": invalid,
        "duplicate_mapping": duplicates,
        "full_coverage_both_directions": bool(left and right and parts_valid and not invalid and not duplicates and matched_a == left and matched_b == right),
    }


def _build_sources(a, b, tree: dict) -> list[dict]:
    nodes = {node["id"]: node for node in tree.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str)}
    selected = list(dict.fromkeys((a.topic_ids or []) + (b.topic_ids or [])))
    records = [
        {"id": "q1", "kind": "question", "text": a.text},
        {"id": "q2", "kind": "question", "text": b.text},
    ]
    for index, node in enumerate(topic_context(tree, selected), start=1):
        records.append({"id": f"s{index}", "kind": "syllabus", "topic_id": node["id"], "text": json_text(node)})
        parent_id = node.get("parent")
        visited = set()
        while parent_id and parent_id in nodes and parent_id not in visited:
            visited.add(parent_id)
            parent = nodes[parent_id]
            records.append({"id": f"sp{len(records)}", "kind": "syllabus_parent", "topic_id": parent_id, "text": json_text(parent)})
            parent_id = parent.get("parent")
        for link in node.get("distinguish_from", []):
            other_id = link.get("node")
            if other_id in nodes:
                records.append({"id": f"sd{len(records)}", "kind": "syllabus_distinction", "topic_id": other_id, "text": json_text({"node": nodes[other_id], "note": link.get("note")})})
    return records


def json_text(value: Any) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class ComparisonToolbox:
    """Tools scoped to one immutable question pair and tree snapshot."""

    def __init__(self, a, b, tree: dict):
        self.sources = _build_sources(a, b, tree)
        self.tree = tree

    def call(self, name: str, arguments: dict) -> dict:
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be an object")
        if name == "lookup_syllabus_topics":
            ids = arguments.get("topic_ids")
            if not isinstance(ids, list) or any(not isinstance(item, str) for item in ids):
                raise ValueError("topic_ids must be a list of strings")
            nodes = {node["id"]: node for node in self.tree.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str)}
            exact = [nodes[item] for item in ids if item in nodes]
            ancestors = []
            distinctions = []
            for node in exact:
                parent = node.get("parent")
                visited = set()
                while parent and parent in nodes and parent not in visited:
                    visited.add(parent)
                    ancestors.append(nodes[parent])
                    parent = nodes[parent].get("parent")
                for link in node.get("distinguish_from", []):
                    target = link.get("node")
                    if target in nodes:
                        distinctions.append({"topic": nodes[target], "note": link.get("note"), "source_topic_id": node["id"]})
            return {
                "requested_ids": ids,
                "unknown_ids": [item for item in ids if item not in nodes],
                "topics": exact,
                "ancestor_paths": list({item["id"]: item for item in ancestors}.values()),
                "same_unit_distinctions": distinctions,
            }
        if name == "get_topic_neighbors":
            ids = arguments.get("topic_ids")
            if not isinstance(ids, list) or len(ids) > 12 or any(not isinstance(item, str) for item in ids):
                raise ValueError("topic_ids must be an array of at most 12 strings")
            nodes = {node["id"]: node for node in self.tree.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str)}
            results = []
            for topic_id in ids:
                node = nodes.get(topic_id)
                if not node or node.get("kind") != "topic":
                    results.append({"topic_id": topic_id, "error": "Unknown topic ID"})
                    continue
                unit = topic_id.split("/u", 1)[-1].split("/", 1)[0]
                siblings = [item for item in nodes.values() if item.get("kind") == "topic" and item.get("parent") == node.get("parent") and item.get("id", "").split("/u", 1)[-1].split("/", 1)[0] == unit]
                siblings.sort(key=lambda item: (item.get("order", 0) if isinstance(item.get("order", 0), int) else 0, item["id"]))
                index = next(i for i, item in enumerate(siblings) if item["id"] == topic_id)
                summarize = lambda item: {key: item.get(key) for key in ("id", "label", "order", "description", "source_text")}
                results.append({"topic_id": topic_id, "unit": unit, "parent": node.get("parent"), "previous": summarize(siblings[index - 1]) if index else None, "next": summarize(siblings[index + 1]) if index + 1 < len(siblings) else None, "warning": "Order proximity is not evidence of semantic similarity."})
            return {"topics": results}
        if name == "get_topic_relation":
            left_id, right_id = arguments.get("topic_id_a"), arguments.get("topic_id_b")
            if not isinstance(left_id, str) or not isinstance(right_id, str):
                raise ValueError("Both topic IDs must be strings")
            nodes = {node["id"]: node for node in self.tree.get("nodes", []) if isinstance(node, dict) and isinstance(node.get("id"), str)}
            left, right = nodes.get(left_id), nodes.get(right_id)
            if not left or not right or left.get("kind") != "topic" or right.get("kind") != "topic":
                return {"topic_ids": [left_id, right_id], "error": "Both IDs must be topics in the active tree"}
            left_unit, right_unit = left_id.split("/u", 1)[-1].split("/", 1)[0], right_id.split("/u", 1)[-1].split("/", 1)[0]
            explicit = next((link.get("note", "") for link in left.get("distinguish_from", []) if isinstance(link, dict) and link.get("node") == right_id), None)
            if left_id == right_id:
                relation = "same_topic"
            elif left_unit != right_unit:
                relation = "different_unit_display_only"
            elif explicit is not None:
                relation = "explicitly_distinguished"
            elif left.get("parent") == right.get("parent"):
                relation = "siblings"
            else:
                relation = "same_unit_without_direct_relation"
            return {"topic_ids": [left_id, right_id], "units": [left_unit, right_unit], "relation": relation, "distinction_note": explicit, "warning": "Syllabus structure and adjacency alone do not decide A, B or C."}
        if name == "compare_requirements":
            return _compare_requirements(arguments)
        if name == "evaluate_subsumption":
            return _subsumption(arguments)
        if name == "check_transformation":
            return _transformation(arguments)
        if name == "build_signal_matrix":
            return _signal_matrix(arguments)
        if name == "check_compound_alignment":
            return _check_compound(arguments)
        if name == "find_question_evidence":
            query = arguments.get("query")
            if not isinstance(query, str) or not query.strip():
                raise ValueError("query must be a non-empty string")
            terms = _tokens(query)
            hits = []
            for source in self.sources:
                text = source["text"]
                source_terms = _tokens(text)
                overlap = terms & source_terms
                if not overlap:
                    continue
                hits.append({**source, "matched_terms": sorted(overlap), "match_ratio": round(len(overlap) / len(terms), 3)})
            return {"query": query, "hits": sorted(hits, key=lambda item: item["match_ratio"], reverse=True)[:8]}
        raise ValueError(f"Unknown comparison tool: {name}")


def requirement_is_grounded(requirement: dict, source_text: str, source_id: str) -> bool:
    quote = requirement.get("quote")
    if not isinstance(quote, str) or not quote.strip() or requirement.get("evidence_id") != source_id:
        return False
    quote_tokens = _normal(quote).split()
    text_tokens = _normal(source_text).split()
    width = len(quote_tokens)
    return bool(width and any(text_tokens[index:index + width] == quote_tokens for index in range(len(text_tokens) - width + 1)))
