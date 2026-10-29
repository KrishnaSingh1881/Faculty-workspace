"""Tool-using local helper and judge roles for question-pair comparison."""

import json
import logging
import time
from inspect import isawaitable
from copy import deepcopy
from typing import Callable

from .model_runtime import ModelUnavailable, chat_json, chat_json_in_session, comparison_context_tokens
from .activity import publish

logger = logging.getLogger(__name__)


HELPER_SYSTEM = """You are the independent comparison helper. You must not decide or emit A/B/C/review.
Inspect both complete original questions and the cached atomic requirement records. Check whether each
record captures the actual ask, including subparts and OR/choose-any structure. If a requirement is
missing, malformed or ambiguous, explain it in concerns and do not silently repair the cached record.
Use the supplied tools: compare each pair you align, build a signal matrix for your complete proposed
mapping using both full requirement lists, and check the proposed compound mapping with part/choice
structure. Look up syllabus evidence when useful. For a possibly narrower ask or scenario transformation,
use the corresponding diagnostic tool and report its limits. Tool results are diagnostic signals, not
verdicts. Return one JSON object with alignments (objects with a_id, b_id, relation
equivalent|overlap|distinct, shared, differences), compound_mapping (objects with a_id, b_id), and
concerns (array of unresolved or possibly missed requirements). Do not assign a final label. Do not
infer syllabus facts from model memory. Requirements and source IDs are supplied as evidence."""

JUDGE_SYSTEM = """You are the final question-comparison judge. Decide from assessed requirements, never from
shared vocabulary, topic adjacency, marks, or broad topic tags alone. A means equivalent concept,
task, scope and expected depth in both directions, with every compound ask aligned. B means material
overlap plus a different or additional assessed requirement. C means the supplied question evidence
supports no meaningful overlap. Use review if extraction, evidence, helper findings or your own tool
checks conflict or are insufficient. You must inspect the helper's findings, call compare_requirements
for every helper-mapped pair, build a signal matrix over the exact helper requirement lists and mapping,
and call check_compound_alignment with the helper's complete requirement lists, part structure, choice
rules and mapping. Independently look for omitted asks in the original text. For B, identify every
unmatched requirement by its supplied ID in `differences`; do not hide additional asks in general prose.
Return JSON with label, reason, evidence_ids, shared_requirements, differences, missed_requirements,
choice_logic_equivalent (boolean), confidence (0 to 1). Cite only evidence IDs supplied in this request. Cite both q1 and q2. Do not
claim the checker has proven semantic truth; state concrete question differences."""


def _tool_definitions(registry: dict[str, Callable]) -> list[dict]:
    from .comparison_tools import TOOL_SCHEMAS

    return [item for item in TOOL_SCHEMAS if item["function"]["name"] in registry]


def _bound_requirement_tools(registry, profile_a, profile_b):
    """Models reference source IDs; code supplies the immutable cached records to tools."""
    left = {item["id"]: item for item in profile_a["requirements"]}
    right = {item["id"]: item for item in profile_b["requirements"]}
    atomic = {"compare_requirements", "evaluate_subsumption", "check_transformation"}
    schemas = deepcopy(_tool_definitions(registry))
    for tool in schemas:
        function = tool["function"]
        if function["name"] in atomic:
            function["parameters"] = {"type": "object", "required": ["a_id", "b_id"], "properties": {
                "a_id": {"type": "string", "enum": list(left)}, "b_id": {"type": "string", "enum": list(right)},
            }}
        elif function["name"] in {"check_compound_alignment", "build_signal_matrix"}:
            function["parameters"] = {"type": "object", "required": ["mapping"], "properties": {
                "mapping": {"type": "array", "items": {"type": "object", "required": ["a_id", "b_id"], "properties": {
                    "a_id": {"type": "string", "enum": list(left)}, "b_id": {"type": "string", "enum": list(right)},
                }}},
            }}
            function["description"] += " Submit mapping IDs only; the server supplies both complete requirement lists and their original part/choice structure."

    def prepare(name, arguments):
        if not isinstance(arguments, dict):
            raise ValueError("Tool arguments must be an object")
        if name in atomic:
            if arguments.get("a_id") not in left or arguments.get("b_id") not in right:
                raise ValueError("Use one supplied requirement ID from each question")
            return {"requirement_a": left[arguments["a_id"]], "requirement_b": right[arguments["b_id"]]}
        if name in {"check_compound_alignment", "build_signal_matrix"}:
            args = {"requirements_a": profile_a["requirements"], "requirements_b": profile_b["requirements"], "mapping": arguments.get("mapping")}
            if name == "check_compound_alignment":
                args.update(parts_a=profile_a["parts"], parts_b=profile_b["parts"], choice_rule_a=profile_a.get("choice_rule"), choice_rule_b=profile_b.get("choice_rule"))
            return args
        return arguments

    return schemas, prepare


async def run_tool_agent(
    *,
    model: str,
    system: str,
    payload: dict,
    registry: dict[str, Callable],
    require_tool_call: bool = True,
    max_calls: int = 12,
    tool_schemas: list[dict] | None = None,
    agent: str = "agent",
    on_event: Callable[[dict], None] | None = None,
    prepare_arguments: Callable | None = None,
    session_per_request: bool = False,
    required_tools: set[str] | None = None,
    num_ctx: int | None = None,
) -> tuple[dict, list[dict], list[str]]:
    """Run a bounded Ollama function-calling loop; tool outputs are captured for the trace."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False, default=str)},
    ]
    tools = tool_schemas if tool_schemas is not None else _tool_definitions(registry)
    trace: list[dict] = []
    used: list[str] = []
    succeeded_tools: set[str] = set()
    retry_without_tools = False
    repairing_json = False
    required_tools = set(required_tools or ())

    def emit(event: str, payload: dict | None = None):
        record = {"agent": agent, "event": event, "payload": payload or {}}
        publish(record)
        if on_event:
            try:
                on_event(record)
            except Exception:
                logger.exception("Could not persist comparison activity")

    emit("started")
    for _ in range(max_calls + 2):
        emit("request", {"tool_calls": len(used), "repairing_json": repairing_json})
        request_model = chat_json if session_per_request else chat_json_in_session
        response = await request_model(
            model, messages, tools=None if repairing_json else tools, keep_alive="5m",
            think=False if repairing_json else None,
            num_ctx=num_ctx,
            on_event=lambda event: emit(event["event"], event["payload"]),
        )
        message = response["message"]
        messages.append(message)
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            missing_tools = sorted(required_tools - succeeded_tools)
            if missing_tools:
                messages.append({
                    "role": "user",
                    "content": "Required diagnostics are still missing. Call each of these tools before returning your final JSON: "
                    + ", ".join(missing_tools)
                    + ". Use the exact supplied requirement IDs and complete mapping.",
                })
                continue
            if require_tool_call and not used and not retry_without_tools:
                messages.append({"role": "user", "content": "Before returning JSON, call the required comparison tools and use their results."})
                retry_without_tools = True
                continue
            content = message.get("content", "")
            try:
                result = json.loads(content)
            except (TypeError, ValueError):
                if repairing_json:
                    raise ModelUnavailable(f"{model} did not return valid JSON after one repair attempt")
                messages.append({
                    "role": "user",
                    "content": "Return the required final result as one valid JSON object now. Do not call more tools. Use only the tool results already in this conversation.",
                })
                retry_without_tools = True
                repairing_json = True
                emit("repair", {"reason": "Final response was not valid JSON"})
                continue
            if not isinstance(result, dict):
                raise ModelUnavailable(f"{model} returned JSON that is not an object")
            emit("finished", {"tool_calls": len(used), "summary": result})
            return result, trace, used
        if len(used) + len(tool_calls) > max_calls:
            raise ModelUnavailable(f"{model} exceeded the comparison tool-call limit")
        for call in tool_calls:
            function = call.get("function") or {}
            name = function.get("name")
            tool_name = name if isinstance(name, str) else "unknown"
            call_id = f"tool_{len(trace) + 1}"
            arguments = function.get("arguments", {})
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except ValueError:
                    arguments = None
            if tool_name not in registry:
                result = {"error": f"Unknown tool: {name}"}
            else:
                tool_started = time.monotonic()
                emit("tool_started", {"name": tool_name, "arguments": arguments, "call_id": call_id})
                try:
                    if prepare_arguments:
                        arguments = prepare_arguments(tool_name, arguments)
                    result = registry[tool_name](arguments)
                    if isawaitable(result):
                        result = await result
                    if not isinstance(result, dict):
                        result = {"result": result}
                except (TypeError, ValueError, KeyError) as exc:
                    result = {"error": str(exc)}
            used.append(tool_name)
            if isinstance(result, dict) and "error" not in result:
                succeeded_tools.add(tool_name)
            trace.append({"id": f"tool_{len(trace) + 1}", "name": tool_name, "arguments": arguments, "result": result})
            emit("tool", {"name": tool_name, "arguments": arguments, "result": result, "call_id": call_id,
                          "duration_ms": round((time.monotonic() - tool_started) * 1000) if tool_name in registry else 0})
            messages.append({"role": "tool", "tool_name": tool_name, "content": json.dumps(result, ensure_ascii=False, default=str)})
    raise ModelUnavailable(f"{model} exceeded the bounded tool-use loop")


async def run_helper(model: str, evidence: list[dict], q1: str, q2: str, profile_a: dict, profile_b: dict, registry: dict[str, Callable], on_event: Callable[[dict], None] | None = None):
    schemas, prepare = _bound_requirement_tools(registry, profile_a, profile_b)
    return await run_tool_agent(
        model=model,
        system=HELPER_SYSTEM,
        payload={
            "evidence": evidence,
            "questions": {"q1": q1, "q2": q2},
            "requirements_a": profile_a["requirements"],
            "requirements_b": profile_b["requirements"],
            "parts_a": profile_a["parts"],
            "parts_b": profile_b["parts"],
            "choice_rule_a": profile_a.get("choice_rule"),
            "choice_rule_b": profile_b.get("choice_rule"),
        },
        registry=registry,
        max_calls=24,
        agent="helper",
        on_event=on_event,
        tool_schemas=schemas,
        prepare_arguments=prepare,
        required_tools={"compare_requirements", "check_compound_alignment", "build_signal_matrix"},
        num_ctx=comparison_context_tokens(),
    )


async def run_judge(model: str, payload: dict, registry: dict[str, Callable], on_event: Callable[[dict], None] | None = None):
    schemas, prepare = _bound_requirement_tools(registry,
        {"requirements": payload["requirements_a"], "parts": payload["parts_a"], "choice_rule": payload.get("choice_rule_a")},
        {"requirements": payload["requirements_b"], "parts": payload["parts_b"], "choice_rule": payload.get("choice_rule_b")})
    return await run_tool_agent(
        model=model,
        system=(JUDGE_SYSTEM if payload.get("helper_analysis") else JUDGE_SYSTEM.replace(
            "You must inspect the helper's findings, call compare_requirements\nfor every helper-mapped pair, build a signal matrix over the exact helper requirement lists and mapping,\nand call check_compound_alignment with the helper's complete requirement lists, part structure, choice\nrules and mapping.",
            "Create your own complete requirement mapping, call compare_requirements for every mapped pair, build a signal matrix, and check compound alignment. Include alignments (a_id, b_id, relation equivalent|overlap|distinct, shared, differences), compound_mapping (a_id, b_id), and concerns in your JSON. If you need independent assistance, set needs_helper to true."
        )),
        payload=payload,
        registry=registry,
        max_calls=24,
        agent="judge",
        on_event=on_event,
        tool_schemas=schemas,
        prepare_arguments=prepare,
        required_tools={"compare_requirements", "check_compound_alignment", "build_signal_matrix"},
        num_ctx=comparison_context_tokens(),
    )
