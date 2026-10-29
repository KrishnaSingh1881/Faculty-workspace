"""Request-local activity delivery and SSE framing."""

import json
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Callable

activity_sink: ContextVar[Callable[[dict], None] | None] = ContextVar("activity_sink", default=None)


def publish(event: dict) -> None:
    sink = activity_sink.get()
    if sink:
        sink({"created_at": datetime.now(timezone.utc).isoformat(), **event})


def sse(event: str, data, event_id: int | None = None) -> str:
    prefix = f"id: {event_id}\n" if event_id is not None else ""
    return prefix + f"event: {event}\ndata: " + json.dumps(data, ensure_ascii=False, default=str) + "\n\n"


def collect(records: list[dict], event: dict) -> None:
    """Join adjacent deltas for compact saved conversations; preserve every tool event."""
    record = {"created_at": datetime.now(timezone.utc).isoformat(), **event}
    if records and event.get("event") in {"thinking", "content"}:
        previous = records[-1]
        if (previous.get("event"), previous.get("agent"), previous.get("payload", {}).get("request_id")) == (
            event.get("event"), event.get("agent"), event.get("payload", {}).get("request_id")
        ):
            previous["payload"]["text"] += event["payload"].get("text", "")
            return
    records.append({**record, "payload": dict(record.get("payload", {}))})
