import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock

from exam_assistant import engine


def test_judge_uses_helper_only_when_requested(monkeypatch):
    question = lambda text: SimpleNamespace(text=text, unit=1, topic_ids=[], marks=None)
    profile = {"requirements": [{"id": "r"}], "parts": [], "choice_rule": None, "concerns": []}
    mapping = [{"a_id": "a", "b_id": "b"}]
    data = {"requirements_a": profile["requirements"], "requirements_b": profile["requirements"], "compound_mapping": mapping,
            "alignments": [{"a_id": "a", "b_id": "b", "relation": "equivalent"}], "concerns": []}
    coverage = {"full_coverage_both_directions": True, "unmatched_a": [], "unmatched_b": []}
    decision = {"label": "A", "reason": "same", "evidence_ids": ["q1", "q2"], "shared_requirements": ["same"],
                "differences": [], "missed_requirements": [], "choice_logic_equivalent": True, "confidence": 1}
    required = ["compare_requirements", "check_compound_alignment", "build_signal_matrix"]
    monkeypatch.setattr(engine, "classifier_models_ready", lambda: True)
    monkeypatch.setattr(engine, "validate_analysis", lambda p, q: p)
    monkeypatch.setattr(engine, "bind_profile", lambda p, source: p.copy())
    monkeypatch.setattr(engine, "evidence_bundle", lambda *args: [{"id": "q1"}, {"id": "q2"}])
    monkeypatch.setattr(engine, "ComparisonToolbox", lambda *args: SimpleNamespace(call=lambda *args: {}))
    monkeypatch.setattr(engine, "_validate_helper", lambda *args: ([data.copy()], coverage))
    for name in ("_tools_succeeded", "_comparison_calls_match", "_compound_call_matches", "_signal_matrix_call_matches"):
        monkeypatch.setattr(engine, name, lambda *args: True)
    @asynccontextmanager
    async def session():
        yield
    monkeypatch.setattr(engine, "model_session", session)
    monkeypatch.setattr(engine, "unload_model", AsyncMock())
    helper = AsyncMock(return_value=({}, [], required))
    monkeypatch.setattr(engine, "run_helper", helper)
    judge = AsyncMock(return_value=(decision, [], required))
    monkeypatch.setattr(engine, "run_judge", judge)
    result = asyncio.run(engine.judge_pair(question('one'), question('two'), {}, profiles=(profile, profile)))
    assert result['label'] == 'A'
    helper.assert_not_awaited()
    judge.side_effect = [({**decision, 'needs_helper': True}, [], required), (decision, [], required)]
    result = asyncio.run(engine.judge_pair(question('one'), question('two'), {}, profiles=(profile, profile)))
    assert result['label'] == 'A'
    helper.assert_awaited_once()
