"""Portable database and content-addressed upload backups."""

import argparse
import hashlib
import json
import os
import shutil
import stat
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from sqlalchemy import select, text

from .db import Base, ROOT, engine


FORMAT = "faculty-workspace-backup-v1"
MAX_BACKUP_BYTES = 5 * 1024 * 1024 * 1024


def create_backup(destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    connection = engine.connect()
    if engine.dialect.name == "postgresql":
        connection = connection.execution_options(isolation_level="REPEATABLE READ")
    with connection, connection.begin():
        tables = {}
        for table in Base.metadata.sorted_tables:
            tables[table.name] = [dict(row._mapping) for row in connection.execute(select(table))]
    manifest = {
        "format": FORMAT,
        "created_at": datetime.now().astimezone().isoformat(),
        "dialect": engine.dialect.name,
        "tables": tables,
    }
    required = {row["file_hash"] for name in ("papers", "materials", "syllabus_imports") for row in tables[name] if row.get("file_hash")}
    required.update(source["sha256"] for row in tables["templates"] if isinstance(row.get("definition"), dict) for source in [row["definition"].get("source")] if isinstance(source, dict) and source.get("sha256"))
    upload_root = ROOT / "data" / "uploads"
    with tempfile.NamedTemporaryFile(prefix=".workspace-backup-", suffix=".zip", dir=destination.parent, delete=False) as temporary:
        staged = Path(temporary.name)
    try:
        included = set()
        with zipfile.ZipFile(staged, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
            manifest_bytes = json.dumps(manifest, ensure_ascii=False, default=str, separators=(",", ":")).encode()
            if len(manifest_bytes) > MAX_BACKUP_BYTES:
                raise ValueError("Backup exceeds the 5 GB restore limit")
            archive.writestr("workspace.json", manifest_bytes)
            total_bytes = len(manifest_bytes)
            if upload_root.exists():
                for item in upload_root.iterdir():
                    if item.is_file() and not item.is_symlink() and len(item.name) == 64 and all(ch in "0123456789abcdef" for ch in item.name):
                        if len(included) >= 99_999 or total_bytes + item.stat().st_size > MAX_BACKUP_BYTES:
                            raise ValueError("Backup exceeds the 5 GB or 100,000-file restore limit")
                        digest = hashlib.sha256()
                        copied = 0
                        with item.open("rb") as source, archive.open(f"uploads/{item.name}", "w") as target:
                            while block := source.read(1024 * 1024):
                                copied += len(block)
                                if total_bytes + copied > MAX_BACKUP_BYTES:
                                    raise ValueError("Backup exceeds the 5 GB restore limit")
                                digest.update(block)
                                target.write(block)
                        if digest.hexdigest() != item.name:
                            raise ValueError(f"Stored upload hash does not match its content: {item.name}")
                        total_bytes += copied
                        included.add(item.name)
        missing = required - included
        if missing:
            raise ValueError(f"Backup is missing {len(missing)} referenced upload file(s)")
        os.replace(staged, destination)
    finally:
        staged.unlink(missing_ok=True)
    return destination


def restore_backup(source: Path) -> None:
    data_root = ROOT / "data"
    data_root.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="restore-uploads-", dir=data_root))
    upload_root = data_root / "uploads"
    previous = data_root / "uploads.restore-previous"
    swapped = False
    database_restored = False
    try:
        with zipfile.ZipFile(source) as archive:
            infos = archive.infolist()
            if len(infos) > 100_000 or sum(info.file_size for info in infos) > MAX_BACKUP_BYTES:
                raise ValueError("Backup exceeds the 5 GB or 100,000-file restore limit")
            for info in infos:
                mode = info.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise ValueError("Backup archives cannot contain symbolic links")
                if info.filename == "workspace.json":
                    continue
                parts = Path(info.filename).parts
                if len(parts) != 2 or parts[0] != "uploads" or len(parts[1]) != 64 or any(ch not in "0123456789abcdef" for ch in parts[1]):
                    raise ValueError(f"Unexpected backup archive path: {info.filename}")
                target = stage / parts[1]
                digest = hashlib.sha256()
                with archive.open(info) as reader, target.open("wb") as writer:
                    while block := reader.read(1024 * 1024):
                        digest.update(block)
                        writer.write(block)
                if digest.hexdigest() != parts[1]:
                    raise ValueError(f"Upload hash does not match its content: {parts[1]}")
            payload = json.loads(archive.read("workspace.json"))
        if not isinstance(payload, dict) or payload.get("format") != FORMAT or not isinstance(payload.get("tables"), dict):
            raise ValueError("This is not a supported faculty workspace backup")
        expected = {table.name for table in Base.metadata.sorted_tables}
        if set(payload["tables"]) != expected:
            raise ValueError("Backup database tables do not match this application version")
        for table in Base.metadata.sorted_tables:
            rows = payload["tables"][table.name]
            if not isinstance(rows, list) or any(not isinstance(row, dict) or set(row) != {column.name for column in table.columns} for row in rows):
                raise ValueError(f"Invalid rows in backup table {table.name}")
            for row in rows:
                for column in table.columns:
                    value = row.get(column.name)
                    if value is not None and column.type.python_type is datetime and isinstance(value, str):
                        row[column.name] = datetime.fromisoformat(value)
        if previous.exists():
            shutil.rmtree(previous)
        if upload_root.exists():
            os.replace(upload_root, previous)
        os.replace(stage, upload_root)
        swapped = True
        engine.dispose()
        with engine.begin() as connection:
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(table.delete())
            for table in Base.metadata.sorted_tables:
                rows = payload["tables"][table.name]
                if rows:
                    connection.execute(table.insert(), rows)
            if engine.dialect.name == "postgresql":
                for table in Base.metadata.sorted_tables:
                    if "id" in table.c and table.c.id.primary_key:
                        name = table.name.replace("'", "''")
                        connection.execute(text(f"SELECT setval(pg_get_serial_sequence('{name}', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM {table.name}"))
        database_restored = True
        if previous.exists():
            try:
                shutil.rmtree(previous)
            except OSError:
                pass
    except Exception:
        if swapped and not database_restored:
            if upload_root.exists():
                shutil.rmtree(upload_root)
            if previous.exists():
                os.replace(previous, upload_root)
        raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create or restore a faculty workspace backup")
    commands = parser.add_subparsers(dest="action", required=True)
    create = commands.add_parser("create", help="write a portable backup archive")
    create.add_argument("path", type=Path, nargs="?", default=Path("workspace-backup.zip"))
    restore = commands.add_parser("restore", help="replace the configured database and uploads")
    restore.add_argument("path", type=Path)
    args = parser.parse_args()
    if args.action == "create":
        create_backup(args.path)
        print(f"Created backup: {args.path}")
    else:
        restore_backup(args.path)
        print("Restored database and uploads. Restart the workspace service.")


if __name__ == "__main__":
    main()
