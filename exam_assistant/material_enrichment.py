"""Fast, approximate mapping of extracted material to syllabus topics."""

import re

PROMPT_VERSION = "material-keywords-v1"
MAX_CHUNKS = 500
STOP = {"a", "an", "and", "are", "as", "at", "by", "for", "from", "in", "into", "is", "it", "of", "on", "or", "the", "to", "using", "with", "iot", "internet", "things", "overview", "introduction", "system", "systems"}


def chunks_for(text: str) -> list[dict]:
    chunks = [{"page": page, "part": 1, "text": content.strip()} for page, content in enumerate(text.split("\f"), 1) if content.strip()]
    if len(chunks) > MAX_CHUNKS:
        raise ValueError(f"Material has too many sections ({len(chunks)}; maximum {MAX_CHUNKS})")
    if not chunks:
        raise ValueError("No readable sections were found in this material")
    return chunks


def _words(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", value.casefold())


def _quote(text: str, matched: set[str]) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return text[:250].strip()
    best = max(lines, key=lambda line: (len(set(_words(line)) & matched), -len(line)))
    return best[:300]


async def map_material(text: str, topics: list[dict], filename: str, progress=None, *, section_cache=None, checkpoint=None, activity=None) -> dict:
    """Match topic terms across the whole document without model calls."""
    chunks = chunks_for(text)
    page_words = [set(_words(chunk["text"])) for chunk in chunks]
    proposals = {}
    mapped_pages = set()
    for topic in topics:
        label = topic["label"]
        terms = list(dict.fromkeys(word for word in _words(label) if len(word) > 2 and word not in STOP))
        if not terms:
            continue
        matches = []
        for chunk, words in zip(chunks, page_words):
            common = set(terms) & words
            if not common:
                continue
            # ponytail: lexical matching can confuse related topics; add semantic reranking only if actual usage needs it.
            required = 1 if len(terms) == 1 else max(2, (len(terms) + 1) // 2)
            if len(common) < required:
                continue
            phrase = " ".join(terms) in " ".join(_words(chunk["text"]))
            score = len(common) / len(terms) + (0.5 if phrase else 0)
            matches.append((score, chunk, common))
        if not matches:
            continue
        matches.sort(key=lambda item: (-item[0], item[1]["page"]))
        citations = [{"file": filename, "page": chunk["page"], "section": 1, "quote": _quote(chunk["text"], common)} for _, chunk, common in matches[:3]]
        mapped_pages.update(item[1]["page"] for item in matches)
        proposals[topic["id"]] = {
            "topic_id": topic["id"], "summaries": [f"Material covers {label} (pages {', '.join(str(item['page']) for item in citations)})."],
            "context_words": [], "scope_terms": [], "supporting_examples": [],
            "citations": citations, "uncertainties": [], "potential_conflicts": [], "prompt_version": PROMPT_VERSION,
        }
    if activity:
        activity("mapping_complete", {"topics": len(proposals), "pages": len(mapped_pages)})
    if progress:
        progress(len(topics), len(topics))
    return {"proposals": proposals, "sections_processed": len(chunks), "sections_total": len(chunks), "mapped_sections": len(mapped_pages), "unmapped_sections": len(chunks) - len(mapped_pages), "potential_conflict_count": 0, "validation_issues": [], "prompt_version": PROMPT_VERSION}
