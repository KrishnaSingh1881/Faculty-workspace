"""Subject-scoped read and explicit-action tools for the local Workspace assistant."""

from copy import deepcopy

from sqlalchemy import func, or_, select

from .db import AuditEvent, BackgroundJob, Comparison, Material, PairResult, Paper, Question, SyllabusImport, Template, TreeRevision
from .jobs import enqueue_job
from .knowledge import unit_for_topic, validate_tree
from .embeddings import semantic_search
from .model_runtime import ModelUnavailable
from .engine import pair_key


SYSTEM = """You are the local faculty Workspace assistant. Use the supplied application tools for
all facts about papers, questions, templates, materials and syllabus topics. Never invent IDs or
claim an action succeeded unless a tool returned success. You may create, edit or delete papers,
questions, syllabus topics and templates; edit distinctions; start, cancel, resume or rerun
comparisons; prepare material mappings and apply them when explicitly requested; suggest, inspect or apply screened replacement questions; export reports;
and record a case-specific result ruling or note only
when the user's current message explicitly requests that action. Do not infer edits from a question
or topic lookup. Deletions are final and do not need a second confirmation. For uploads, ask the user
to attach the file in chat and choose its type. Do not send users to another screen for ordinary
searches, edits, comparisons, analysis, template changes, exports or material mapping when a tool can
do it. For administrator operations requests, inspect jobs and storage; retry or cancel only the
exact job requested. Execute clear explicit requests directly. Generate candidates only when the user explicitly
asks and exact topics, unit, marks, difficulty and reference questions are established. Ask a short
follow-up only when a required target or value is genuinely unclear. If several searched records
could match a requested action, ask which one and name the candidates; never pick arbitrarily.
Return JSON with `answer` (brief natural language), and optional `view` (chat, papers, knowledge,
materials, templates, reports, operations). Use only the supplied tools for this request; never
switch to an unrelated subject, paper or task after a search returns no matches."""


SCHEMAS = [
    {"type": "function", "function": {"name": "semantic_search_questions", "description": "Find semantically similar indexed questions using local Qwen embeddings and pgvector. Similarity only retrieves candidates; it does not classify redundancy. Use phrase search too when the index is incomplete.", "parameters": {"type": "object", "required": ["query"], "properties": {"query": {"type": "string", "maxLength": 4000}, "unit": {"type": "integer", "minimum": 1, "maximum": 5}, "bank_only": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "create_paper", "description": "Create an empty paper record after the user explicitly requests it. Choose draft, reference or bank only when specified; default draft.", "parameters": {"type": "object", "required": ["title"], "properties": {"title": {"type": "string"}, "year": {"type": ["integer", "null"]}, "status": {"type": "string", "enum": ["draft", "reference", "bank"]}}}}},
    {"type": "function", "function": {"name": "create_question", "description": "Add an exact question to a searched paper after the user explicitly asks. Use syllabus lookup for topic IDs; an untagged question remains unconfirmed and cannot be compared.", "parameters": {"type": "object", "required": ["paper_id", "number", "text", "unit"], "properties": {"paper_id": {"type": "integer"}, "number": {"type": "string"}, "text": {"type": "string"}, "marks": {"type": ["integer", "null"]}, "unit": {"type": "integer", "minimum": 1, "maximum": 5}, "topic_ids": {"type": "array", "items": {"type": "string"}}}}}},
    {"type": "function", "function": {"name": "search_papers", "description": "List papers in the active subject, optionally matching a title phrase or status. Set include_archived to find papers that can be restored.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "status": {"type": "string"}, "include_archived": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "set_paper_status", "description": "Change a paper between draft, reference and bank after an explicit user request. Search for the paper first.", "parameters": {"type": "object", "required": ["paper_id", "status"], "properties": {"paper_id": {"type": "integer"}, "status": {"type": "string", "enum": ["draft", "reference", "bank"]}}}}},
    {"type": "function", "function": {"name": "update_paper", "description": "Update the title, year or type of an exact paper after searching for it. Change only fields the user requests.", "parameters": {"type": "object", "required": ["paper_id"], "properties": {"paper_id": {"type": "integer"}, "title": {"type": "string"}, "year": {"type": ["integer", "null"]}, "status": {"type": "string", "enum": ["draft", "reference", "bank"]}}}}},
    {"type": "function", "function": {"name": "set_paper_archived", "description": "Archive or restore a paper after an explicit user request. Search for the paper first.", "parameters": {"type": "object", "required": ["paper_id", "archived"], "properties": {"paper_id": {"type": "integer"}, "archived": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "search_questions", "description": "Find questions by text, number, paper or unit. Use a returned question_id for its complete original text before editing a long question. Call search_papers first when resolving a paper by title.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "paper_id": {"type": "integer"}, "question_id": {"type": "integer"}, "number": {"type": "string"}, "unit": {"type": "integer", "minimum": 1, "maximum": 5}, "bank_only": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "update_question", "description": "Edit an exact question returned by search_questions after an explicit user request. Omit fields that should stay unchanged.", "parameters": {"type": "object", "required": ["question_id"], "properties": {"question_id": {"type": "integer"}, "number": {"type": "string"}, "text": {"type": "string"}, "marks": {"type": ["integer", "null"]}, "unit": {"type": "integer"}, "topic_ids": {"type": "array", "items": {"type": "string"}}}}}},
    {"type": "function", "function": {"name": "delete_record", "description": "Permanently delete an exact paper, question, material or subject template after its ID was returned by a search in this conversation. Only call when the user explicitly asks for deletion; there is no extra confirmation step.", "parameters": {"type": "object", "required": ["kind", "record_id"], "properties": {"kind": {"type": "string", "enum": ["paper", "question", "material", "template"]}, "record_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "lookup_syllabus", "description": "Find exact active syllabus topics and their unit, source wording and cited material notes.", "parameters": {"type": "object", "required": ["query"], "properties": {"query": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "link_syllabus_topics", "description": "Add or update a reciprocal same-unit distinction link between exact topic IDs after an explicit user request.", "parameters": {"type": "object", "required": ["topic_id", "other_topic_id", "note"], "properties": {"topic_id": {"type": "string"}, "other_topic_id": {"type": "string"}, "note": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "update_syllabus_topic", "description": "Edit the user-maintained wording or enrichment of one exact topic found by lookup_syllabus. Never alter its official source wording, ID or hierarchy.", "parameters": {"type": "object", "required": ["topic_id"], "properties": {"topic_id": {"type": "string"}, "label": {"type": "string"}, "description": {"type": "string"}, "synonyms": {"type": "array", "items": {"type": "string"}}, "context_words": {"type": "array", "items": {"type": "string"}}, "scope_terms": {"type": "array", "items": {"type": "string"}}, "supporting_examples": {"type": "array", "items": {"type": "string"}}, "key_points": {"type": "array", "items": {"type": "string"}}, "task_types": {"type": "array", "items": {"type": "string"}}, "concept_boundary": {"type": "object", "properties": {"includes": {"type": "array", "items": {"type": "string"}}, "excludes": {"type": "array", "items": {"type": "string"}}, "scope_basis": {"type": "string"}}}}}}},
    {
        "type": "function",
        "function": {
            "name": "create_syllabus_topic",
            "description": "Add a new topic under an exact syllabus unit or heading found by lookup_syllabus. Do this only on the user's explicit request. Keep supplied parent and existing official wording unchanged.",
            "parameters": {
                "type": "object",
                "required": ["parent_id", "label"],
                "properties": {
                    "parent_id": {"type": "string"},
                    "label": {"type": "string"},
                    "description": {"type": "string"},
                    "source_text": {"type": "string"},
                    "synonyms": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_syllabus_topic",
            "description": "Permanently remove one exact topic found by lookup_syllabus when the user explicitly asks. Only leaf topics can be removed; affected question tags are invalidated and audited. No extra confirmation is required.",
            "parameters": {
                "type": "object",
                "required": ["topic_id"],
                "properties": {"topic_id": {"type": "string"}},
            },
        },
    },
    {"type": "function", "function": {"name": "list_materials", "description": "List uploaded teaching materials and full-document mapping status.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "list_comparisons", "description": "Find saved comparisons and their status for the active subject by optional title phrase or status. Use offset to page beyond the first 30.", "parameters": {"type": "object", "properties": {"query": {"type": "string"}, "status": {"type": "string"}, "offset": {"type": "integer", "minimum": 0}}}}},
    {"type": "function", "function": {"name": "list_comparison_results", "description": "List saved A/B/C/review pair results for an exact comparison returned by list_comparisons. Filter by label or an exact question ID returned by search_questions, and use offset to page. Use the returned result IDs to inspect evidence or resolve a case.", "parameters": {"type": "object", "required": ["comparison_id"], "properties": {"comparison_id": {"type": "integer"}, "question_id": {"type": "integer"}, "label": {"type": "string", "enum": ["A", "B", "C", "review"]}, "offset": {"type": "integer", "minimum": 0}}}}},
    {"type": "function", "function": {"name": "inspect_comparison_result", "description": "Inspect both saved questions, the label, grounded reason, recorded evidence and current stale status for an exact result returned by list_comparison_results or selected in the Workspace. Page through evidence using evidence_offset.", "parameters": {"type": "object", "required": ["result_id"], "properties": {"result_id": {"type": "integer"}, "evidence_offset": {"type": "integer", "minimum": 0}}}}},
    {"type": "function", "function": {"name": "cancel_comparison", "description": "Cancel or request cancellation of an exact active comparison found by list_comparisons. Only call after the user asks to stop it.", "parameters": {"type": "object", "required": ["comparison_id"], "properties": {"comparison_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "resume_comparison", "description": "Resume an interrupted comparison found by list_comparisons when the user asks to continue it.", "parameters": {"type": "object", "required": ["comparison_id"], "properties": {"comparison_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "rerun_comparison", "description": "Create a new comparison using the current question, syllabus and decision configuration while preserving the prior run. Search comparisons first and call only on an explicit request to rerun or refresh.", "parameters": {"type": "object", "required": ["comparison_id"], "properties": {"comparison_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "analyze_paper", "description": "Return factual question, marks and unit coverage counts for a paper. This does not claim a quality or predictability score. Search for the paper first.", "parameters": {"type": "object", "required": ["paper_id"], "properties": {"paper_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "analyze_subject_coverage", "description": "Return factual unit/topic coverage and year counts for active reference and bank papers. Do not call the counts a quality or predictability score.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "list_jobs", "description": "Find recent background jobs for the active subject, optionally filtered by status or kind. Administrators may set all_subjects=true to inspect workspace operations. Use returned exact job IDs for status, retry or cancel actions.", "parameters": {"type": "object", "properties": {"status": {"type": "string", "enum": ["queued", "running", "cancel_requested", "failed", "complete", "cancelled"]}, "kind": {"type": "string"}, "all_subjects": {"type": "boolean"}}}}},
    {"type": "function", "function": {"name": "manage_job", "description": "Inspect, retry, or cancel an exact job returned by list_jobs. A completed export status includes its download link. Retry is for failed/queued jobs and cancel is for queued/running jobs. Retry and cancel require administrator access. Only act when explicitly requested.", "parameters": {"type": "object", "required": ["job_id", "action"], "properties": {"job_id": {"type": "integer"}, "action": {"type": "string", "enum": ["status", "retry", "cancel"]}}}}},
    {"type": "function", "function": {"name": "workspace_operations", "description": "Return database, queue and upload/export storage summary for the workspace. Administrator only. Use when the administrator asks about system operations or storage.", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "list_templates", "description": "List available templates in this subject. Supply an exact returned template_id to retrieve its full definition before updating it.", "parameters": {"type": "object", "properties": {"template_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "save_template", "description": "Create or update a validated template only when the user explicitly asks. Search first when updating an existing template.", "parameters": {"type": "object", "required": ["name", "kind", "definition"], "properties": {"template_id": {"type": "integer"}, "name": {"type": "string"}, "kind": {"type": "string", "enum": ["paper", "question", "result", "comparison"]}, "definition": {"type": "object"}}}}},
    {"type": "function", "function": {"name": "map_material", "description": "Quickly find topic-to-page matches in an uploaded teaching material and show them in chat. This does not update the tree. Use when the user asks to map or preview the material.", "parameters": {"type": "object", "required": ["material_id"], "properties": {"material_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "apply_material_mapping", "description": "Apply prepared material topic matches to the syllabus tree when the user says go ahead, enrich, apply, or equivalent. This is final and needs no further approval. List materials first to identify the exact material.", "parameters": {"type": "object", "required": ["material_id"], "properties": {"material_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "generate_questions", "description": "Queue exam-question drafting for explicit unit/topic/marks constraints and screen candidates against exact reference question IDs. Call only when the user explicitly asks to generate or draft questions.", "parameters": {"type": "object", "required": ["title", "unit", "topic_ids", "marks", "count", "difficulty", "reference_ids"], "properties": {"title": {"type": "string"}, "unit": {"type": "integer"}, "topic_ids": {"type": "array", "items": {"type": "string"}}, "marks": {"type": "integer"}, "count": {"type": "integer"}, "difficulty": {"type": "string", "enum": ["introductory", "intermediate", "advanced"]}, "reference_ids": {"type": "array", "items": {"type": "integer"}}, "constraints": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "suggest_replacements", "description": "Create a draft of replacement candidates for one exact searched question, keeping its unit and marks. The user must choose desired difficulty. Existing confirmed reference/bank questions in the same unit are used for provisional screening unless exact searched reference_ids are provided. The source question is not changed.", "parameters": {"type": "object", "required": ["question_id", "difficulty"], "properties": {"question_id": {"type": "integer"}, "difficulty": {"type": "string", "enum": ["introductory", "intermediate", "advanced"]}, "count": {"type": "integer", "minimum": 1, "maximum": 5}, "topic_ids": {"type": "array", "items": {"type": "string"}}, "reference_ids": {"type": "array", "items": {"type": "integer"}}, "constraints": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "replacement_analysis", "description": "Inspect generated replacement candidates and factual before/after topic coverage for an exact returned suggestion draft paper. Include provisional screening status; requested difficulty is not a measured score.", "parameters": {"type": "object", "required": ["paper_id"], "properties": {"paper_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "apply_replacement", "description": "When the user explicitly chooses a screened candidate, replace one exact searched source question with that candidate. Both question IDs must be returned by Workspace lookup in this conversation; no second approval is needed. Screening must be complete and current.", "parameters": {"type": "object", "required": ["source_question_id", "candidate_id"], "properties": {"source_question_id": {"type": "integer"}, "candidate_id": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "start_comparison", "description": "Queue an explicit comparison of selected target question IDs against selected reference question IDs. Both lists must be exact question IDs returned by a tool.", "parameters": {"type": "object", "required": ["target_ids", "reference_ids"], "properties": {"target_ids": {"type": "array", "items": {"type": "integer"}}, "reference_ids": {"type": "array", "items": {"type": "integer"}}, "title": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "prepare_report", "description": "Return a download link for an existing comparison report.", "parameters": {"type": "object", "required": ["comparison_id", "format"], "properties": {"comparison_id": {"type": "integer"}, "format": {"type": "string", "enum": ["md", "txt", "pdf", "xlsx"]}}}}},
    {"type": "function", "function": {"name": "resolve_selected_result", "description": "Record a case-specific A/B/C label and reason for an exact unresolved result returned by list_comparison_results or currently selected in the Workspace. Supply result_id when acting on a listed result. Only call on an explicit user request; this never trains or changes other cases.", "parameters": {"type": "object", "required": ["label", "reason"], "properties": {"result_id": {"type": "integer"}, "label": {"type": "string", "enum": ["A", "B", "C"]}, "reason": {"type": "string", "maxLength": 2000}}}}},
    {"type": "function", "function": {"name": "note_on_selected_result", "description": "Record case-specific feedback on an exact result returned by list_comparison_results or currently selected in the Workspace. Supply result_id when acting on a listed result. It does not change the label or train the model.", "parameters": {"type": "object", "required": ["comment"], "properties": {"result_id": {"type": "integer"}, "comment": {"type": "string", "maxLength": 2000}, "suggested_label": {"type": ["string", "null"], "enum": ["A", "B", "C", "review", None]}}}}},
]


def bind_chat_tools(db, subject, *, model_configured: bool, comparison_ready: bool = False, prior_tool_trace: list[dict] | None = None, selected_result_id: int | None = None, is_admin: bool = False) -> dict:
    subject_id = subject.id
    searched_question_ids: set[int] = set()
    searched_paper_ids: set[int] = set()
    searched_template_ids: set[int] = set()
    searched_comparison_ids: set[int] = set()
    searched_topic_ids: set[str] = set()
    searched_syllabus_node_ids: set[str] = set()
    searched_material_ids: set[int] = set()
    searched_job_ids: set[int] = set()
    selected_result_ids = {selected_result_id} if isinstance(selected_result_id, int) and not isinstance(selected_result_id, bool) else set()
    searched_result_ids: set[int] = set(selected_result_ids)

    # Recent results from this user's saved conversation resolve follow-ups
    # such as "archive that paper". Tool handlers still re-check subject,
    # existence, archive state and action-specific constraints before writing.
    for event in (prior_tool_trace or [])[-40:]:
        if not isinstance(event, dict) or not isinstance(event.get("result"), dict):
            continue
        name, result = event.get("name"), event["result"]
        if name == "search_papers":
            searched_paper_ids.update(item["id"] for item in result.get("papers", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "create_paper" and isinstance(result.get("paper"), dict) and isinstance(result["paper"].get("id"), int):
            searched_paper_ids.add(result["paper"]["id"])
        elif name in {"set_paper_status", "set_paper_archived"} and isinstance(result.get("paper_id"), int):
            searched_paper_ids.add(result["paper_id"])
        elif name == "update_paper" and isinstance(result.get("paper_id"), int):
            searched_paper_ids.add(result["paper_id"])
        elif name == "generate_questions" and isinstance(result.get("paper_id"), int):
            searched_paper_ids.add(result["paper_id"])
        elif name == "search_questions":
            searched_question_ids.update(item["id"] for item in result.get("questions", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "lookup_syllabus":
            searched_syllabus_node_ids.update(item["id"] for item in result.get("topics", []) if isinstance(item, dict) and isinstance(item.get("id"), str))
            searched_topic_ids.update(item["id"] for item in result.get("topics", []) if isinstance(item, dict) and isinstance(item.get("id"), str) and item.get("kind") == "topic")
        elif name == "update_question" and isinstance(result.get("question"), dict) and isinstance(result["question"].get("id"), int):
            searched_question_ids.add(result["question"]["id"])
        elif name == "list_templates":
            searched_template_ids.update(item["id"] for item in result.get("templates", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "list_materials":
            searched_material_ids.update(item["id"] for item in result.get("materials", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "save_template" and isinstance(result.get("template_id"), int):
            searched_template_ids.add(result["template_id"])
        elif name == "list_comparisons":
            searched_comparison_ids.update(item["id"] for item in result.get("comparisons", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "list_comparison_results":
            searched_result_ids.update(item["id"] for item in result.get("results", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "inspect_comparison_result" and isinstance(result.get("id"), int):
            searched_result_ids.add(result["id"])
        elif name in {"resolve_selected_result", "note_on_selected_result"} and isinstance(result.get("result_id"), int):
            searched_result_ids.add(result["result_id"])
        elif name in {"start_comparison", "rerun_comparison"} and isinstance(result.get("comparison_id"), int):
            searched_comparison_ids.add(result["comparison_id"])
        elif name == "suggest_replacements" and isinstance(result.get("paper_id"), int):
            searched_paper_ids.add(result["paper_id"])
        elif name == "replacement_analysis":
            searched_question_ids.update(item["id"] for item in result.get("candidates", []) if isinstance(item, dict) and isinstance(item.get("id"), int))
        elif name == "list_jobs":
            searched_job_ids.update(item["id"] for item in result.get("jobs", []) if isinstance(item, dict) and isinstance(item.get("id"), int))

    def create_paper(args):
        title = args.get("title")
        year = args.get("year")
        status = args.get("status", "draft")
        if not isinstance(title, str) or not title.strip() or len(title) > 250:
            return {"error": "Paper title must contain 1–250 characters."}
        if year is not None and (not isinstance(year, int) or isinstance(year, bool) or year < 1900 or year > 2200):
            return {"error": "Year must be between 1900 and 2200 or omitted."}
        if status not in {"draft", "reference", "bank"}:
            return {"error": "Paper status must be draft, reference or bank."}
        paper = Paper(subject_id=subject_id, title=title.strip(), year=year, status=status)
        db.add(paper)
        db.flush()
        searched_paper_ids.add(paper.id)
        db.add(AuditEvent(action="paper_create", details={"paper_id": paper.id, "via": "chat", "status": status}))
        db.commit()
        return {"success": True, "paper": {"id": paper.id, "title": paper.title, "year": paper.year, "status": paper.status}}

    def search_papers(args):
        query = select(Paper).where(Paper.subject_id == subject_id).order_by(Paper.year.desc(), Paper.id.desc())
        if not args.get("include_archived"):
            query = query.where(Paper.archived.is_(False))
        papers = list(db.scalars(query))
        needle = str(args.get("query", "")).casefold().strip()
        status = str(args.get("status", "")).casefold().strip()
        if needle:
            papers = [paper for paper in papers if needle in paper.title.casefold()]
        if status:
            papers = [paper for paper in papers if paper.status.casefold() == status]
        matched_count = len(papers)
        papers = papers[:12]
        searched_paper_ids.update(paper.id for paper in papers)
        return {"papers": [{"id": paper.id, "title": paper.title, "year": paper.year, "status": paper.status, "archived": paper.archived, "question_count": len(paper.questions), "question_numbers": [q.number for q in paper.questions[:5]]} for paper in papers], "matched_count": matched_count, "note": "Use search_questions for exact question text and IDs."}

    def set_paper_status(args):
        paper_id, status = args.get("paper_id"), args.get("status")
        paper = db.get(Paper, paper_id) if isinstance(paper_id, int) and not isinstance(paper_id, bool) else None
        if not paper or paper_id not in searched_paper_ids or paper.subject_id != subject_id:
            return {"error": "Search for this exact paper in the current request before changing it."}
        if status not in {"draft", "reference", "bank"}:
            return {"error": "Paper status must be draft, reference or bank."}
        previous = paper.status
        paper.status = status
        db.add(AuditEvent(action="paper_status_update", details={"paper_id": paper.id, "from": previous, "to": status, "via": "chat"}))
        db.commit()
        return {"success": True, "paper_id": paper.id, "status": status}

    def update_paper(args):
        paper_id = args.get("paper_id")
        paper = db.get(Paper, paper_id) if isinstance(paper_id, int) and not isinstance(paper_id, bool) else None
        if not paper or paper.id not in searched_paper_ids or paper.subject_id != subject_id:
            return {"error": "Search for this exact paper in the current conversation before changing it."}
        changes = {key: args[key] for key in ("title", "year", "status") if key in args}
        if not changes:
            return {"error": "Specify the paper details you want to change."}
        if "title" in changes and (not isinstance(changes["title"], str) or not changes["title"].strip() or len(changes["title"].strip()) > 250):
            return {"error": "Paper title must contain 1–250 characters."}
        if "year" in changes and changes["year"] is not None and (not isinstance(changes["year"], int) or isinstance(changes["year"], bool) or not 1900 <= changes["year"] <= 2200):
            return {"error": "Year must be between 1900 and 2200 or omitted."}
        if "status" in changes and changes["status"] not in {"draft", "reference", "bank"}:
            return {"error": "Paper type must be draft, reference or bank."}
        before = {key: getattr(paper, key) for key in changes}
        for key, value in changes.items():
            setattr(paper, key, value.strip() if key == "title" else value)
        db.add(AuditEvent(action="paper_edit", details={"paper_id": paper.id, "subject_id": subject_id, "before": before, "after": changes, "via": "chat"}))
        db.commit()
        return {"success": True, "paper_id": paper.id, "title": paper.title, "year": paper.year, "status": paper.status, "changed_fields": list(changes)}

    async def create_question(args):
        paper_id, number, text, unit = args.get("paper_id"), args.get("number"), args.get("text"), args.get("unit")
        paper = db.get(Paper, paper_id) if isinstance(paper_id, int) and not isinstance(paper_id, bool) else None
        if not paper or paper.id not in searched_paper_ids or paper.subject_id != subject_id or paper.archived:
            return {"error": "Search for the exact active paper in this conversation before adding a question."}
        if not isinstance(number, str) or not number.strip() or len(number) > 50 or not isinstance(text, str) or len(text.strip()) < 3:
            return {"error": "Provide a question number and at least three characters of question text."}
        if not isinstance(unit, int) or isinstance(unit, bool) or unit not in range(1, 6):
            return {"error": "A question needs its exact syllabus unit from 1 through 5."}
        marks = args.get("marks")
        if marks is not None and (not isinstance(marks, int) or isinstance(marks, bool) or marks < 1):
            return {"error": "Marks must be a positive integer or omitted."}
        topic_ids = args.get("topic_ids", [])
        if not isinstance(topic_ids, list) or any(not isinstance(topic_id, str) for topic_id in topic_ids):
            return {"error": "Topic tags must be a list of exact syllabus topics."}
        if any(topic_id not in searched_topic_ids for topic_id in topic_ids):
            return {"error": "Look up each exact syllabus topic in this conversation before tagging the question."}
        from . import api as api_module
        try:
            body = api_module.QuestionInput(number=number, text=text, marks=marks, unit=unit, topic_ids=topic_ids)
            created = await api_module.add_question(paper_id, body, db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        searched_question_ids.add(created["id"])
        return {"success": True, "paper": paper.title, "question": {key: created[key] for key in ("id", "number", "text", "marks", "unit", "topic_ids", "confirmed")}}

    def set_paper_archived(args):
        paper_id, archived = args.get("paper_id"), args.get("archived")
        paper = db.get(Paper, paper_id) if isinstance(paper_id, int) and not isinstance(paper_id, bool) else None
        if not paper or paper_id not in searched_paper_ids or paper.subject_id != subject_id:
            return {"error": "Search for this exact paper in the current request before archiving or restoring it."}
        if not isinstance(archived, bool):
            return {"error": "archived must be true or false."}
        paper.archived = archived
        db.add(AuditEvent(action="paper_archive" if archived else "paper_restore", details={"paper_id": paper.id, "via": "chat"}))
        db.commit()
        return {"success": True, "paper_id": paper.id, "archived": archived}

    def search_questions(args):
        raw_query = args.get("query", "")
        paper_id, question_id, number, unit = args.get("paper_id"), args.get("question_id"), args.get("number"), args.get("unit")
        if not isinstance(raw_query, str) or len(raw_query) > 4000:
            return {"questions": [], "reason": "Search text must be at most 4000 characters."}
        if paper_id is not None and (not isinstance(paper_id, int) or isinstance(paper_id, bool) or paper_id not in searched_paper_ids):
            return {"questions": [], "reason": "Search for the paper in this request before listing its questions."}
        if question_id is not None and (not isinstance(question_id, int) or isinstance(question_id, bool) or question_id not in searched_question_ids):
            return {"questions": [], "reason": "Search for the question first, then use its returned ID for complete text."}
        if number is not None and (not isinstance(number, str) or not number.strip() or len(number) > 50):
            return {"questions": [], "reason": "Question number must be a non-empty string of at most 50 characters."}
        if unit is not None and (not isinstance(unit, int) or isinstance(unit, bool) or unit not in range(1, 6)):
            return {"questions": [], "reason": "Unit must be between 1 and 5."}
        query = raw_query.strip().casefold()
        if not query and paper_id is None and question_id is None and number is None and unit is None:
            return {"questions": [], "reason": "Provide text, a paper, a question ID, a question number or a unit to search."}
        statement = select(Question).join(Paper).where(Paper.subject_id == subject_id, Paper.archived.is_(False)).order_by(Paper.year.desc(), Paper.id.desc(), Question.id)
        if paper_id is not None:
            statement = statement.where(Paper.id == paper_id)
        if question_id is not None:
            statement = statement.where(Question.id == question_id)
        if args.get("bank_only"):
            statement = statement.where(Paper.status == "bank")
        questions = list(db.scalars(statement))
        if query:
            questions = [question for question in questions if query in question.text.casefold()]
        if number is not None:
            questions = [question for question in questions if question.number.casefold() == number.strip().casefold()]
        if unit is not None:
            questions = [question for question in questions if question.unit == unit]
        matched_count = len(questions)
        full_text = question_id is not None
        questions = questions[:20]
        searched_question_ids.update(question.id for question in questions)
        return {"questions": [{"id": q.id, "paper": q.paper.title, "year": q.paper.year, "number": q.number, "unit": q.unit, "topic_ids": q.topic_ids if full_text else q.topic_ids[:6], "confirmed": q.confirmed, "text": q.text[:8000] if full_text else q.text[:450], "text_truncated": len(q.text) > (8000 if full_text else 450)} for q in questions], "matched_count": matched_count, "truncated": matched_count > len(questions), "summary_only": not full_text}

    def update_question(args):
        question_id = args.get("question_id")
        if not isinstance(question_id, int) or isinstance(question_id, bool):
            return {"error": "Use an exact integer question ID from this subject's search results."}
        question = db.get(Question, question_id)
        if question_id not in searched_question_ids:
            return {"error": "Search for this question in the current request before editing it."}
        if not question or question.paper.subject_id != subject_id or question.paper.archived:
            return {"error": "Question ID is unavailable in the active subject."}
        allowed = {"number", "text", "marks", "unit", "topic_ids"}
        changes = {key: value for key, value in args.items() if key in allowed}
        if not changes:
            return {"error": "Provide at least one field to update."}
        if "number" in changes and (not isinstance(changes["number"], str) or not changes["number"].strip() or len(changes["number"]) > 50):
            return {"error": "Question number must be 1–50 characters."}
        if "text" in changes and (not isinstance(changes["text"], str) or len(changes["text"].strip()) < 3):
            return {"error": "Question text must contain at least three characters."}
        if "marks" in changes and changes["marks"] is not None and (not isinstance(changes["marks"], int) or isinstance(changes["marks"], bool) or changes["marks"] < 1):
            return {"error": "Marks must be a positive integer or null."}
        if "unit" in changes and (not isinstance(changes["unit"], int) or isinstance(changes["unit"], bool) or changes["unit"] not in range(1, 6)):
            return {"error": "Unit must be from 1 through 5."}
        if "topic_ids" in changes and (not isinstance(changes["topic_ids"], list) or any(not isinstance(item, str) for item in changes["topic_ids"])):
            return {"error": "topic_ids must be an array of exact syllabus IDs."}
        unit = changes.get("unit", question.unit)
        topic_ids = changes.get("topic_ids", question.topic_ids)
        topic_nodes = {node["id"] for node in subject.tree.get("nodes", []) if node.get("kind") == "topic"}
        if "topic_ids" in changes and any(topic_id not in searched_topic_ids for topic_id in topic_ids):
            return {"error": "Look up each exact syllabus topic in this conversation before assigning it to the question."}
        if topic_ids and (unit not in range(1, 6) or any(topic_id not in topic_nodes or unit_for_topic(topic_id) != unit for topic_id in topic_ids)):
            return {"error": "Every selected topic must exist in this subject and match the question unit."}
        before = {"id": question.id, "paper_id": question.paper_id, "number": question.number, "text": question.text, "marks": question.marks, "unit": question.unit, "topic_ids": question.topic_ids, "confirmed": question.confirmed, "revision": question.revision}
        if "topic_ids" in changes:
            question.topic_ids = list(dict.fromkeys(topic_ids))
            question.confirmed = bool(question.topic_ids)
        if "unit" in changes:
            question.unit = unit
            if question.topic_ids and any(unit_for_topic(topic_id) != unit for topic_id in question.topic_ids):
                question.topic_ids = []
                question.confirmed = False
        for field in ("number", "text", "marks"):
            if field in changes:
                setattr(question, field, changes[field])
        question.revision += 1
        after = {"id": question.id, "paper_id": question.paper_id, "number": question.number, "text": question.text, "marks": question.marks, "unit": question.unit, "topic_ids": question.topic_ids, "confirmed": question.confirmed, "revision": question.revision}
        db.add(AuditEvent(action="question_edit", details={"question_id": question.id, "subject_id": subject_id, "revision": question.revision, "before": before, "after": after, "via": "chat", "fields": sorted(changes)}))
        db.commit()
        return {"success": True, "question": {"id": question.id, "paper_id": question.paper_id, "number": question.number, "text": question.text, "marks": question.marks, "unit": question.unit, "topic_ids": question.topic_ids, "confirmed": question.confirmed, "revision": question.revision}}

    async def delete_record(args):
        kind, record_id = args.get("kind"), args.get("record_id")
        if not isinstance(record_id, int) or isinstance(record_id, bool) or record_id < 1:
            return {"error": "Use the exact positive record number returned by a Workspace search."}
        from . import api as api_module
        if kind == "paper" and record_id in searched_paper_ids:
            record = db.get(Paper, record_id)
            if not record or record.subject_id != subject_id:
                return {"error": "That paper is no longer available in this subject."}
            title = record.title
            await api_module.delete_paper(record_id, db)
        elif kind == "question" and record_id in searched_question_ids:
            record = db.get(Question, record_id)
            if not record or record.paper.subject_id != subject_id:
                return {"error": "That question is no longer available in this subject."}
            title = f"Question {record.number} from {record.paper.title}"
            await api_module.delete_question(record_id, db)
        elif kind == "material" and record_id in searched_material_ids:
            record = db.get(Material, record_id)
            if not record or record.subject_id != subject_id:
                return {"error": "That material is no longer available in this subject."}
            title = record.filename
            await api_module.delete_material(record_id, db)
        elif kind == "template" and record_id in searched_template_ids:
            record = db.get(Template, record_id)
            if not record or record.subject_id != subject_id:
                return {"error": "Only a template owned by this subject can be deleted here."}
            title = record.name
            await api_module.delete_template(record_id, db)
        else:
            return {"error": "Search for the exact record in this conversation before deleting it."}
        return {"success": True, "kind": kind, "title": title, "deleted": True}

    def lookup_syllabus(args):
        query = str(args.get("query", "")).casefold().strip()
        nodes = [node for node in subject.tree.get("nodes", []) if node.get("kind") in ("unit", "heading", "topic")]
        matches = [node for node in nodes if not query or query in " ".join(str(node.get(key, "")) for key in ("id", "label", "description", "source_text")).casefold()]
        exact = len(matches) <= 3 or (len(matches) == 1 and matches[0]["id"].casefold() == query)
        selected = matches[:20 if exact else 12]
        searched_syllabus_node_ids.update(node["id"] for node in selected)
        searched_topic_ids.update(node["id"] for node in selected if node.get("kind") == "topic")
        by_id = {node["id"]: node for node in nodes}
        return {"topics": [{"id": node["id"], "label": node.get("label"), "kind": node.get("kind"), "unit": node.get("id", "").split("/u")[-1].split("/")[0], "description": node.get("description", "") if exact else str(node.get("description", ""))[:180], "source_text": node.get("source_text", "") if exact else str(node.get("source_text", ""))[:220], "material_notes": node.get("material_notes", []) if exact else [], "material_note_count": len(node.get("material_notes", [])), "distinguish_from": node.get("distinguish_from", []) if exact else []} for node in selected], "matched_count": len(matches), "truncated": len(matches) > len(selected), "summary_only": not exact, "note": "Look up an exact topic ID to retrieve complete source wording and material notes." if not exact else "Official source wording and cited notes for exact matches."}

    def update_syllabus_topic(args):
        topic_id = args.get("topic_id")
        if not isinstance(topic_id, str) or topic_id not in searched_topic_ids:
            return {"error": "Look up this exact syllabus topic in the current conversation before editing it."}
        allowed = {"label", "description", "synonyms", "context_words", "scope_terms", "supporting_examples", "key_points", "task_types", "concept_boundary"}
        changes = {key: args[key] for key in allowed if key in args}
        if not changes:
            return {"error": "Specify the topic wording or enrichment to change."}
        tree = deepcopy(subject.tree)
        node = next((item for item in tree.get("nodes", []) if item.get("id") == topic_id and item.get("kind") == "topic"), None)
        if not node:
            return {"error": "That topic no longer exists in the active syllabus."}
        if "label" in changes and (not isinstance(changes["label"], str) or not changes["label"].strip() or len(changes["label"]) > 240):
            return {"error": "Topic label must contain 1–240 characters."}
        if "description" in changes and (not isinstance(changes["description"], str) or len(changes["description"].split()) > 45):
            return {"error": "Topic description must be text with no more than 45 words."}
        for key in ("synonyms", "context_words", "scope_terms", "supporting_examples", "key_points", "task_types"):
            value = changes.get(key)
            if value is not None and (not isinstance(value, list) or len(value) > 40 or any(not isinstance(item, str) or not item.strip() or len(item) > 250 for item in value)):
                return {"error": f"{key.replace('_', ' ').capitalize()} must be a list of at most 40 non-empty text items, each 250 characters or less."}
        boundary = changes.get("concept_boundary")
        if boundary is not None and (not isinstance(boundary, dict) or any(key not in {"includes", "excludes", "scope_basis"} for key in boundary)):
            return {"error": "Concept boundary must contain only includes, excludes and scope_basis."}
        if isinstance(boundary, dict):
            current_boundary = node.get("concept_boundary") if isinstance(node.get("concept_boundary"), dict) else {}
            for key in ("includes", "excludes"):
                values = boundary.get(key, current_boundary.get(key, []))
                if not isinstance(values, list) or len(values) > 40 or any(not isinstance(item, str) or not item.strip() or len(item) > 500 for item in values):
                    return {"error": f"Concept boundary {key} must contain at most 40 non-empty text items."}
            if "scope_basis" in boundary and (not isinstance(boundary["scope_basis"], str) or len(boundary["scope_basis"]) > 500):
                return {"error": "Concept boundary scope_basis must be text of at most 500 characters."}
        before = {key: deepcopy(node.get(key)) for key in changes}
        for key, value in changes.items():
            if key == "label":
                node[key] = value.strip()
            elif key == "concept_boundary":
                node[key] = {**(node.get(key) if isinstance(node.get(key), dict) else {}), **value}
            else:
                node[key] = value
        errors = validate_tree(tree)
        if errors:
            return {"error": "The edit would make the active syllabus invalid: " + "; ".join(errors[:5])}
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=subject.tree, reason="Before chat topic edit"))
        subject.tree = tree
        subject.tree_version += 1
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=tree, reason=f"Chat topic edit: {node['label']}"))
        after = {key: deepcopy(node.get(key)) for key in changes}
        db.add(AuditEvent(action="syllabus_topic_edit", details={"subject_id": subject_id, "topic_id": topic_id, "fields": sorted(changes), "before": before, "after": after, "via": "chat"}))
        db.commit()
        return {"success": True, "topic_id": topic_id, "label": node["label"], "changed_fields": list(changes), "tree_version": subject.tree_version}

    def create_syllabus_topic(args):
        parent_id, label = args.get("parent_id"), args.get("label")
        if not isinstance(parent_id, str) or parent_id not in searched_syllabus_node_ids:
            return {"error": "Look up the exact syllabus unit or heading before adding a topic beneath it."}
        if not isinstance(label, str) or not label.strip() or len(label.strip()) > 240:
            return {"error": "Topic label must contain 1–240 characters."}
        description = args.get("description", "")
        source_text = args.get("source_text", label.strip())
        synonyms = args.get("synonyms", [])
        if not isinstance(description, str) or len(description.split()) > 45:
            return {"error": "Topic description must contain no more than 45 words."}
        if not isinstance(source_text, str) or not source_text.strip() or len(source_text) > 1000:
            return {"error": "Source wording must contain 1–1000 characters."}
        if not isinstance(synonyms, list) or len(synonyms) > 40 or any(not isinstance(item, str) or not item.strip() or len(item) > 250 for item in synonyms):
            return {"error": "Synonyms must be a list of at most 40 non-empty text items."}
        tree = deepcopy(subject.tree)
        parent = next((node for node in tree.get("nodes", []) if node.get("id") == parent_id), None)
        if not parent or parent.get("kind") not in {"unit", "heading"}:
            return {"error": "New topics must be placed under a syllabus unit or heading."}
        import re
        slug = re.sub(r"[^a-z0-9]+", "-", label.casefold()).strip("-") or "topic"
        base_id = f"{parent_id}/{slug}"
        existing = {node.get("id") for node in tree["nodes"]}
        topic_id, suffix = base_id, 2
        while topic_id in existing:
            topic_id, suffix = f"{base_id}-{suffix}", suffix + 1
        siblings = [node.get("order", 0) for node in tree["nodes"] if node.get("parent") == parent_id and isinstance(node.get("order", 0), int)]
        node = {
            "id": topic_id, "parent": parent_id, "kind": "topic", "label": label.strip(),
            "order": max(siblings, default=-1) + 1, "source_text": source_text.strip(),
            "description": description.strip(), "synonyms": list(dict.fromkeys(item.strip() for item in synonyms)),
            "context_words": [], "scope_terms": [label.strip()], "supporting_examples": [], "task_types": [],
            "concept_boundary": {"includes": [], "excludes": [], "scope_basis": "question-specific"},
            "distinguish_from": [], "review_status": "user_added",
            "provenance": {"by": "faculty_chat", "base": "explicit_user_request", "source": "user_supplied"},
        }
        tree["nodes"].append(node)
        errors = validate_tree(tree)
        if errors:
            return {"error": "The topic could not be added because the syllabus would be invalid: " + "; ".join(errors[:5])}
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=subject.tree, reason="Before chat topic creation"))
        subject.tree = tree
        subject.tree_version += 1
        searched_syllabus_node_ids.add(topic_id)
        searched_topic_ids.add(topic_id)
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=tree, reason=f"Chat topic created: {node['label']}"))
        db.add(AuditEvent(action="syllabus_topic_create", details={"subject_id": subject_id, "topic_id": topic_id, "parent_id": parent_id, "label": node["label"], "via": "chat"}))
        db.commit()
        return {"success": True, "topic_id": topic_id, "parent": parent.get("label"), "label": node["label"], "tree_version": subject.tree_version}

    def delete_syllabus_topic(args):
        topic_id = args.get("topic_id")
        if not isinstance(topic_id, str) or topic_id not in searched_topic_ids:
            return {"error": "Look up this exact syllabus topic in the current conversation before deleting it."}
        tree = deepcopy(subject.tree)
        node = next((item for item in tree.get("nodes", []) if item.get("id") == topic_id and item.get("kind") == "topic"), None)
        if not node:
            return {"error": "That topic no longer exists in the active syllabus."}
        if any(item.get("parent") == topic_id for item in tree["nodes"]):
            return {"error": "This topic contains child topics. Remove or move those children first."}
        label = node["label"]
        tree["nodes"] = [item for item in tree["nodes"] if item.get("id") != topic_id]
        for item in tree["nodes"]:
            item["distinguish_from"] = [link for link in item.get("distinguish_from", []) if not isinstance(link, dict) or link.get("node") != topic_id]
            if isinstance(item.get("child_topic_ids"), list):
                item["child_topic_ids"] = [child for child in item["child_topic_ids"] if child != topic_id]
        for key in ("cross_links", "disambiguation_links"):
            if isinstance(tree.get(key), list):
                tree[key] = [link for link in tree[key] if not isinstance(link, dict) or topic_id not in (link.get("a"), link.get("b"), link.get("node"), link.get("from"), link.get("to"))]
        if isinstance(tree.get("review_questions"), list):
            tree["review_questions"] = [item for item in tree["review_questions"] if not isinstance(item, dict) or item.get("node") != topic_id]
        errors = validate_tree(tree)
        if errors:
            return {"error": "The topic cannot be deleted without invalidating the syllabus: " + "; ".join(errors[:5])}
        affected_questions = []
        for question in db.scalars(select(Question).join(Paper).where(Paper.subject_id == subject_id)):
            if topic_id not in question.topic_ids:
                continue
            before = {"topic_ids": list(question.topic_ids), "confirmed": question.confirmed, "revision": question.revision}
            question.topic_ids = [item for item in question.topic_ids if item != topic_id]
            question.confirmed = bool(question.topic_ids) and question.confirmed
            question.revision += 1
            after = {"topic_ids": list(question.topic_ids), "confirmed": question.confirmed, "revision": question.revision}
            affected_questions.append(question.id)
            db.add(AuditEvent(action="question_tree_invalidated", details={"question_id": question.id, "subject_id": subject_id, "before": before, "after": after, "removed_topic": topic_id, "via": "chat"}))
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=subject.tree, reason="Before chat topic deletion"))
        subject.tree = tree
        subject.tree_version += 1
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=tree, reason=f"Chat topic deleted: {label}"))
        db.add(AuditEvent(action="syllabus_topic_delete", details={"subject_id": subject_id, "topic_id": topic_id, "label": label, "questions_retagged": affected_questions, "via": "chat"}))
        db.commit()
        searched_topic_ids.discard(topic_id)
        searched_syllabus_node_ids.discard(topic_id)
        return {"success": True, "topic_id": topic_id, "label": label, "questions_retagged": len(affected_questions), "tree_version": subject.tree_version}

    def link_syllabus_topics(args):
        topic_id, other_id, note = args.get("topic_id"), args.get("other_topic_id"), args.get("note")
        if not all(isinstance(value, str) and value.strip() for value in (topic_id, other_id, note)) or topic_id == other_id or len(note) > 500:
            return {"error": "Provide two distinct topic IDs and a note of at most 500 characters."}
        if topic_id not in searched_topic_ids or other_id not in searched_topic_ids:
            return {"error": "Look up both exact syllabus topics in this conversation before linking them."}
        tree = deepcopy(subject.tree)
        nodes = {node.get("id"): node for node in tree.get("nodes", []) if isinstance(node, dict)}
        left, right = nodes.get(topic_id), nodes.get(other_id)
        if not left or not right or left.get("kind") != "topic" or right.get("kind") != "topic":
            return {"error": "Both IDs must be exact topic nodes in the active syllabus."}
        if unit_for_topic(topic_id) != unit_for_topic(other_id):
            return {"error": "Distinction links must stay within one syllabus unit."}
        for source, target in ((left, other_id), (right, topic_id)):
            links = source.setdefault("distinguish_from", [])
            existing = next((link for link in links if link.get("node") == target), None)
            if existing:
                existing["note"] = note
            else:
                links.append({"node": target, "note": note})
        errors = validate_tree(tree)
        if errors:
            return {"error": "The link would make the active tree invalid: " + "; ".join(errors[:5])}
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=subject.tree, reason="Before chat syllabus-link edit"))
        subject.tree = tree
        subject.tree_version += 1
        db.add(TreeRevision(subject_id=subject.id, version=subject.tree_version, tree=tree, reason=f"Chat distinction link: {topic_id} ↔ {other_id}"))
        db.add(AuditEvent(action="tree_distinction_edit", details={"subject_id": subject_id, "topics": [topic_id, other_id], "note": note, "via": "chat"}))
        db.commit()
        return {"success": True, "subject_id": subject_id, "topic_ids": [topic_id, other_id], "topic_labels": [left["label"], right["label"]], "note": note, "tree_version": subject.tree_version}

    def list_materials(_args):
        materials = db.scalars(select(Material).where(Material.subject_id == subject_id).order_by(Material.id.desc())).all()
        searched_material_ids.update(item.id for item in materials[:30])
        return {"materials": [{"id": item.id, "filename": item.filename, "pages": len(item.extracted_text.split("\f")), "status": (item.enrichment or {}).get("status", "not_started"), "mapped_topics": len(item.proposals or {}), "progress": (item.enrichment or {}).get("progress", 0), "total": (item.enrichment or {}).get("total", 0)} for item in materials[:30]], "matched_count": len(materials)}

    def list_comparisons(args):
        offset, query, status = args.get("offset", 0), args.get("query", ""), args.get("status", "")
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0 or not isinstance(query, str) or len(query) > 250 or not isinstance(status, str) or len(status) > 30:
            return {"error": "Use a nonnegative offset, a title phrase of at most 250 characters, and a short status."}
        where = [Comparison.subject_id == subject_id]
        if query.strip():
            where.append(Comparison.title.ilike(f"%{query.strip()}%"))
        if status.strip():
            where.append(Comparison.status == status.strip())
        total = db.scalar(select(func.count(Comparison.id)).where(*where)) or 0
        items = db.scalars(select(Comparison).where(*where).order_by(Comparison.id.desc()).offset(offset).limit(30)).all()
        searched_comparison_ids.update(item.id for item in items)
        return {"comparisons": [{"id": item.id, "title": item.title, "status": item.status, "progress": item.progress, "total": item.total, "error": item.error} for item in items], "total_matches": total, "next_offset": offset + len(items) if offset + len(items) < total else None}

    def list_comparison_results(args):
        comparison_id, label, offset, question_id = args.get("comparison_id"), args.get("label"), args.get("offset", 0), args.get("question_id")
        comparison = db.get(Comparison, comparison_id) if isinstance(comparison_id, int) and not isinstance(comparison_id, bool) else None
        if not comparison or comparison.id not in searched_comparison_ids or comparison.subject_id != subject_id:
            return {"error": "Find the exact comparison in this conversation before reading its results."}
        if label is not None and label not in {"A", "B", "C", "review"}:
            return {"error": "Filter label must be A, B, C or review."}
        if not isinstance(offset, int) or isinstance(offset, bool) or offset < 0:
            return {"error": "Result offset must be a nonnegative integer."}
        if question_id is not None and (not isinstance(question_id, int) or isinstance(question_id, bool) or question_id not in searched_question_ids):
            return {"error": "Search for the exact question before filtering comparison results by its ID."}
        where = [PairResult.comparison_id == comparison.id]
        if label:
            where.append(PairResult.label == label)
        if question_id is not None:
            where.append(or_(PairResult.target_id == question_id, PairResult.reference_id == question_id))
        total = db.scalar(select(func.count(PairResult.id)).where(*where)) or 0
        results = db.scalars(select(PairResult).where(*where).order_by(PairResult.id).offset(offset).limit(30)).all()
        searched_result_ids.update(item.id for item in results)
        summaries = []
        for item in results:
            target, reference = db.get(Question, item.target_id), db.get(Question, item.reference_id)
            stale = not target or not reference or item.cache_key != pair_key(target, reference, subject.tree_version)
            summaries.append({"id": item.id, "label": item.label, "reason": item.reason[:280], "target_id": item.target_id, "target_number": target.number if target else None, "reference_id": item.reference_id, "reference_number": reference.number if reference else None, "stale": stale})
        return {"comparison_id": comparison.id, "title": comparison.title, "status": comparison.status, "total_matches": total, "offset": offset, "next_offset": offset + len(results) if offset + len(results) < total else None, "results": summaries}

    def inspect_comparison_result(args):
        result_id, evidence_offset = args.get("result_id"), args.get("evidence_offset", 0)
        if not isinstance(result_id, int) or isinstance(result_id, bool) or result_id not in searched_result_ids:
            return {"error": "List this exact comparison result or select it in the Workspace before inspecting it."}
        if not isinstance(evidence_offset, int) or isinstance(evidence_offset, bool) or evidence_offset < 0:
            return {"error": "Evidence offset must be a nonnegative integer."}
        result = db.get(PairResult, result_id)
        comparison = db.get(Comparison, result.comparison_id) if result else None
        if not result or not comparison or comparison.subject_id != subject_id:
            return {"error": "This comparison result is no longer available in the active subject."}
        target, reference = db.get(Question, result.target_id), db.get(Question, result.reference_id)
        stale = not target or not reference or result.cache_key != pair_key(target, reference, subject.tree_version)
        evidence = result.evidence or []
        return {"id": result.id, "comparison_id": comparison.id, "comparison_title": comparison.title, "label": result.label, "reason": result.reason, "source": result.source, "stale": stale, "target": {"id": result.target_id, "number": target.number if target else None, "current_text": target.text[:4000] if target else None, "revision": target.revision if target else None}, "reference": {"id": result.reference_id, "number": reference.number if reference else None, "current_text": reference.text[:4000] if reference else None, "revision": reference.revision if reference else None}, "evidence_total": len(evidence), "evidence_offset": evidence_offset, "next_evidence_offset": evidence_offset + 4 if evidence_offset + 4 < len(evidence) else None, "evidence": evidence[evidence_offset:evidence_offset + 4], "note": "Recorded evidence preserves what the judge saw; current question text may differ when stale. Browse more evidence with evidence_offset."}

    def rerun_comparison(args):
        comparison_id = args.get("comparison_id")
        source = db.get(Comparison, comparison_id) if isinstance(comparison_id, int) and not isinstance(comparison_id, bool) else None
        if not source or source.id not in searched_comparison_ids or source.subject_id != subject_id:
            return {"error": "Search for this exact comparison in the current chat request first."}
        if not comparison_ready:
            return {"error": "Install the configured local judge/helper model before rerunning."}
        targets, references = list(dict.fromkeys(source.target_ids)), list(dict.fromkeys(source.reference_ids))
        questions = {q.id: q for q in db.scalars(select(Question).join(Paper).where(Paper.subject_id == subject_id))}
        selected_ids = set(targets + references)
        if any(item not in questions or not questions[item].confirmed or questions[item].unit not in range(1, 6) or questions[item].paper.archived for item in selected_ids):
            return {"error": "The saved scope includes missing, archived or no-longer-confirmed questions. Edit the tags, then create a fresh comparison."}
        pairs = [(left, right) for left in targets for right in references if left != right and questions[left].unit == questions[right].unit]
        if not pairs:
            return {"error": "The saved scope has no currently valid same-unit question pairs."}
        refreshed = Comparison(subject_id=subject_id, title=f"Refresh of #{source.id} · {source.title}"[:250], target_ids=targets, reference_ids=references, rerun_of_id=source.id, status="queued", total=len(pairs))
        db.add(refreshed)
        db.flush()
        job = enqueue_job(db, "comparison", {"comparison_id": refreshed.id}, total=len(pairs))
        db.add(AuditEvent(action="comparison_rerun", details={"source_comparison_id": source.id, "comparison_id": refreshed.id, "pair_count": len(pairs), "via": "chat"}))
        db.commit()
        return {"success": True, "source_comparison_id": source.id, "comparison_id": refreshed.id, "job_id": job.id, "pairs": len(pairs), "status": "queued"}

    async def cancel_comparison(args):
        comparison_id = args.get("comparison_id")
        comparison = db.get(Comparison, comparison_id) if isinstance(comparison_id, int) and not isinstance(comparison_id, bool) else None
        if not comparison or comparison.id not in searched_comparison_ids or comparison.subject_id != subject_id:
            return {"error": "Find this exact comparison in the current conversation before cancelling it."}
        from . import api as api_module
        try:
            result = await api_module.cancel_comparison(comparison_id, db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "comparison_id": comparison_id, "title": comparison.title, "status": result.get("status"), "cancel_requested": result.get("cancel_requested", False)}

    async def resume_comparison(args):
        comparison_id = args.get("comparison_id")
        comparison = db.get(Comparison, comparison_id) if isinstance(comparison_id, int) and not isinstance(comparison_id, bool) else None
        if not comparison or comparison.id not in searched_comparison_ids or comparison.subject_id != subject_id:
            return {"error": "Find this exact comparison in the current conversation before resuming it."}
        from . import api as api_module
        try:
            result = await api_module.resume_comparison(comparison_id, db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "comparison_id": comparison_id, "title": comparison.title, "status": result.get("status"), "progress": result.get("progress"), "total": result.get("total")}

    def analyze_paper(args):
        paper_id = args.get("paper_id")
        paper = db.get(Paper, paper_id) if isinstance(paper_id, int) and not isinstance(paper_id, bool) else None
        if not paper or paper.id not in searched_paper_ids or paper.subject_id != subject_id:
            return {"error": "Search for this exact paper in the current request before analyzing it."}
        units = []
        for unit in range(1, 6):
            tagged = [question for question in paper.questions if question.confirmed and question.unit == unit]
            units.append({"unit": unit, "confirmed_questions": len(tagged), "marks": sum(question.marks or 0 for question in tagged)})
        return {"paper_id": paper.id, "title": paper.title, "confirmed_questions": sum(question.confirmed for question in paper.questions), "unconfirmed_questions": sum(not question.confirmed for question in paper.questions), "total_questions": len(paper.questions), "known_marks": sum(item["marks"] for item in units), "units": units, "quality_score": None, "predictability_score": None, "note": "Counts describe the imported paper; quality and predictability scores are not calibrated."}

    def analyze_subject_coverage(_args):
        papers = db.scalars(select(Paper).where(Paper.subject_id == subject_id, Paper.status.in_(("reference", "bank")), Paper.archived.is_(False))).all()
        questions = [question for paper in papers for question in paper.questions if question.confirmed]
        topic_nodes = {node["id"]: node for node in subject.tree.get("nodes", []) if node.get("kind") == "topic"}
        units, years = [], {}
        for unit in range(1, 6):
            valid_topics = {topic_id for topic_id in topic_nodes if unit_for_topic(topic_id) == unit}
            unit_questions = [question for question in questions if question.unit == unit]
            covered = {topic_id for question in unit_questions for topic_id in question.topic_ids if topic_id in valid_topics}
            units.append({"unit": unit, "question_count": len(unit_questions), "covered_topics": len(covered), "topic_count": len(valid_topics), "coverage_percent": round(100 * len(covered) / len(valid_topics), 1) if valid_topics else None, "marks": sum(question.marks or 0 for question in unit_questions)})
        for paper in papers:
            if paper.year is None:
                continue
            entry = years.setdefault(paper.year, {"year": paper.year, "units": {unit: 0 for unit in range(1, 6)}})
            for question in paper.questions:
                if question.confirmed and question.unit in range(1, 6):
                    entry["units"][question.unit] += 1
        return {"subject": subject.name, "reference_papers": len(papers), "confirmed_questions": len(questions), "units": units, "years": [years[year] for year in sorted(years)], "quality_score": None, "predictability_score": None}

    def list_jobs(args):
        statement = select(BackgroundJob).order_by(BackgroundJob.id.desc())
        if args.get("all_subjects"):
            if not is_admin:
                return {"error": "Workspace-wide operations are available to administrators only."}
            statement = statement.limit(100)
        else:
            scoped_ids = set(db.scalars(select(Paper.id).where(Paper.subject_id == subject_id)))
            scoped_material_ids = set(db.scalars(select(Material.id).where(Material.subject_id == subject_id)))
            scoped_comparison_ids = set(db.scalars(select(Comparison.id).where(Comparison.subject_id == subject_id)))
            scoped_source_ids = set(db.scalars(select(SyllabusImport.id).where(SyllabusImport.subject_id == subject_id)))
            jobs = list(db.scalars(statement.limit(200)))
            def in_scope(job):
                payload = job.payload or {}
                return (
                    (job.kind in {"tag_paper", "question_generation", "index_paper"} and payload.get("paper_id") in scoped_ids)
                    or (job.kind == "material_enrichment" and payload.get("material_id") in scoped_material_ids)
                    or (job.kind == "comparison" and payload.get("comparison_id") in scoped_comparison_ids)
                    or (job.kind == "comparison_export" and payload.get("comparison_id") in scoped_comparison_ids)
                    or (job.kind == "syllabus_import" and payload.get("source_id") in scoped_source_ids)
                )
            jobs = [job for job in jobs if in_scope(job)]
            statement = None
        if statement is not None:
            jobs = list(db.scalars(statement))
        status, kind = args.get("status"), args.get("kind")
        if status:
            jobs = [job for job in jobs if job.status == status]
        if kind:
            jobs = [job for job in jobs if job.kind == kind]
        jobs = jobs[:50]
        searched_job_ids.update(job.id for job in jobs)
        return {"jobs": [{"id": job.id, "kind": job.kind, "status": job.status, "progress": job.progress, "total": job.total, "attempts": job.attempts, "error": job.error, "created_at": job.created_at.isoformat() if job.created_at else None} for job in jobs]}

    def job_in_subject(job):
        payload = job.payload or {}
        field, model = (
            ("paper_id", Paper) if job.kind in {"tag_paper", "question_generation", "index_paper"} else
            ("material_id", Material) if job.kind == "material_enrichment" else
            ("comparison_id", Comparison) if job.kind in {"comparison", "comparison_export"} else
            ("source_id", SyllabusImport) if job.kind == "syllabus_import" else
            (None, None)
        )
        record = db.get(model, payload.get(field)) if model and isinstance(payload.get(field), int) else None
        return bool(record and record.subject_id == subject_id)

    async def manage_job(args):
        job_id, action = args.get("job_id"), args.get("action")
        job = db.get(BackgroundJob, job_id) if isinstance(job_id, int) and not isinstance(job_id, bool) else None
        if not job or job.id not in searched_job_ids:
            return {"error": "Find this exact job using list_jobs in the current conversation before managing it."}
        if not is_admin and not job_in_subject(job):
            return {"error": "This job is not available in the active subject."}
        if action == "status":
            payload = job.payload or {}
            ready_export = job.kind == "comparison_export" and job.status == "complete" and isinstance(payload.get("artifact"), str) and not payload.get("artifact_expired")
            return {"success": True, "id": job.id, "kind": job.kind, "status": job.status, "progress": job.progress, "total": job.total, "attempts": job.attempts, "error": job.error, "artifact_expired": bool(payload.get("artifact_expired")), "file_url": f"/api/jobs/{job.id}/download" if ready_export else None, "action": "status"}
        if action not in {"retry", "cancel"}:
            return {"error": "Action must be status, retry or cancel."}
        if not is_admin:
            return {"error": "Retrying or cancelling background jobs requires administrator access."}
        from . import api as api_module
        try:
            result = await (api_module.retry_job(job.id, db) if action == "retry" else api_module.cancel_job(job.id, db))
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "id": result["id"], "kind": result.get("kind", job.kind), "status": result["status"], "action": action}

    async def workspace_operations(_args):
        if not is_admin:
            return {"error": "Workspace-wide operations are available to administrators only."}
        from . import api as api_module
        try:
            status = await api_module.operations_status(db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "database": status["database"], "auth_mode": status["auth_mode"], "job_counts": status["job_counts"], "upload_bytes": status["upload_bytes"], "export_bytes": status["export_bytes"]}

    def list_templates(args):
        items = db.scalars(select(Template).where(or_(Template.subject_id.is_(None), Template.subject_id == subject_id)).order_by(Template.kind, Template.name)).all()
        template_id = args.get("template_id")
        if template_id is not None:
            if not isinstance(template_id, int) or isinstance(template_id, bool) or template_id not in searched_template_ids:
                return {"error": "List templates first, then use an exact returned template ID for its definition."}
            items = [item for item in items if item.id == template_id]
        searched_template_ids.update(item.id for item in items[:30])
        return {"templates": [{"id": item.id, "kind": item.kind, "name": item.name, "version": item.version, **({"definition": item.definition} if template_id is not None else {})} for item in items[:30]], "matched_count": len(items), "summary_only": template_id is None}

    def save_template(args):
        name, kind, definition = args.get("name"), args.get("kind"), args.get("definition")
        if not isinstance(name, str) or not name.strip() or len(name) > 200 or kind not in {"paper", "question", "result", "comparison"} or not isinstance(definition, dict):
            return {"error": "Provide a template name, supported kind and object definition."}
        from .api import validate_template
        errors = validate_template(kind, definition)
        if errors:
            return {"error": "Template validation failed: " + "; ".join(errors)}
        template_id = args.get("template_id")
        if template_id is None:
            item = Template(subject_id=subject_id, kind=kind, name=name.strip(), definition=definition)
            db.add(item)
            db.flush()
            action = "template_create"
        else:
            item = db.get(Template, template_id) if isinstance(template_id, int) and not isinstance(template_id, bool) else None
            if not item or item.id not in searched_template_ids or item.subject_id not in (None, subject_id):
                return {"error": "Search for this exact subject template in the current request before updating it."}
            if item.subject_id is None:
                return {"error": "Shared default templates cannot be edited from a subject chat."}
            item.kind, item.name, item.definition = kind, name.strip(), definition
            item.version += 1
            action = "template_update"
        db.add(AuditEvent(action=action, details={"template_id": item.id, "kind": kind, "version": item.version, "via": "chat"}))
        db.commit()
        return {"success": True, "template_id": item.id, "kind": item.kind, "name": item.name, "version": item.version}

    async def map_material(args):
        material_id = args.get("material_id")
        material = db.get(Material, material_id) if isinstance(material_id, int) else None
        if not material or material.id not in searched_material_ids or material.subject_id != subject_id:
            return {"error": "Search for the exact material in this conversation before mapping it."}
        if material.enrichment.get("status") in ("queued", "running"):
            return {"error": "This material already has a mapping job in progress."}
        from .api import _prepare_material_mapping
        try:
            result = await _prepare_material_mapping(db, material)
        except Exception as exc:
            db.rollback()
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, **result}

    def apply_material_mapping(args):
        material_id = args.get("material_id")
        material = db.get(Material, material_id) if isinstance(material_id, int) else None
        if not material or material.id not in searched_material_ids or material.subject_id != subject_id:
            return {"error": "List the exact material before applying its mapping."}
        if (material.enrichment or {}).get("status") != "review_ready":
            return {"error": "The material has no prepared mapping yet. Map it first."}
        from .api import _apply_material_mapping
        try:
            result = _apply_material_mapping(db, material, subject)
            db.commit()
        except Exception as exc:
            db.rollback()
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, **result}

    def start_comparison(args):
        if not comparison_ready:
            return {"error": "Configure local judge and helper model roles before comparing."}
        targets, references = args.get("target_ids"), args.get("reference_ids")
        if not isinstance(targets, list) or not isinstance(references, list) or not targets or not references or any(not isinstance(item, int) or isinstance(item, bool) for item in targets + references):
            return {"error": "Provide non-empty target_ids and reference_ids from the question search results."}
        targets, references = list(dict.fromkeys(targets)), list(dict.fromkeys(references))
        questions = {q.id: q for q in db.scalars(select(Question).join(Paper).where(Paper.subject_id == subject_id))}
        missing = [item for item in targets + references if item not in questions]
        if missing:
            return {"error": f"Question IDs are not in this subject: {missing}"}
        if any(item not in searched_question_ids for item in targets + references):
            return {"error": "Search for each target and reference question in this chat request before comparing."}
        invalid = [item for item in targets + references if questions[item].paper.archived or not questions[item].confirmed or not questions[item].unit]
        if invalid:
            return {"error": f"Questions need confirmed unit and topic tags before comparison: {sorted(set(invalid))}"}
        title = str(args.get("title") or "Chat comparison")[:250]
        pair_total = sum(1 for a in targets for b in references if a != b and questions[a].unit == questions[b].unit)
        if not pair_total:
            return {"error": "The selected target and reference sets contain no same-unit question pairs."}
        all_distinct_pairs = sum(1 for a in targets for b in references if a != b)
        skipped_cross_unit = all_distinct_pairs - pair_total
        comparison = Comparison(subject_id=subject_id, title=title, target_ids=targets, reference_ids=references, status="queued", total=pair_total)
        db.add(comparison)
        db.flush()
        job = enqueue_job(db, "comparison", {"comparison_id": comparison.id}, total=pair_total)
        db.add(AuditEvent(action="comparison_create", details={"comparison_id": comparison.id, "pairs": job.total, "via": "chat"}))
        db.commit()
        return {"success": True, "comparison_id": comparison.id, "job_id": job.id, "title": title, "pairs": job.total, "skipped_cross_unit_pairs": skipped_cross_unit, "status": "queued"}

    def generate_questions(args):
        if not model_configured:
            return {"error": "Configure a local JUDGE_MODEL_NAME before generating questions."}
        unit, topic_ids, marks = args.get("unit"), args.get("topic_ids"), args.get("marks")
        count, difficulty = args.get("count"), args.get("difficulty")
        reference_ids, title = args.get("reference_ids"), str(args.get("title", "Chat generated draft")).strip()[:250]
        if not title:
            return {"error": "Provide a non-empty draft title."}
        if not isinstance(unit, int) or isinstance(unit, bool) or unit not in range(1, 6) or not isinstance(marks, int) or isinstance(marks, bool) or marks < 1 or not isinstance(count, int) or isinstance(count, bool) or count not in range(1, 11):
            return {"error": "Generation needs a valid unit, positive marks and a question count from 1 to 10."}
        if difficulty not in {"introductory", "intermediate", "advanced"} or not isinstance(topic_ids, list) or not topic_ids or any(not isinstance(topic_id, str) for topic_id in topic_ids):
            return {"error": "Provide a valid difficulty and exact syllabus topic IDs."}
        topics = {node["id"]: node for node in subject.tree.get("nodes", []) if node.get("kind") == "topic"}
        if any(topic_id not in searched_topic_ids for topic_id in topic_ids):
            return {"error": "Look up each exact syllabus topic in this conversation before generating questions."}
        if any(topic_id not in topics or unit_for_topic(topic_id) != unit for topic_id in topic_ids):
            return {"error": "Every selected syllabus topic must belong to the requested unit."}
        if not isinstance(reference_ids, list) or not reference_ids or any(not isinstance(item, int) or isinstance(item, bool) for item in reference_ids):
            return {"error": "Select exact confirmed reference question IDs using the question search tool."}
        if any(question_id not in searched_question_ids for question_id in reference_ids):
            return {"error": "Search for each reference question in this conversation before using it for generation."}
        references = {q.id: q for q in db.scalars(select(Question).where(Question.id.in_(reference_ids)))}
        if len(references) != len(set(reference_ids)) or any(q.paper.subject_id != subject_id or q.paper.archived or not q.confirmed for q in references.values()) or not any(q.unit == unit for q in references.values()):
            return {"error": "References must be unique, confirmed questions in this subject and include one from the selected unit."}
        slot = {"section": "Generated questions", "unit": unit, "topic_ids": list(dict.fromkeys(topic_ids)), "marks": marks, "count": count, "difficulty": difficulty, "constraints": str(args.get("constraints", ""))[:1200]}
        paper = Paper(subject_id=subject_id, title=title, status="draft", generated=True, generation={"status": "queued", "reference_ids": reference_ids, "slots": [slot]})
        db.add(paper)
        db.flush()
        job = BackgroundJob(kind="question_generation", payload={"paper_id": paper.id, "reference_ids": reference_ids, "slots": [slot]}, total=count)
        db.add(job)
        db.add(AuditEvent(action="question_generation_start", details={"paper_id": paper.id, "via": "chat", "reference_ids": reference_ids, "slot": slot}))
        db.commit()
        return {"success": True, "paper_id": paper.id, "title": title, "job_id": job.id, "candidate_count": count, "status": "queued"}

    async def suggest_replacements(args):
        question_id, difficulty = args.get("question_id"), args.get("difficulty")
        source = db.get(Question, question_id) if isinstance(question_id, int) and not isinstance(question_id, bool) else None
        if not source or source.id not in searched_question_ids or source.paper.subject_id != subject_id or source.paper.archived:
            return {"error": "Search for the exact active source question before requesting replacements."}
        if not comparison_ready:
            return {"error": "Install the configured local judge and helper before generating screened replacements."}
        if not source.confirmed or source.unit not in range(1, 6) or not source.topic_ids or not isinstance(source.marks, int) or not 1 <= source.marks <= 100:
            return {"error": "The source question needs confirmed syllabus topics, a unit and 1–100 marks before replacement drafting."}
        if difficulty not in {"introductory", "intermediate", "advanced"}:
            return {"error": "Choose the desired replacement difficulty: introductory, intermediate or advanced. The source question's difficulty is not measured."}
        count = args.get("count", 3)
        if not isinstance(count, int) or isinstance(count, bool) or not 1 <= count <= 5:
            return {"error": "Request between one and five replacement candidates."}
        topic_ids = args.get("topic_ids", source.topic_ids)
        if not isinstance(topic_ids, list) or not 1 <= len(topic_ids) <= 3 or any(not isinstance(item, str) for item in topic_ids):
            return {"error": "Choose one to three exact syllabus topics for these replacement candidates."}
        valid_topics = {node["id"] for node in subject.tree.get("nodes", []) if node.get("kind") == "topic"}
        if "topic_ids" in args and any(item not in searched_topic_ids for item in topic_ids):
            return {"error": "Look up each requested replacement topic before using it."}
        if len(set(topic_ids)) != len(topic_ids) or any(item not in valid_topics or unit_for_topic(item) != source.unit for item in topic_ids):
            return {"error": "Replacement topics must be distinct active topics in the source question's unit."}
        supplied_refs = args.get("reference_ids")
        if supplied_refs is not None:
            if not isinstance(supplied_refs, list) or not supplied_refs or any(not isinstance(item, int) or isinstance(item, bool) or item not in searched_question_ids for item in supplied_refs):
                return {"error": "Search for each exact reference question before selecting a custom screening scope."}
            reference_ids = list(dict.fromkeys(supplied_refs))
            reference_scope = "selected exact questions"
        else:
            reference_ids = [item.id for item in db.scalars(select(Question).join(Paper).where(Paper.subject_id == subject_id, Paper.status.in_(("reference", "bank")), Paper.archived.is_(False), Question.confirmed.is_(True), Question.unit == source.unit, Question.id != source.id).order_by(Paper.year.desc(), Paper.id.desc(), Question.id))]
            reference_scope = "all active confirmed reference/bank questions in the same unit"
        if not reference_ids or len(reference_ids) > 120:
            return {"error": "Replacement screening needs 1–120 confirmed same-unit reference questions. Search and select a bounded exact scope or add reference papers."}
        references = {item.id: item for item in db.scalars(select(Question).where(Question.id.in_(reference_ids)))}
        if len(references) != len(reference_ids) or any(item.paper.subject_id != subject_id or item.paper.archived or not item.confirmed or item.unit != source.unit or item.id == source.id for item in references.values()):
            return {"error": "Every selected screening reference must be a confirmed active question in the same subject and unit, excluding the source question."}
        constraints = args.get("constraints", "")
        if not isinstance(constraints, str) or len(constraints) > 1200:
            return {"error": "Replacement constraints must be at most 1200 characters."}
        from . import api as api_module
        title = f"Replacements for {source.paper.title} · Q{source.number}"[:250]
        try:
            created = await api_module.start_generation(api_module.GenerationInput(subject_id=subject_id, title=title, reference_ids=reference_ids, unit=source.unit, topic_ids=topic_ids, marks=source.marks, count=count, difficulty=difficulty, constraints=constraints), db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        draft = db.get(Paper, created["paper"]["id"])
        draft.generation = {**(draft.generation or {}), "replacement_for_question_id": source.id, "source_revision": source.revision, "source_paper_id": source.paper_id, "requested_difficulty": difficulty, "reference_scope": reference_scope}
        db.add(AuditEvent(action="replacement_suggestions_start", details={"source_question_id": source.id, "draft_paper_id": draft.id, "source_revision": source.revision, "reference_count": len(reference_ids), "via": "chat"}))
        db.commit()
        searched_paper_ids.add(draft.id)
        return {"success": True, "paper_id": draft.id, "title": draft.title, "job_id": created["job_id"], "source_question_id": source.id, "source_number": source.number, "candidate_count": count, "requested_difficulty": difficulty, "reference_count": len(reference_ids), "reference_scope": reference_scope, "status": "queued"}

    async def replacement_analysis(args):
        paper_id = args.get("paper_id")
        if not isinstance(paper_id, int) or isinstance(paper_id, bool) or paper_id not in searched_paper_ids:
            return {"error": "Find the exact replacement draft paper before inspecting candidates."}
        from . import api as api_module
        try:
            report = await api_module.replacement_analysis(paper_id, db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        candidates = [{"id": item["id"], "number": item["number"], "text": item["text"][:500], "topic_ids": item["topic_ids"], "coverage_after": item["coverage_after"], "difficulty": item["difficulty"], "screening": item["screening"]} for item in report["candidates"]]
        searched_question_ids.update(item["id"] for item in candidates)
        return {"success": True, "paper_id": paper_id, "source_question": {key: report["source_question"][key] for key in ("id", "paper_title", "number", "unit", "marks", "topic_ids", "revision")}, "coverage_before": report["coverage_before"], "source_changed": report["source_changed"], "candidates": candidates, "generation_status": report["generation_status"], "note": report["note"]}

    async def apply_replacement(args):
        source_id, candidate_id = args.get("source_question_id"), args.get("candidate_id")
        if not isinstance(source_id, int) or isinstance(source_id, bool) or source_id not in searched_question_ids or not isinstance(candidate_id, int) or isinstance(candidate_id, bool) or candidate_id not in searched_question_ids:
            return {"error": "Look up both the exact source question and replacement candidate in this conversation before applying it."}
        source = db.get(Question, source_id)
        candidate = db.get(Question, candidate_id)
        if not source or not candidate or source.paper.subject_id != subject_id or candidate.paper.subject_id != subject_id:
            return {"error": "Both questions must be available in the active subject."}
        from . import api as api_module
        try:
            applied = await api_module.apply_replacement(source_id, api_module.ApplyReplacementInput(candidate_id=candidate_id), db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "source_question_id": source_id, "candidate_id": candidate_id, "paper_id": source.paper_id, "new_revision": applied["source_question"]["revision"], "screening_labels": applied["screening_labels"]}

    async def semantic_search_questions(args):
        query = args.get("query")
        unit = args.get("unit")
        if not isinstance(query, str) or not query.strip() or len(query) > 4000 or unit is not None and (isinstance(unit, bool) or not isinstance(unit, int) or unit not in range(1, 6)):
            return {"error": "Provide a query of at most 4000 characters and an optional unit from 1 through 5"}
        try:
            matches = await semantic_search(db, subject_id, query, unit=unit, limit=30, bank_only=bool(args.get("bank_only", False)))
        except ModelUnavailable as exc:
            return {"error": str(exc)}
        questions = []
        for match in matches[:12]:
            q = match["question"]
            questions.append({"id": q.id, "paper_id": q.paper_id, "number": q.number, "text": q.text[:450], "unit": q.unit, "topic_ids": q.topic_ids[:6], "confirmed": q.confirmed, "similarity": match["similarity"], "matched_part": match["matched_part"]})
        # Seed the same exact-ID guard as ordinary question search.
        searched_question_ids.update(item["id"] for item in questions)
        return {"questions": questions, "note": "Current indexed questions only; similarity does not decide A/B/C."}

    def prepare_report(args):
        comparison_id, fmt = args.get("comparison_id"), args.get("format")
        comparison = db.get(Comparison, comparison_id) if isinstance(comparison_id, int) else None
        if not comparison or comparison.id not in searched_comparison_ids or comparison.subject_id != subject_id or fmt not in ("md", "txt", "pdf", "xlsx"):
            return {"error": "Comparison or report format is invalid for this subject."}
        return {"success": True, "comparison_id": comparison.id, "format": fmt, "file_url": f"/api/comparisons/{comparison.id}/export?format={fmt}"}

    async def resolve_selected_result(args):
        label, reason = args.get("label"), args.get("reason")
        result_id = args.get("result_id", selected_result_id)
        if not isinstance(result_id, int) or isinstance(result_id, bool) or result_id not in searched_result_ids:
            return {"error": "List the exact comparison result or select it in the Workspace before resolving it."}
        if label not in {"A", "B", "C"} or not isinstance(reason, str) or not reason.strip() or len(reason) > 2000:
            return {"error": "A case resolution needs an A/B/C label and a reason of 1–2000 characters."}
        result = db.get(PairResult, result_id)
        comparison = db.get(Comparison, result.comparison_id) if result else None
        if not result or not comparison or comparison.subject_id != subject_id:
            return {"error": "The selected result is no longer available in this subject."}
        from . import api as api_module
        try:
            resolved = await api_module.resolve_result(result_id, api_module.ResultResolutionInput(label=label, reason=reason), db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "result_id": result_id, "label": resolved["label"], "reason": resolved["reason"], "propagation": "none"}

    async def note_on_selected_result(args):
        result_id = args.get("result_id", selected_result_id)
        if not isinstance(result_id, int) or isinstance(result_id, bool) or result_id not in searched_result_ids:
            return {"error": "List the exact comparison result or select it in the Workspace before adding a case note."}
        comment, suggested_label = args.get("comment"), args.get("suggested_label")
        if not isinstance(comment, str) or not comment.strip() or len(comment) > 2000:
            return {"error": "Feedback must contain 1–2000 characters."}
        if suggested_label not in (None, "A", "B", "C", "review"):
            return {"error": "Suggested label must be A, B, C, review or omitted."}
        result = db.get(PairResult, result_id)
        comparison = db.get(Comparison, result.comparison_id) if result else None
        if not result or not comparison or comparison.subject_id != subject_id:
            return {"error": "The selected result is no longer available in this subject."}
        from . import api as api_module
        try:
            recorded = await api_module.record_result_feedback(result_id, api_module.ResultFeedbackInput(comment=comment, suggested_label=suggested_label), db)
        except Exception as exc:
            return {"error": str(getattr(exc, "detail", exc))}
        return {"success": True, "result_id": result_id, "feedback_id": recorded["feedback_id"], "suggested_label": suggested_label}

    return {
        "create_paper": create_paper, "create_question": create_question, "search_papers": search_papers,
        "set_paper_status": set_paper_status, "update_paper": update_paper, "set_paper_archived": set_paper_archived,
        "search_questions": search_questions, "update_question": update_question, "delete_record": delete_record,
        "lookup_syllabus": lookup_syllabus, "link_syllabus_topics": link_syllabus_topics, "update_syllabus_topic": update_syllabus_topic,
        "create_syllabus_topic": create_syllabus_topic, "delete_syllabus_topic": delete_syllabus_topic,
        "list_materials": list_materials, "list_comparisons": list_comparisons, "list_comparison_results": list_comparison_results, "inspect_comparison_result": inspect_comparison_result, "cancel_comparison": cancel_comparison,
        "resume_comparison": resume_comparison, "rerun_comparison": rerun_comparison,
        "analyze_paper": analyze_paper, "analyze_subject_coverage": analyze_subject_coverage,
        "list_jobs": list_jobs, "manage_job": manage_job, "workspace_operations": workspace_operations,
        "list_templates": list_templates, "save_template": save_template, "map_material": map_material, "apply_material_mapping": apply_material_mapping,
        "start_comparison": start_comparison, "prepare_report": prepare_report,
        "resolve_selected_result": resolve_selected_result, "note_on_selected_result": note_on_selected_result,
        "generate_questions": generate_questions,
        "suggest_replacements": suggest_replacements, "replacement_analysis": replacement_analysis, "apply_replacement": apply_replacement,
        "semantic_search_questions": semantic_search_questions,
    }
