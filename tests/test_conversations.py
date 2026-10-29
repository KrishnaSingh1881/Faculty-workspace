"""Conversation deletion removes messages and respects ownership and subject access."""
import asyncio
from types import SimpleNamespace

import httpx
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from exam_assistant.api import app, current_user, db_session, require_access
from exam_assistant.db import AuditEvent, ChatMessage, Conversation, Subject


def test_delete_conversation():
    engine = create_engine("sqlite://", poolclass=StaticPool, connect_args={"check_same_thread": False})
    event.listen(engine, "connect", lambda connection, _: connection.execute("PRAGMA foreign_keys=ON"))
    for model in (Subject, Conversation, ChatMessage, AuditEvent):
        model.__table__.create(engine)
    with Session(engine) as db:
        db.add(Subject(id=1, code="test", name="Test", tree={}))
        db.commit()
        db.add_all([Conversation(id=1, user_id=7, subject_id=1, title="Delete me"), Conversation(id=2, user_id=8, subject_id=1, title="Keep me")])
        db.commit()
        db.add_all([ChatMessage(conversation_id=cid, role="user", text="Hello") for cid in (1, 2)])
        db.commit()

    user = SimpleNamespace(id=7, role="teacher", subject_ids=[1])

    async def access():
        current_user.set(user)

    async def session():
        with Session(engine) as db:
            yield db

    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://testclient") as client:
            assert (await client.delete("/api/conversations/999")).status_code == 404
            assert (await client.delete("/api/conversations/2")).status_code == 404
            user.subject_ids = []
            assert (await client.delete("/api/conversations/1")).status_code == 403
            user.subject_ids = [1]
            response = await client.delete("/api/conversations/1")
            assert response.status_code == 200, response.text
            assert (await client.get("/api/conversations/1")).status_code == 404
            assert (await client.delete("/api/conversations/1")).status_code == 404

    previous = app.dependency_overrides.copy()
    app.dependency_overrides.update({require_access: access, db_session: session})
    try:
        asyncio.run(run())
        with Session(engine) as db:
            assert db.get(Conversation, 1) is None
            assert db.get(Conversation, 2) is not None
            assert [m.conversation_id for m in db.scalars(select(ChatMessage))] == [2]
            assert db.scalar(select(AuditEvent)).details == {"conversation_id": 1, "by": 7}
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
        engine.dispose()
