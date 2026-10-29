"""Restore a real isolated database and content-addressed upload."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class BackupTest(unittest.TestCase):
    def test_sqlite_restore_and_reject_changed_upload(self):
        with tempfile.TemporaryDirectory() as directory:
            script = r'''
import hashlib
from pathlib import Path
from exam_assistant.db import Session, Subject, Paper, Question, initialize
import exam_assistant.backup as backup

root = Path(__import__('os').environ['BACKUP_TEST_ROOT'])
backup.ROOT = root
initialize()
content = b'backup fixture upload'
digest = hashlib.sha256(content).hexdigest()
uploads = root / 'data' / 'uploads'
uploads.mkdir(parents=True)
(uploads / digest).write_bytes(content)
with Session.begin() as db:
    paper = Paper(subject_id=db.query(Subject).first().id, title='Recovery fixture', status='reference', file_hash=digest, filename='paper.txt')
    db.add(paper)
    db.flush()
    db.add(Question(paper_id=paper.id, number='Q1', text='Explain FCFS', marks=5, unit=1, topic_ids=[], confirmed=False))
    paper_id = paper.id
archive = root / 'backup.zip'
backup.create_backup(archive)
with Session.begin() as db:
    db.delete(db.get(Paper, paper_id))
(uploads / digest).unlink()
backup.restore_backup(archive)
with Session.begin() as db:
    restored = db.get(Paper, paper_id)
    assert restored and restored.questions[0].text == 'Explain FCFS'
    another = Paper(subject_id=restored.subject_id, title='Next paper', status='draft')
    db.add(another)
    db.flush()
    assert another.id > paper_id
assert (uploads / digest).read_bytes() == content

(uploads / digest).unlink()
missing = root / 'missing.zip'
try:
    backup.create_backup(missing)
except ValueError as error:
    assert 'missing' in str(error)
else:
    raise AssertionError('Backup accepted a missing referenced upload')
assert not missing.exists()
(uploads / digest).write_bytes(content)
(uploads / digest).write_bytes(b'changed')
bad_source = root / 'bad-source.zip'
try:
    backup.create_backup(bad_source)
except ValueError as error:
    assert 'hash' in str(error)
else:
    raise AssertionError('Backup accepted a changed stored upload')
assert not bad_source.exists()
(uploads / digest).write_bytes(content)

import zipfile
corrupt = root / 'corrupt.zip'
with zipfile.ZipFile(archive) as source, zipfile.ZipFile(corrupt, 'w') as target:
    for item in source.infolist():
        target.writestr(item.filename, b'changed' if item.filename == 'uploads/' + digest else source.read(item))
try:
    backup.restore_backup(corrupt)
except ValueError as error:
    assert 'hash' in str(error)
else:
    raise AssertionError('Changed upload was accepted')
assert (uploads / digest).read_bytes() == content
'''
            environment = {**os.environ, "DATABASE_URL": f"sqlite:///{directory}/test.db", "BACKUP_TEST_ROOT": directory, "EMBEDDING_MODEL_NAME": "", "AUTH_MODE": "local"}
            result = subprocess.run([sys.executable, "-c", script], cwd=Path(__file__).resolve().parents[1], env=environment, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
