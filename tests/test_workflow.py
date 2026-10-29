"""Small end-to-end check for the real API without substituting a model verdict."""
import asyncio
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import httpx
from sqlalchemy import select


class WorkflowTest(unittest.TestCase):
    def test_public_comparison_reason_uses_validated_mapping(self):
        from exam_assistant.engine import _decision_reason

        helper = {"alignments": [{"a_id": "q1_r1", "b_id": "q2_r1", "relation": "equivalent"}]}
        coverage = {"unmatched_a": [], "unmatched_b": []}
        self.assertIn("q1_r1 ↔ q2_r1", _decision_reason("A", helper, coverage, True))
        helper["alignments"][0]["relation"] = "overlap"
        coverage["unmatched_b"] = ["q2_r2"]
        reason = _decision_reason("B", helper, coverage, True)
        self.assertIn("partial alignment", reason)
        self.assertIn("additional reference asks: q2_r2", reason)
        helper["alignments"][0]["relation"] = "distinct"
        self.assertIn("no material assessed overlap", _decision_reason("C", helper, coverage, True))

    def test_question_parser_keeps_compound_parts_together(self):
        from exam_assistant.documents import draft_questions

        questions = draft_questions("""Q1. Explain process scheduling. [8 marks]
(a) Describe FCFS scheduling. [4 marks]
(b) Compare it with SJF. [4 marks]
OR
(c) Explain round-robin scheduling.""")
        assert len(questions) == 1
        assert "(a) Describe FCFS" in questions[0]["text"]
        assert "(b) Compare it with SJF" in questions[0]["text"]
        assert "\nOR\n" in questions[0]["text"]
        assert "(c) Explain round-robin" in questions[0]["text"]
        assert questions[0]["marks"] == 8
        assert [part["label"] for part in questions[0]["structure"]["parts"]] == ["prompt", "a", "b", "c"]
        assert questions[0]["structure"]["parts"][1]["marks"] == 4
        assert questions[0]["structure"]["choice_groups"][0]["alternatives"] == [["p2", "p3"], ["p4"]]

    def test_scanned_paper_parser_skips_instructions_and_keeps_or_groups(self):
        from exam_assistant.documents import draft_questions

        questions = draft_questions("""Instructions:
1. This question paper contains 2 pages.
2. Answer each new question on a new page.
Question No. 1
1 a) Define system software. (4) CO1
1 b) Give examples of assembly language. (3) CO1
Question No. 2
2 a) Explain a two-pass assembler. (4) CO1
2 b) Define a symbol table. (4) CO1
Group OR
2 c) Compare a compiler and assembler. (4) CO1
2 d) Explain linking and loading. (4) CO1
End of question paper""")
        self.assertEqual([q["number"] for q in questions], ["1", "2"])
        self.assertEqual([p["marks"] for p in questions[0]["structure"]["parts"]], [4, 3])
        self.assertEqual(questions[1]["structure"]["choice_groups"][0]["alternatives"], [["p1", "p2"], ["p3", "p4"]])
        self.assertNotIn("question paper contains", " ".join(q["text"] for q in questions))

    def test_confirmed_same_unit_scope_and_model_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            os.environ["DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", f"sqlite:///{directory}/test.db")
            # Keep this API workflow deterministic and prove its no-model
            # behavior even on developer machines with Ollama installed.
            os.environ["JUDGE_MODEL_NAME"] = ""
            os.environ["HELPER_MODEL_NAME"] = ""
            os.environ["MODEL_NAME"] = ""
            os.environ["EMBEDDING_MODEL_NAME"] = ""
            os.environ["MODEL_URL"] = "http://127.0.0.1:1"
            from exam_assistant.api import app
            from exam_assistant.db import AuditEvent, BackgroundJob, Comparison, PairResult, Paper, Question, Session, Subject, initialize
            # Other unit tests may have imported the runtime before these env settings.
            for module, values in (
                ("exam_assistant.model_runtime", {"JUDGE_MODEL": "", "HELPER_MODEL": "", "MODEL": "", "MODEL_URL": "http://127.0.0.1:1"}),
                ("exam_assistant.engine", {"JUDGE_MODEL": "", "HELPER_MODEL": ""}),
                ("exam_assistant.api", {"MODEL": ""}),
            ):
                mocked = patch.multiple(module, **values)
                mocked.start()
                self.addCleanup(mocked.stop)

            initialize()

            async def run():
                async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testclient") as client:
                    subjects = (await client.get("/api/subjects")).json()
                    os_subject = next(s for s in subjects if s["code"] == "2301202")
                    assert os_subject["active"]
                    removed_gate = await client.post(f"/api/subjects/{os_subject['id']}/approve", json={"answers": {}})
                    assert removed_gate.status_code in (404, 405)
                    paper = (await client.post("/api/papers", json={"subject_id": os_subject["id"], "title": "Test draft"})).json()
                    questions = []
                    for number, unit in (("1", 2), ("2", 2), ("3", 3)):
                        topic = "2301202/u2/introduction-to-os" if unit == 2 else "2301202/u3/synchronization/critical-section-problem"
                        response = await client.post(f"/api/papers/{paper['id']}/questions", json={"number": number, "text": "Explain a confirmed concept", "unit": unit, "topic_ids": [topic], "confirmed": True})
                        assert response.status_code == 200, response.text
                        assert response.json()["structure"]["parts"][0]["label"] == "prompt"
                        questions.append(response.json())
                    wrong_unit = await client.post(f"/api/papers/{paper['id']}/questions", json={"number": "4", "text": "A mislabeled question", "unit": 2, "topic_ids": ["2301202/u3/synchronization/critical-section-problem"], "confirmed": True})
                    assert wrong_unit.status_code == 422
                    scope = {"subject_id": os_subject["id"], "title": "Test comparison", "target_ids": [questions[0]["id"]], "reference_ids": [questions[1]["id"], questions[2]["id"]]}
                    preview = (await client.post("/api/comparisons/preview", json=scope)).json()
                    assert preview["pairs"] == 1
                    assert len(preview["skipped"]) == 1
                    blocked = await client.post("/api/comparisons", json=scope)
                    assert blocked.status_code == 503
                    with Session.begin() as db:
                        suggestion = Paper(subject_id=os_subject["id"], title="Replacement fixture", generated=True, generation={"replacement_for_question_id": questions[0]["id"], "source_revision": 1, "requested_difficulty": "advanced", "status": "checking", "reference_ids": [questions[1]["id"]]})
                        db.add(suggestion)
                        db.flush()
                        candidate = Question(paper_id=suggestion.id, number="G1.1", text="Explain an advanced confirmed concept", unit=2, topic_ids=["2301202/u2/introduction-to-os"], confirmed=True)
                        db.add(candidate)
                        db.flush()
                        suggestion_id, candidate_id = suggestion.id, candidate.id
                    replacement = await client.get(f"/api/papers/{suggestion_id}/replacement-analysis")
                    assert replacement.status_code == 200 and replacement.json()["candidates"][0]["difficulty"]["measured"] is None
                    unscreened = await client.post(f"/api/questions/{questions[0]['id']}/apply-replacement", json={"candidate_id": candidate_id})
                    assert unscreened.status_code == 409
                    with Session() as db:
                        assert db.get(Question, questions[0]["id"]).text == questions[0]["text"]
                    analysis = (await client.get(f"/api/papers/{paper['id']}/analysis")).json()
                    assert analysis["confirmed"] == 3
                    subject_analysis = (await client.get(f"/api/subjects/{os_subject['id']}/analytics")).json()
                    assert "historical_topic_recurrence_by_year" in subject_analysis
                    streamed = await client.post("/api/chat/stream", json={"subject_id": os_subject["id"], "text": "Show the syllabus"})
                    assert streamed.status_code == 200, streamed.text
                    assert "event: activity" in streamed.text and "event: complete" in streamed.text
                    uploaded = (await client.post("/api/papers", json={"subject_id": os_subject["id"], "title": "Uploaded draft"})).json()
                    extracted = await client.post(f"/api/papers/{uploaded['id']}/upload", files={"file": ("paper.txt", b"Q1. Explain scheduling.\nQ2. Describe deadlock prevention.", "text/plain")})
                    chat_upload = await client.post("/api/chat/upload", data={"subject_id": str(os_subject["id"]), "kind": "paper", "status": "reference"}, files={"file": ("chat-paper.txt", b"Q1. Explain process scheduling.\nQ2. Describe deadlock prevention.", "text/plain")})
                    assert chat_upload.status_code == 200, chat_upload.text
                    chat_result = chat_upload.json()
                    assert chat_result["view"] == "chat"
                    uploaded_questions = chat_result["upload"]["paper"]["questions"]
                    assert [q["number"] for q in uploaded_questions] == ["1", "2"]
                    assert "Explain process scheduling." in uploaded_questions[0]["text"]
                    assert "Describe deadlock prevention." in uploaded_questions[1]["text"]
                    assert chat_result["upload"]["tagging_job_id"] is None
                    assert extracted.status_code == 200, extracted.text
                    assert extracted.json()["drafted_questions"] == 2
                    assert len(extracted.json()["paper"]["questions"]) == 2
                    material = await client.post(f"/api/subjects/{os_subject['id']}/materials", files={"file": ("notes.txt", b"Deadlock prevention breaks a necessary condition.", "text/plain")})
                    assert material.status_code == 200, material.text
                    assert material.json()["pages"] == 1
                    proposal = await client.post(f"/api/materials/{material.json()['id']}/propose", json={"topic_id": "2301202/u3/deadlock/prevention"})
                    assert proposal.status_code == 503
                    with Session.begin() as db:
                        db.add(Comparison(subject_id=os_subject["id"], title="Empty export", target_ids=[questions[0]["id"]], reference_ids=[questions[1]["id"]], status="failed", progress=0, total=1, error="Model unavailable"))
                        db.flush()
                        from exam_assistant.engine import pair_key
                        target, reference = db.get(Question, questions[0]["id"]), db.get(Question, questions[1]["id"])
                        saved_result = PairResult(comparison_id=1, target_id=target.id, reference_id=reference.id, label="review", reason="Model checks were incomplete", evidence=[{"id": "q1", "source": "confirmed target question", "text": target.text}, {"id": "q2", "source": "confirmed reference question", "text": reference.text}], source="model", cache_key=pair_key(target, reference, db.get(Subject, os_subject["id"]).tree_version))
                        db.add(saved_result)
                        db.flush()
                        saved_result_id = saved_result.id
                    from exam_assistant.chat_tools import bind_chat_tools
                    with Session() as db:
                        tools = bind_chat_tools(db, db.get(Subject, os_subject["id"]), model_configured=False, prior_tool_trace=[{"name": "list_comparisons", "result": {"comparisons": [{"id": 1}]}}, {"name": "search_questions", "result": {"questions": [{"id": questions[0]["id"]}]}}])
                        assert tools["list_comparisons"]({"query": "Empty export"})["total_matches"] == 1
                        listed = tools["list_comparison_results"]({"comparison_id": 1, "label": "review", "question_id": questions[0]["id"]})
                        assert listed["total_matches"] == 1 and listed["results"][0]["id"] == saved_result_id
                        inspected = tools["inspect_comparison_result"]({"result_id": saved_result_id})
                        assert inspected["label"] == "review" and inspected["evidence_total"] == 2 and not inspected["stale"]
                        noted = await tools["note_on_selected_result"]({"result_id": saved_result_id, "comment": "Needs a closer look"})
                        assert noted["success"]
                        resolved = await tools["resolve_selected_result"]({"result_id": saved_result_id, "label": "B", "reason": "Different required depth"})
                        assert resolved["success"] and resolved["result_id"] == saved_result_id
                    with Session() as db:
                        assert db.get(PairResult, saved_result_id).source == "faculty_case_review"
                        assert db.scalar(select(AuditEvent).where(AuditEvent.action == "comparison_case_resolution"))
                    report = await client.get("/api/comparisons/1/export?format=pdf")
                    assert report.status_code == 200 and report.content.startswith(b"%PDF")
                    sheet = await client.get("/api/comparisons/1/export?format=xlsx")
                    assert sheet.status_code == 200 and sheet.content.startswith(b"PK")
                    queued_export = await client.post("/api/comparisons/1/exports", json={"format": "xlsx"})
                    assert queued_export.status_code == 200 and queued_export.json()["status"] == "queued"
                    export_job_id = queued_export.json()["id"]
                    with Session.begin() as db:
                        export_job = db.get(BackgroundJob, export_job_id)
                        export_job.status, export_job.attempts = "running", 1
                        export_payload = dict(export_job.payload)
                    import exam_assistant.api as api_module
                    export_root = Path(directory) / "workspace-root"
                    with patch.object(api_module, "ROOT", export_root):
                        await api_module.JOB_HANDLERS["comparison_export"](export_payload, export_job_id)
                        with Session.begin() as db:
                            db.get(BackgroundJob, export_job_id).status = "complete"
                        export_detail = await client.get(f"/api/jobs/{export_job_id}")
                        assert export_detail.status_code == 200 and export_detail.json()["download_url"]
                        queued_file = await client.get(export_detail.json()["download_url"])
                        assert queued_file.status_code == 200 and queued_file.content.startswith(b"PK")
                        from exam_assistant.chat_tools import bind_chat_tools
                        with Session() as db:
                            tools = bind_chat_tools(db, db.get(Subject, os_subject["id"]), model_configured=False, is_admin=False, prior_tool_trace=[{"name": "list_jobs", "result": {"jobs": [{"id": export_job_id}]}}])
                            status = await tools["manage_job"]({"job_id": export_job_id, "action": "status"})
                            assert status["file_url"] == export_detail.json()["download_url"]
                        with Session.begin() as db:
                            db.get(BackgroundJob, export_job_id).finished_at = datetime.now(timezone.utc) - timedelta(days=31)
                        import exam_assistant.jobs as jobs_module
                        with patch.object(jobs_module, "ROOT", export_root):
                            assert jobs_module.expire_export_artifacts(30) == 1
                        expired = await client.get(f"/api/jobs/{export_job_id}")
                        assert expired.json()["artifact_expired"] and expired.json()["download_url"] is None
                        assert (await client.get(f"/api/jobs/{export_job_id}/download")).status_code == 410
                        with Session() as db:
                            tools = bind_chat_tools(db, db.get(Subject, os_subject["id"]), model_configured=False, is_admin=False, prior_tool_trace=[{"name": "list_jobs", "result": {"jobs": [{"id": export_job_id}]}}])
                            status = await tools["manage_job"]({"job_id": export_job_id, "action": "status"})
                            assert status["artifact_expired"] and status["file_url"] is None
                    live = await client.get("/api/comparisons/1/events")
                    assert live.status_code == 200 and '"status": "failed"' in live.text
                    removed = await client.delete(f"/api/papers/{uploaded['id']}")
                    assert removed.status_code == 200 and removed.json()["deleted"] == uploaded["id"]

                    iot_subject = next(s for s in subjects if s["code"] == "2301306A")
                    iot_paper = (await client.post("/api/papers", json={"subject_id": iot_subject["id"], "title": "IoT private job"})).json()
                    with Session.begin() as db:
                        private_job = BackgroundJob(kind="tag_paper", payload={"paper_id": iot_paper["id"]}, status="queued")
                        private_comparison = Comparison(subject_id=iot_subject["id"], title="IoT private comparison", target_ids=[], reference_ids=[], status="complete", progress=0, total=0)
                        db.add(private_comparison)
                        db.flush()
                        private_export = BackgroundJob(kind="comparison_export", payload={"comparison_id": private_comparison.id, "format": "md"}, status="queued")
                        db.add(private_job)
                        db.add(private_export)
                        db.flush()
                        private_job_id = private_job.id
                        private_comparison_id = private_comparison.id
                        private_export_id = private_export.id

                    os.environ.update(AUTH_MODE="shared", ADMIN_EMAIL="admin@example.edu", ADMIN_PASSWORD="initial-password-123")
                    initialize()
                    anonymous = await client.get("/api/subjects")
                    assert anonymous.status_code == 401
                    admin = await client.post("/api/auth/login", json={"email": "admin@example.edu", "password": "initial-password-123"})
                    assert admin.status_code == 200, admin.text
                    teacher = await client.post("/api/users", json={"email": "teacher@example.edu", "display_name": "Teacher", "password": "teacher-password-123", "role": "teacher", "subject_ids": [os_subject["id"]]})
                    assert teacher.status_code == 200, teacher.text
                    await client.post("/api/auth/logout")
                    logged_in = await client.post("/api/auth/login", json={"email": "teacher@example.edu", "password": "teacher-password-123"})
                    assert logged_in.status_code == 200
                    visible = (await client.get("/api/subjects")).json()
                    assert [item["code"] for item in visible] == ["2301202"]
                    denied = await client.get("/api/users")
                    assert denied.status_code == 403
                    hidden_job = await client.get(f"/api/jobs/{private_job_id}")
                    assert hidden_job.status_code == 403
                    assert (await client.get(f"/api/comparisons/{private_comparison_id}/export")).status_code == 403
                    assert (await client.post(f"/api/comparisons/{private_comparison_id}/exports", json={"format": "pdf"})).status_code == 403
                    assert (await client.get(f"/api/jobs/{private_export_id}")).status_code == 403
                    assert (await client.get(f"/api/jobs/{private_export_id}/download")).status_code == 403
                    assert (await client.get("/api/admin/backup")).status_code == 403
                    with Session() as db:
                        tools = bind_chat_tools(db, db.get(Subject, os_subject["id"]), model_configured=False, is_admin=False, prior_tool_trace=[{"name": "list_jobs", "result": {"jobs": [{"id": private_export_id}]}}])
                        hidden_status = await tools["manage_job"]({"job_id": private_export_id, "action": "status"})
                        assert "error" in hidden_status and "file_url" not in hidden_status
                    os.environ.pop("AUTH_MODE")
                    os.environ.pop("ADMIN_EMAIL")
                    os.environ.pop("ADMIN_PASSWORD")

                    with Session.begin() as db:
                        job = BackgroundJob(kind="tag_paper", payload={"paper_id": paper["id"]}, status="queued")
                        db.add(job)
                        db.flush()
                        queued_job_id = job.id
                    cancelled = await client.post(f"/api/admin/jobs/{queued_job_id}/cancel")
                    assert cancelled.status_code == 200 and cancelled.json()["status"] == "cancelled"

                    with Session.begin() as db:
                        running = BackgroundJob(kind="tag_paper", payload={"paper_id": paper["id"]}, status="running")
                        db.add(running)
                        db.flush()
                        running_job_id = running.id
                    requested = await client.post(f"/api/admin/jobs/{running_job_id}/cancel")
                    assert requested.status_code == 200 and requested.json()["status"] == "cancel_requested"
                    from exam_assistant.jobs import JobCancelled, ensure_not_cancelled
                    with self.assertRaises(JobCancelled):
                        ensure_not_cancelled(running_job_id)

                    from exam_assistant.chat_tools import bind_chat_tools
                    with Session() as db:
                        registry = bind_chat_tools(
                            db,
                            db.get(Subject, os_subject["id"]),
                            model_configured=False,
                            prior_tool_trace=[{"name": "search_papers", "result": {"papers": [{"id": paper["id"]}]}}],
                        )
                        archived = registry["set_paper_archived"]({"paper_id": paper["id"], "archived": True})
                        assert archived["success"] is True

            asyncio.run(run())


if __name__ == "__main__":
    unittest.main()
