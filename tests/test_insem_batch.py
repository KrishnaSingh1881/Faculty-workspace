import asyncio
from unittest.mock import AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from exam_assistant import api
from exam_assistant.generation import validate_batch_screen
from exam_assistant.db import Subject, Paper, Question, AuditEvent


def test_screen_missing_or_duplicate_is_review():
    result=validate_batch_screen({'results':[{'number':'1a','status':'different','reason':'different'}, {'number':'1a','status':'different','reason':'duplicate'}]}, {'1a','1b'})
    assert result['1a']['status']=='review' and result['1b']['status']=='review'


def test_batch_generation_retries_only_repeats_and_resumes(monkeypatch):
    engine=create_engine('sqlite://',poolclass=StaticPool,connect_args={'check_same_thread':False})
    for model in (Subject,Paper,Question,AuditEvent): model.__table__.create(engine)
    sessions=sessionmaker(bind=engine,expire_on_commit=False)
    monkeypatch.setattr(api,'Session',sessions)
    monkeypatch.setattr(api,'ensure_not_cancelled',lambda _:None)
    monkeypatch.setattr(api,'set_progress',lambda *args:None)
    slots=[{'number':str(i),'unit':1,'topic_ids':['t'],'marks':4,'count':1} for i in range(5)]
    with sessions.begin() as db:
        db.add(Subject(id=1,code='T',name='Test',tree={'nodes':[{'id':'t'}]}))
        db.add_all([Paper(id=1,subject_id=1,title='Past'),Paper(id=2,subject_id=1,title='Draft',generated=True,generation={'screen_strategy':'insem_quick_v1'})])
        db.add(Question(id=1,paper_id=1,number='q',text='Explain the past topic',unit=1,confirmed=True))
    async def draft(batch,topics,refs,existing):
        return {slot['number']:{'text':f"Question {slot['number']} attempt {len(existing)} about syllabus",'topic_ids':['t']} for slot in batch}
    async def screen(batch,refs,existing):
        return {q['number']:{'status':'too_close' if q['number']=='1' and not existing else 'different','reason':'Checked'} for q in batch}
    d=AsyncMock(side_effect=draft); check=AsyncMock(side_effect=screen)
    monkeypatch.setattr(api,'draft_batch_with_fallback',d);monkeypatch.setattr(api,'screen_batch',check)
    monkeypatch.setattr(api,'semantic_topic_hints',AsyncMock(return_value={'t': [{'question':'q','similarity':0.9}]}))
    payload={'paper_id':2,'reference_ids':[1],'slots':slots}
    asyncio.run(api._insem_batch_generation_job(payload,1))
    with sessions() as db:
        paper=db.get(Paper,2)
        assert len(paper.questions)==5 and paper.generation['quick_counts']['different']==5
        assert len(paper.generation['quick_screens'])==5
    assert d.await_count==2 and len(d.await_args_list[1].args[0])==1
    assert d.await_args_list[0].args[1][0]['related_past_questions'][0]['question'] == 'q'
    asyncio.run(api._insem_batch_generation_job(payload,1))
    assert d.await_count==2
    engine.dispose()


def test_invalid_batch_splits_into_smaller_calls(monkeypatch):
    from exam_assistant import generation
    async def draft(slots, topics, refs, existing):
        if len(slots) > 2:
            raise ValueError('incomplete')
        return {slot['number']:{'text': 'valid ' + slot['number']} for slot in slots}
    monkeypatch.setattr(generation, 'draft_batch', draft)
    slots=[{'number':str(i)} for i in range(5)]
    result=asyncio.run(generation.draft_batch_with_fallback(slots, [], [], []))
    assert set(result)==set(str(i) for i in range(5))


def test_semantic_hints_rank_past_questions_for_topics(monkeypatch):
    from exam_assistant import generation
    monkeypatch.setattr(generation, 'embed_texts', AsyncMock(return_value=[[1, 0], [0, 1], [1, 0]]))
    result = asyncio.run(generation.semantic_topic_hints(
        [{'id':'1', 'label':'topic'}],
        [{'number':'2', 'text':'other'}, {'number':'3', 'text':'similar'}]))
    assert result['1'][0] == {'question':'3', 'similarity':1.0}
    assert result['1'][1]['question'] == '2'
