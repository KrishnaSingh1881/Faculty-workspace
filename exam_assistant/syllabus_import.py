"""Source-grounded syllabus-to-tree conversion for local subject onboarding."""

import json
import re

from .engine import MODEL
from .engine import model_json
from .knowledge import validate_tree


MAX_SYLLABUS_CHARS = 120_000
PROMPT_VERSION = "syllabus-tree-v1"

TREE_SYSTEM = """Convert only the supplied syllabus text into the app's five-unit tree JSON.
Do not use outside knowledge to add topics, course details or expected answers. Preserve official
wording and hierarchy. Return one JSON object with key `tree`, whose value has `schema_version`,
`course` (code, title, year, semester, course_type, unit_count), `nodes`, and `review_questions`.
Create a root course node, exactly five unit nodes with IDs `<course-code>/u1` through `/u5`, and
topic nodes beneath the correct unit. Keep descriptions under 45 words and use them only when
supported by the syllabus. Every unit and topic must include `source_text` copied verbatim from the
source and `source_pages` with one or more supplied page numbers. Every topic ID must be unique and
use a stable lowercase slug below its unit. If hierarchy or wording is unclear, preserve the source
text and add a concise `review_questions` item; do not guess. Include no enrichment, textbooks,
synonyms or assessment guidance unless the source explicitly provides them."""


def _normal(text: str) -> str:
    return " ".join(re.findall(r"[\w]+", text.casefold()))


def _contains_source(source: str, quote: str) -> bool:
    source_tokens, quote_tokens = _normal(source).split(), _normal(quote).split()
    width = len(quote_tokens)
    return bool(width and any(source_tokens[i:i + width] == quote_tokens for i in range(len(source_tokens) - width + 1)))


def validate_source_grounding(tree: dict, text: str) -> None:
    pages = text.split("\f")
    course = tree.get("course", {})
    code, title = course.get("code"), course.get("title")
    if not isinstance(code, str) or not isinstance(title, str) or not code.strip() or not title.strip():
        raise ValueError("Syllabus needs a course code and title")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", code):
        raise ValueError("Course code contains characters that cannot form stable topic IDs")
    normalized_text = _normal(text)
    if _normal(code) not in normalized_text or _normal(title) not in normalized_text:
        raise ValueError("Course code or title was not found in the supplied syllabus text")
    nodes = tree.get("nodes", [])
    if any(node.get("kind") not in {"course", "unit", "topic"} for node in nodes):
        raise ValueError("Syllabus import supports course, unit and topic nodes")
    root = next((node for node in nodes if node.get("kind") == "course"), None)
    if not root or root.get("id") != code or root.get("parent") is not None:
        raise ValueError("Tree root must use the official course code")
    units = {node.get("id"): node for node in nodes if node.get("kind") == "unit"}
    expected_units = {f"{code}/u{number}" for number in range(1, 6)}
    if set(units) != expected_units or any(node.get("parent") != code for node in units.values()):
        raise ValueError("The tree must contain the five numbered units directly under the course")
    topics_per_unit = {f"{code}/u{n}": 0 for n in range(1, 6)}
    for node in nodes:
        kind = node.get("kind")
        if kind == "topic":
            unit_id = next((candidate for candidate in topics_per_unit if node.get("id", "").startswith(candidate + "/")), None)
            if unit_id is None:
                raise ValueError(f"Topic {node.get('id')} is not inside one of the five units")
            topics_per_unit[unit_id] += 1
        if kind not in ("unit", "topic"):
            continue
        quote = node.get("source_text")
        cited_pages = node.get("source_pages")
        if not isinstance(quote, str) or len(quote.strip()) < 5:
            raise ValueError(f"{kind.title()} {node.get('id')} needs a verbatim source excerpt")
        if not isinstance(cited_pages, list) or not cited_pages or any(not isinstance(page, int) or page < 1 or page > len(pages) for page in cited_pages):
            raise ValueError(f"{kind.title()} {node.get('id')} needs valid source page citations")
        if not any(_contains_source(pages[page - 1], quote) for page in cited_pages):
            raise ValueError(f"Source excerpt for {node.get('id')} does not match its cited page")
    empty_units = [unit for unit, count in topics_per_unit.items() if count == 0]
    if empty_units:
        raise ValueError("Every one of the five units must contain at least one syllabus topic")


async def build_tree(text: str, filename: str) -> dict:
    if not MODEL:
        raise RuntimeError("Configure a local JUDGE_MODEL_NAME before importing a syllabus")
    if len(text) > MAX_SYLLABUS_CHARS:
        raise ValueError(f"Syllabus text exceeds the {MAX_SYLLABUS_CHARS:,}-character onboarding limit")
    pages = [{"page": number, "text": page} for number, page in enumerate(text.split("\f"), 1) if page.strip()]
    result = await model_json([
        {"role": "system", "content": TREE_SYSTEM},
        {"role": "user", "content": json.dumps({"filename": filename, "page_count": len(text.split("\f")), "pages": pages}, ensure_ascii=False)},
    ])
    tree = result.get("tree")
    if not isinstance(tree, dict):
        raise ValueError("Local model did not return a syllabus tree")
    tree["schema_version"] = tree.get("schema_version", "1.0-source-grounded")
    errors = validate_tree(tree)
    if errors:
        raise ValueError("Generated syllabus tree failed structural validation: " + "; ".join(errors))
    validate_source_grounding(tree, text)
    return tree
