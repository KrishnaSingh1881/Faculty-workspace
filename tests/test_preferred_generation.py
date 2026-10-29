import asyncio
from unittest.mock import AsyncMock
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from exam_assistant import api
from exam_assistant.db import Subject, Paper, Question, Comparison, PairResult, AuditEvent


def test_retry_repeat_and_save_actual_outcome(monkeypatch):
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    for model in (Subject, Paper, Question, Comparison, PairResult, AuditEvent):
        model.__table__.create(engine)
    sessions = sessionmaker(bind=engine, expire_on_commit=False)
    monkeypatch.setattr(api, 'Session', sessions)
    monkeypatch.setattr(api, 'ensure_not_cancelled', lambda job_id: None)
    monkeypatch.setattr(api, 'set_progress', lambda *args: None)
    with sessions.begin() as db:
        db.add(Subject(id=1, code='test', name='Test', tree={'nodes':[{'id':'t1','kind':'topic','label':'Topic'}]}))
        db.add_all([Paper(id=1, subject_id=1, title='Reference'), Paper(id=2, subject_id=1, title='Draft', generated=True, generation={'status':'queued'})])
        db.add(Question(id=1, paper_id=1, number='1a', text='Explain a reference topic', unit=1, topic_ids=['t1'], confirmed=True))
    draft = AsyncMock(side_effect=[[{'text':'First candidate repeated', 'topic_ids':['t1']}],[{'text':'Second candidate differs', 'topic_ids':['t1']}]])
    async def judge(q, refs, unit):
        label = 'A' if q.text.startswith('First') else 'B'
        return {'label':label,'reason':'Step 3', 'source':api.BLOCK_VERSION, 'model':'test', 'evidence':[{'id':'block','unit':unit,'questions':[{'id':refs[0].id,'number':refs[0].number,'text':refs[0].text,'revision':refs[0].revision}]}]}
    monkeypatch.setattr(api, 'draft_slot', draft)
    monkeypatch.setattr(api, 'classify_block', judge)
    slot={'unit':1,'topic_ids':['t1'],'marks':4,'count':1,'constraints':''}
    asyncio.run(api._preferred_generation_job({'paper_id':2,'reference_ids':[1],'slots':[slot]}, 1))
    with sessions() as db:
        paper=db.get(Paper,2)
        assert paper.questions[0].text == 'Second candidate differs'
        assert paper.generation['outcome_counts'] == {'A':0,'B':1,'C':0,'review':0}
        assert paper.generation['screens']['G1.1']['attempts'] == 2
        assert db.scalar(select(PairResult)).label == 'B'
        assert db.scalar(select(Comparison)).status == 'complete'
    assert draft.await_count == 2
    engine.dispose()


def test_insem_automatically_selects_ten_questions_per_unit(monkeypatch):
    from exam_assistant.db import BackgroundJob
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    for model in (Subject, Paper, Question, BackgroundJob, AuditEvent):
        model.__table__.create(engine)
    sessions = sessionmaker(bind=engine, expire_on_commit=False)
    monkeypatch.setattr(api, 'MODEL', 'test-model')
    monkeypatch.setattr(api, 'inspect_local_models', AsyncMock(return_value={'judge_installed': True}))
    with sessions.begin() as db:
        db.add(Subject(id=1, code='test', name='Test', tree={'nodes':[{'id':'test/u1/a','kind':'topic'}, {'id':'test/u2/a','kind':'topic'}]}))
        db.add(Paper(id=1, subject_id=1, title='Past paper'))
        db.add_all([Question(id=unit,paper_id=1,number=str(unit),text='Explain the topic',unit=unit,topic_ids=[f'test/u{unit}/a'],confirmed=True) for unit in (1,2)])
    with sessions() as db:
        result = asyncio.run(api.start_generation(api.GenerationInput(subject_id=1,title='InSem',insem=True,prefer_bc=True),db))
        slots=result['paper']['generation']['slots']
        assert len(slots)==20
        assert [slot['unit'] for slot in slots]==[1]*10+[2]*10
        assert [slot['number'] for slot in slots]==['1a','1b','1c','1d','1e','2a','2b','2c','2d','2e','3a','3b','3c','3d','3e','4a','4b','4c','4d','4e']
        assert all(slot['marks']==4 for slot in slots)
        assert result['paper']['generation']['reference_ids']==[1,2]
        assert result['paper']['generation']['prefer_bc'] is True
    engine.dispose()
