import asyncio
import io
from types import SimpleNamespace
import httpx
from openpyxl import Workbook
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from exam_assistant.api import app, current_user, db_session, require_access
from exam_assistant.db import AuditEvent, Template


def test_report_template_import():
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    for model in (Template, AuditEvent):
        model.__table__.create(engine)
    async def access():
        current_user.set(SimpleNamespace(id=1, role='admin', subject_ids=[]))
    async def session():
        with Session(engine) as db:
            yield db
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='http://test') as client:
            text = await client.post('/api/templates/import-report', files={'file': ('report.txt', b'Classification | Reason', 'text/plain')})
            assert text.status_code == 200 and text.json()['columns'] == ['label', 'reason']
            book = Workbook(); book.active.append(['Base question', 'Reference question']); output = io.BytesIO(); book.save(output)
            excel = await client.post('/api/templates/import-report', files={'file': ('report.xlsx', output.getvalue())})
            assert excel.status_code == 200 and excel.json()['columns'] == ['base_question_number', 'reference_question_number']
            invalid = await client.post('/api/templates/import-report', files={'file': ('bad.xlsx', b'not an excel file')})
            assert invalid.status_code == 422
    previous = app.dependency_overrides.copy()
    app.dependency_overrides.update({require_access: access, db_session: session})
    try:
        asyncio.run(run())
    finally:
        app.dependency_overrides.clear(); app.dependency_overrides.update(previous); engine.dispose()
