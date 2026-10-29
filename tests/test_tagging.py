"""Template units, restricted topic prompts, validation and incremental saves."""
import asyncio
from types import SimpleNamespace
from unittest.mock import patch

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from exam_assistant import api
from exam_assistant.db import AuditEvent, BackgroundJob, Paper, Question, Subject, Template


def test_template_parent_units_and_topic_tagging():
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    for model in (Subject, Paper, Question, Template, AuditEvent, BackgroundJob):
        model.__table__.create(engine)
    sessions = sessionmaker(engine, expire_on_commit=False)
    with sessions() as db:
        db.add(Subject(id=1, code="test", name="Test", tree={"nodes": [
            {"id": f"test/u{unit}/topic", "kind": "topic", "label": f"Unit {unit} topic"} for unit in (1, 2, 3)
        ]}))
        template = Template(kind="comparison", name="InSem", definition={"question_pattern": {"units": [
            {"unit": 1, "questions": ["1a", "2a"]}, {"unit": 2, "questions": ["3a", "4a"]}
        ]}})
        db.add(template)
        paper = Paper(subject_id=1, title="InSem")
        db.add(paper); db.flush()
        for number in ("Q1(a)", "1b", "2(d)", "3a", "4b"):
            db.add(Question(paper_id=paper.id, number=number, text="Explain the concept"))
        db.commit()
        pid = paper.id
        mapping = api.template_question_units(template, paper.questions)
        assert list(mapping.values()) == [1, 1, 1, 2, 2]
        assert api.template_question_units(template, [SimpleNamespace(id=999, number="5a")]) == {}
        job = api.enqueue_paper_tagging(db, paper)
        jid = job.id
        job.status = "running"; db.commit()
        assert [q.unit for q in paper.questions] == [1, 1, 1, 2, 2]
        assert not any(q.confirmed for q in paper.questions)

    calls = []

    async def model(messages, **options):
        import json
        request = json.loads(messages[1]["content"])
        calls.append(request)
        assert options["think"] is False
        unit = request["unit"]
        assert all(topic["unit"] == unit for topic in request["topics"])
        options["on_event"]({"event": "content"})
        results = []
        for index, q in enumerate(request["questions"]):
            # One uncertain answer and one invalid cross-unit tag must stay unconfirmed.
            if unit == 2 and index == 0:
                results.append({"id": q["id"], "topic_ids": [], "uncertain": True, "reason": "No suitable topic"})
            else:
                results.append({"id": q["id"], "topic_ids": [f'test/u{3 if unit == 2 else unit}/topic'], "unit": unit, "uncertain": False})
        return {"results": results}

    token = api.current_user.set(None)
    try:
        with patch.object(api, "Session", sessions), patch("exam_assistant.jobs.Session", sessions), patch.object(api, "model_json", model):
            try:
                asyncio.run(api.tag_paper(pid, jid))
            except RuntimeError as exc:
                assert "failed for 1 question" in str(exc)
            else:
                raise AssertionError("Invalid topic must fail tagging")
            assert len(calls) == 2  # one model call per unit, rather than per question
            with sessions() as db:
                questions = list(db.scalars(select(Question).order_by(Question.id)))
                assert [q.unit for q in questions] == [1, 1, 1, 2, 2]
                assert [q.confirmed for q in questions] == [True, True, True, False, False]
                saved = db.get(BackgroundJob, jid)
                assert saved.progress == saved.total == 5
                assert len(saved.payload["tagging"]["needs_review"]) == 2
            calls.clear()
            try:
                asyncio.run(api.tag_paper(pid, jid))
            except RuntimeError:
                pass
            assert len(calls) == 1 and calls[0]["unit"] == 2  # successful tags survive retries
    finally:
        api.current_user.reset(token)
        engine.dispose()


def test_conflicting_templates_do_not_guess_units():
    engine = create_engine("sqlite://")
    for model in (Template, Paper, Question):
        model.__table__.create(engine)
    with sessionmaker(engine)() as db:
        paper = Paper(subject_id=1, title="Unknown pattern")
        db.add(paper); db.flush()
        db.add(Question(paper_id=paper.id, number="1a", text="Question"))
        for unit in (1, 2):
            db.add(Template(kind="comparison", name=str(unit), definition={"question_pattern": {"units": [{"unit": unit, "questions": ["1"]}]}}))
        db.commit()
        assert api.apply_tagging_pattern(db, paper) == {}
        assert paper.questions[0].unit is None
    engine.dispose()
