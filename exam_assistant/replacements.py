"""Factual coverage view for generated replacement candidates."""

from .knowledge import unit_for_topic


def replacement_report(subject, source_question, draft_paper, comparison=None) -> dict:
    generation = draft_paper.generation or {}
    valid_topics = {node["id"] for node in subject.tree.get("nodes", []) if node.get("kind") == "topic"}
    unit_topics = {topic_id for topic_id in valid_topics if unit_for_topic(topic_id) == source_question.unit}
    siblings = [question for question in source_question.paper.questions if question.id != source_question.id and question.confirmed]
    sibling_topics = {topic_id for question in siblings for topic_id in question.topic_ids if topic_id in valid_topics}
    before_topics = sibling_topics | {topic_id for topic_id in source_question.topic_ids if topic_id in valid_topics}
    results = list(comparison.results) if comparison else []
    candidates = []
    for candidate in draft_paper.questions:
        after_topics = sibling_topics | {topic_id for topic_id in candidate.topic_ids if topic_id in valid_topics}
        labels = {label: sum(result.label == label and result.target_id == candidate.id for result in results) for label in ("A", "B", "C", "review")}
        candidates.append({
            "id": candidate.id, "number": candidate.number, "text": candidate.text, "marks": candidate.marks,
            "topic_ids": candidate.topic_ids, "confirmed": candidate.confirmed,
            "coverage_after": {"covered_topics": len(after_topics), "unit_covered_topics": len(after_topics & unit_topics), "added_topic_ids": sorted(after_topics - before_topics), "lost_topic_ids": sorted(before_topics - after_topics)},
            "difficulty": {"requested": generation.get("requested_difficulty"), "measured": None},
            "screening": {"status": comparison.status if comparison else generation.get("status", "queued"), "A": labels["A"], "B": labels["B"], "C": labels["C"], "review": labels["review"]},
        })
    return {
        "draft_paper_id": draft_paper.id, "draft_title": draft_paper.title,
        "source_question": {"id": source_question.id, "paper_id": source_question.paper_id, "paper_title": source_question.paper.title, "number": source_question.number, "text": source_question.text, "marks": source_question.marks, "unit": source_question.unit, "topic_ids": source_question.topic_ids, "revision": source_question.revision},
        "source_changed": source_question.revision != generation.get("source_revision"),
        "coverage_before": {"covered_topics": len(before_topics), "unit_covered_topics": len(before_topics & unit_topics), "topic_ids": sorted(before_topics)},
        "difficulty_before": {"measured": None, "note": "The source question's difficulty has not been calibrated."},
        "requested_difficulty": generation.get("requested_difficulty"),
        "generation_status": generation.get("status"), "candidates": candidates,
        "note": "Coverage counts use confirmed syllabus tags. Requested difficulty is a drafting constraint, not a measured level. Screening labels are provisional; C alone does not prove novelty.",
    }
