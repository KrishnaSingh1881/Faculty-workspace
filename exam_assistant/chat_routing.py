"""Select a compact, relevant tool set for one Workspace chat request."""

import json
import re

from .chat_tools import SCHEMAS
from .model_runtime import ModelUnavailable, chat_json


FAMILIES = {
    "general": set(),
    "papers": {"search_papers", "create_paper", "create_question", "set_paper_status", "update_paper", "set_paper_archived", "search_questions", "semantic_search_questions", "update_question", "delete_record", "analyze_paper", "replacement_analysis", "apply_replacement"},
    "syllabus": {"lookup_syllabus", "link_syllabus_topics", "update_syllabus_topic", "create_syllabus_topic", "delete_syllabus_topic", "analyze_subject_coverage"},
    "materials": {"list_materials", "map_material", "apply_material_mapping", "delete_record", "lookup_syllabus"},
    "comparisons": {"list_comparisons", "list_comparison_results", "inspect_comparison_result", "start_comparison", "cancel_comparison", "resume_comparison", "rerun_comparison", "prepare_report", "resolve_selected_result", "note_on_selected_result", "search_questions", "search_papers"},
    "templates": {"list_templates", "save_template", "delete_record"},
    "generation": {"generate_questions", "suggest_replacements", "replacement_analysis", "apply_replacement", "lookup_syllabus", "search_questions", "search_papers", "list_templates"},
    "operations": {"list_jobs", "manage_job", "workspace_operations"},
}

ROUTER_SYSTEM = """Choose the Workspace tool families needed to handle the user's request.
Consider the latest request and short conversation context. Include every family needed for a
multi-step action. Select the smallest set that can complete the actual request; do not add a
family merely because its tools might be generally useful. A request about syllabus topics alone
uses syllabus, even if the user plans to edit them later. Do not answer the user or invent IDs.
Families: general (greetings or questions about what the assistant can do, with no Workspace data
lookup); papers (paper/question records, including paper archiving and restoration,
bank search, paper analysis); syllabus (topics and coverage); materials (uploaded teaching notes
and mapping); comparisons (redundancy runs, results, exports, case notes); templates (saved paper,
comparison or report formats); generation (draft questions); operations (background jobs, database,
storage). Return one JSON object with `families`, an array of family names. Use 1-3 families
unless the user explicitly requests more independent workflows. Examples: "find FCFS syllabus
topics" => ["syllabus"]; "map teaching notes into the tree" => ["materials", "syllabus"];
"go ahead, enrich the mapped notes" => ["materials"];
"compare questions in two papers" => ["papers", "comparisons"]; "suggest a harder replacement for this question" => ["generation", "papers"]; "show replacement candidates and coverage" => ["generation", "papers"]; "apply candidate 17" => ["papers"]; "archive that one"
after search_papers => ["papers"]; "what can you do?"
=> ["general"]."""

LOOKUP_FAMILY = {
    "search_papers": "papers", "search_questions": "papers", "semantic_search_questions": "papers",
    "lookup_syllabus": "syllabus", "list_materials": "materials", "list_comparisons": "comparisons",
    "list_templates": "templates", "list_jobs": "operations", "replacement_analysis": "papers", "suggest_replacements": "generation",
    "list_comparison_results": "comparisons", "inspect_comparison_result": "comparisons",
}


def compact_trace(events: list[dict]) -> str:
    """Keep exact IDs for follow-ups without repeating large source documents."""
    compact = []
    for event in events[-8:]:
        result = event.get("result") or {}
        if not isinstance(result, dict):
            continue
        entry = {"tool": event.get("name")}
        for key in ("papers", "questions", "topics", "materials", "comparisons", "results", "templates", "jobs"):
            items = result.get(key)
            if isinstance(items, list):
                entry[key] = [{field: item[field] for field in ("id", "title", "name", "label", "filename", "number", "paper", "kind", "status", "unit") if field in item} for item in items[:12] if isinstance(item, dict)]
        for key in ("paper", "question", "paper_id", "question_id", "comparison_id", "template_id", "material_id", "job_id", "result_id", "topic_id", "status", "success"):
            value = result.get(key)
            if isinstance(value, (str, int, bool, dict)):
                entry[key] = value if not isinstance(value, dict) else {field: value[field] for field in ("id", "title", "number", "status") if field in value}
        compact.append(entry)
    return json.dumps(compact, ensure_ascii=False, default=str)


async def select_chat_tools(model: str, request: str, recent: list[dict], tool_names: list[str], on_event=None) -> tuple[list[dict], list[str]]:
    payload = {"request": request, "recent_conversation": recent[-4:], "recent_tools": tool_names[-8:]}
    response = await chat_json(model, [{"role": "system", "content": ROUTER_SYSTEM}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}], keep_alive="5m", think=False, on_event=on_event)
    try:
        selected = json.loads(response["message"].get("content", ""))["families"]
    except (TypeError, ValueError, KeyError) as exc:
        raise ModelUnavailable("The local assistant could not select Workspace tools for this request") from exc
    if not isinstance(selected, list) or not selected or any(not isinstance(item, str) or item not in FAMILIES for item in selected):
        raise ModelUnavailable("The local assistant selected an invalid Workspace tool family")
    if re.search(r"\b(that|those|this|these|it|one|them)\b", request, re.I) and not re.search(r"\b(paper|question|topic|syllabus|material|template|comparison|job|report|draft|database|storage)\b", request, re.I):
        recent_family = next((LOOKUP_FAMILY[name] for name in reversed(tool_names) if name in LOOKUP_FAMILY), None)
        if recent_family and recent_family not in selected:
            selected.insert(0, recent_family)
    names = set().union(*(FAMILIES[family] for family in selected))
    return [item for item in SCHEMAS if item["function"]["name"] in names], list(dict.fromkeys(selected))
