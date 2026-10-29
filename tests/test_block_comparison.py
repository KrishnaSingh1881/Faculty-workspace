import asyncio
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
from exam_assistant import block_comparison as block
from exam_assistant.api import group_comparison_blocks


def question(identifier, paper, unit=1):
    return SimpleNamespace(id=identifier, revision=1, paper_id=paper, number=str(identifier), text=f'Explain topic {identifier}', unit=unit)


def test_group_by_target_paper_and_unit_and_invalidate_cache():
    a, b = question(1, 1), question(2, 1, 2)
    x, y, z = question(3, 2), question(4, 2), question(5, 3)
    groups = group_comparison_blocks([(a, x), (a, y), (a, z), (b, x)], {1: 1, 2: 2})
    assert [(target.id, [r.id for r in refs], unit) for target, refs, unit in groups] == [(1, [3, 4], 1), (1, [5], 1), (2, [3], 2)]
    key = block.block_key(a, [x, y], 1, 1)
    y.revision += 1
    assert key != block.block_key(a, [x, y], 1, 1)


def test_one_judge_call_reads_entire_block(monkeypatch):
    @asynccontextmanager
    async def session():
        yield
    monkeypatch.setattr(block, 'model_session', session)
    model = AsyncMock(return_value={'message': {'content': 'ANSWER: B\nREASON: Step 3 found only partial coverage in Q2.'}})
    monkeypatch.setattr(block, 'chat_json_in_session', model)
    a, x, y = question(1, 1), question(2, 2), question(3, 2)
    result = asyncio.run(block.classify_block(a, [x, y], 1))
    assert result['label'] == 'B'
    assert [item['id'] for item in result['evidence'][1]['questions']] == [2, 3]
    assert model.await_count == 1
    assert 'Q2:' in model.call_args.args[1][1]['content'] and 'Q3:' in model.call_args.args[1][1]['content']
    assert model.call_args.kwargs['think'] is False
    assert model.call_args.kwargs['format_json'] is False
    assert block.parse_response('ANSWER: A\nextra') [0] == 'review'


def test_instruction_and_citation_checks():
    base = question(1, 1); base.text = 'Explain process scheduling.'
    ref = question(2, 2); ref.text = 'Describe process scheduling.'
    assert block.validate_decision('ANSWER: A\nREASON: Step 3: Q2 covers process scheduling with the same depth.', base, [ref])[0] == 'A'
    assert block.validate_decision('ANSWER: B\nREASON: Step 3: Q2 covers only part of process scheduling.', base, [ref])[0] == 'B'
    assert block.validate_decision('ANSWER: C\nREASON: Step 2: the topic is absent.', base, [ref])[0] == 'review'
    assert block.validate_decision('ANSWER: A\nREASON: Step 3: Q9 matches.', base, [ref])[0] == 'review'
    ref.text = 'Compare scheduling methods.'
    assert block.validate_decision('ANSWER: A\nREASON: Step 3: Q2 matches.', base, [ref])[0] == 'A'
    assert block.validate_decision('ANSWER: B\nREASON: Step 3: Q2 compares scheduling.', base, [ref])[0] == 'B'
    base.text = 'Draw a scheduling diagram.'
    assert block.validate_decision('ANSWER: A\nREASON: Step 3: Q2 matches.', base, [ref])[0] == 'A'
    assert block.instruction_verb('Q2a. Write short note on scheduling')['group'] == 'A'


def test_helper_only_for_unresolved_judge(monkeypatch):
    @asynccontextmanager
    async def session():
        yield
    monkeypatch.setattr(block, 'model_session', session)
    monkeypatch.setattr(block, 'HELPER_MODEL', block.JUDGE_MODEL or 'test')
    judge = AsyncMock(side_effect=[
        {'message': {'content': 'ANSWER: A\nREASON: Step 3: the topic matches.'}},
        {'message': {'content': 'ANSWER: A\nREASON: Step 3: Q2 covers the same topic.'}},
        {'message': {'content': 'ANSWER: A\nREASON: Step 3: Q2 covers the same topic and depth.'}},
    ])
    monkeypatch.setattr(block, 'chat_json_in_session', judge)
    a, ref = question(1, 1), question(2, 2)
    events = []
    result = asyncio.run(block.classify_block(a, [ref], 1, on_event=events.append))
    assert result['label'] == 'A'
    assert judge.await_count == 3
    assert any(event['event'] == 'helper_requested' for event in events)


def test_c_with_shared_topic_phrase_needs_review():
    base = question(1, 1); base.text = 'Compare system software and application software.'
    ref = question(2, 2); ref.text = 'Define system software and explain its components.'
    label, reason, checks = block.validate_decision('ANSWER: C\nREASON: Step 2: the comparison topic is absent.', base, [ref])
    assert label == 'review'
    assert checks['shared_phrases'] == {'2': ['system software']}
    assert block.validate_decision('ANSWER: B\nREASON: Step 2: Q2 covers system software, but not application software.', base, [ref])[0] == 'B'


def test_expanded_instruction_verbs_and_unknowns():
    for verb, group in [('Discuss', 'A'), ('Draw', 'A'), ('Distinguish', 'B'),
                        ('Contrast', 'B'), ('Develop', 'C'), ('Formulate', 'C')]:
        assert block.instruction_verb(f'Q2a. {verb} the process')['group'] == group
    assert block.instruction_verb('List the process states')['group'] is None


def test_unknown_verbs_are_context_not_automatic_review():
    base, ref = question(1, 1), question(2, 2)
    base.text, ref.text = 'List the process states.', 'Identify the process states.'
    result = block.validate_decision('ANSWER: A\nREASON: Step 3: Q2 covers the same process states and task.', base, [ref])
    assert result[0] == 'A'
    assert result[2]['base_verb']['group'] is None
