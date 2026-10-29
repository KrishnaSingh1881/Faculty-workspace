"""Explicit stop cancels server work and saves the interrupted turn for its owner."""
import asyncio
import json
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from exam_assistant import api
from exam_assistant.activity import publish
from exam_assistant.db import ChatMessage, Conversation, Subject


def test_stop_response_cancels_server_task_and_preserves_turn():
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    for model in (Subject, Conversation, ChatMessage):
        model.__table__.create(engine)
    sessions = sessionmaker(engine, expire_on_commit=False)
    with sessions.begin() as db:
        db.add(Subject(id=1, code="test", name="Test", tree={}))
        db.add(Conversation(id=1, user_id=7, subject_id=1, title="Test chat"))

    async def run():
        cancelled = asyncio.Event()
        user = SimpleNamespace(id=7, role="teacher", subject_ids=[1])
        token = api.current_user.set(user)

        async def generate(body, db):
            publish({"agent": "workspace", "event": "conversation", "payload": {"conversation_id": 1}})
            publish({"agent": "workspace", "event": "tool", "payload": {"name": "lookup", "result": {"found": True}}})
            try:
                await asyncio.Event().wait()
            finally:
                cancelled.set()

        try:
            with patch.object(api, "Session", sessions), patch.object(api, "chat", generate), sessions() as db:
                response = await api.stream_chat(api.ChatInput(subject_id=1, conversation_id=1, text="Check my paper"), db)
                stream = response.body_iterator
                first = await anext(stream)
                payload = json.loads(first.split("data: ", 1)[1])
                run_id = payload["payload"]["run_id"]
                user.id = 8
                try:
                    await api.stop_chat(run_id)
                except HTTPException as exc:
                    assert exc.status_code == 404
                else:
                    raise AssertionError("Another user must not be allowed to stop this response")
                user.id = 7
                assert not cancelled.is_set()
                assert (await api.stop_chat(run_id))["status"] == "stopping"
                assert (await api.stop_chat(run_id))["status"] == "stopping"
                frames = []
                async for frame in stream:
                    frames.append(frame)
                assert cancelled.is_set()
                assert '"stopped": true' in frames[-1]
                await asyncio.sleep(0)
                assert run_id not in api.chat_runs
            with sessions() as db:
                messages = list(db.scalars(select(ChatMessage).order_by(ChatMessage.id)))
                assert [m.role for m in messages] == ["user", "assistant"]
                assert messages[1].payload["stopped"] is True
                assert any(event["event"] == "tool" for event in messages[1].payload["activity"])
        finally:
            api.current_user.reset(token)

    try:
        asyncio.run(run())
    finally:
        engine.dispose()
