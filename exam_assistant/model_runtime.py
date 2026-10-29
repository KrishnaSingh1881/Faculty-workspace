"""Local Ollama adapter shared by the classifier's judge and helper models."""

import asyncio
import base64
import ipaddress
import json
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any
from uuid import uuid4
from urllib.parse import urlsplit

import httpx


MODEL_URL = os.getenv("MODEL_URL", "http://127.0.0.1:11434").rstrip("/")
JUDGE_MODEL = os.getenv("JUDGE_MODEL_NAME", os.getenv("MODEL_NAME", "gemma4:12b"))
HELPER_MODEL = os.getenv("HELPER_MODEL_NAME", JUDGE_MODEL)
OCR_MODEL = os.getenv("OCR_MODEL_NAME", "hf.co/PaddlePaddle/PaddleOCR-VL-1.6-GGUF")
MODEL = JUDGE_MODEL  # Kept for existing tagging, enrichment and chat callers.
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL_NAME", "qwen3-embedding:4b")
GPU_LOCK = asyncio.Lock()
GPU_LOCK_PATH = Path(__file__).resolve().parents[1] / "data" / "model-runtime.lock"


def _max_output_tokens() -> int:
    try:
        return min(8192, max(256, int(os.getenv("MODEL_MAX_OUTPUT_TOKENS", "2048"))))
    except ValueError:
        return 2048


def chat_context_tokens() -> int:
    try:
        return min(16384, max(4096, int(os.getenv("CHAT_CONTEXT_TOKENS", "8192"))))
    except ValueError:
        return 8192


def comparison_context_tokens() -> int:
    try:
        return min(16384, max(4096, int(os.getenv("COMPARISON_CONTEXT_TOKENS", "8192"))))
    except ValueError:
        return 8192


def _lock_file():
    """Acquire a cross-process advisory lock; the async lock handles same-loop callers."""
    GPU_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    handle = GPU_LOCK_PATH.open("a+b")
    if os.name == "nt":
        import msvcrt
        while True:
            try:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                return handle
            except OSError:
                time.sleep(0.1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        return handle


def _unlock_file(handle) -> None:
    if os.name == "nt":
        import msvcrt
        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    handle.close()


class ModelUnavailable(RuntimeError):
    """The configured local inference runtime could not complete a request."""


def _validate_local_endpoint() -> None:
    parsed = urlsplit(MODEL_URL)
    host = (parsed.hostname or "").casefold()
    if parsed.scheme not in {"http", "https"} or not host:
        raise ModelUnavailable("MODEL_URL must point to a local Ollama endpoint")
    try:
        address = ipaddress.ip_address(host)
        local = address.is_loopback or address.is_private or address.is_link_local
    except ValueError:
        local = host in {"localhost", "ollama"} or host.endswith((".localhost", ".local", ".internal"))
    if not local:
        raise ModelUnavailable("External model endpoints are disabled; use local Ollama or a private host")


def classifier_models_ready() -> bool:
    return bool(JUDGE_MODEL and HELPER_MODEL)


def classifier_model_status() -> dict[str, Any]:
    return {
        "configured": classifier_models_ready(),
        "judge_model": JUDGE_MODEL or None,
        "helper_model": HELPER_MODEL or None,
        "distinct_models": bool(JUDGE_MODEL and HELPER_MODEL and JUDGE_MODEL != HELPER_MODEL),
        "shared_model_roles": bool(JUDGE_MODEL and HELPER_MODEL and JUDGE_MODEL == HELPER_MODEL),
        "runtime": "local Ollama",
    }


async def chat_json(
    model: str,
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    keep_alive: str = "0",
    think: bool | None = None,
    num_ctx: int | None = None,
    on_event=None,
) -> dict:
    async with model_session():
        return await chat_json_in_session(model, messages, tools=tools, keep_alive=keep_alive, think=think, num_ctx=num_ctx, on_event=on_event)


async def chat_json_in_session(
    model: str,
    messages: list[dict],
    *,
    tools: list[dict] | None = None,
    keep_alive: str = "0",
    think: bool | None = None,
    num_ctx: int | None = None,
    on_event=None,
    format_json: bool = True,
) -> dict:
    """Call Ollama while the caller owns the shared model/GPU session lock."""
    if not model:
        raise ModelUnavailable("Configure both JUDGE_MODEL_NAME and HELPER_MODEL_NAME")
    _validate_local_endpoint()
    request: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": True,
        "options": {"temperature": 0, "num_predict": _max_output_tokens()},
        "keep_alive": keep_alive,
    }
    if num_ctx is not None:
        request["options"]["num_ctx"] = num_ctx
    if tools:
        request["tools"] = tools
    elif format_json:
        request["format"] = "json"
    if think is None and os.getenv("MODEL_THINKING", "auto").lower() in {"true", "false"}:
        think = os.environ["MODEL_THINKING"].lower() == "true"
    if think is not None:
        request["think"] = think
    request_id = uuid4().hex
    started = time.monotonic()
    message = {"role": "assistant", "content": "", "thinking": "", "tool_calls": []}
    pending = {"thinking": "", "content": ""}
    last_emit = started

    def flush():
        nonlocal last_emit
        if on_event:
            for field, value in pending.items():
                if value:
                    on_event({"event": field, "payload": {"text": value, "model": model, "request_id": request_id}})
        pending.update(thinking="", content="")
        last_emit = time.monotonic()

    try:
        async with httpx.AsyncClient(timeout=240, trust_env=False) as client:
            # Bound total wall time as well as idle reads; live chunks reset read timeouts.
            async with asyncio.timeout(900):
                async with client.stream("POST", f"{MODEL_URL}/api/chat", json=request) as response:
                    response.raise_for_status()
                    finished = False
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        body = json.loads(line)
                        if body.get("error"):
                            raise ModelUnavailable(str(body["error"]))
                        chunk = body.get("message", {})
                        if not isinstance(chunk, dict):
                            raise ModelUnavailable("Local model returned an invalid stream message")
                        for field in pending:
                            delta = chunk.get(field) or ""
                            if not isinstance(delta, str):
                                raise ModelUnavailable(f"Local model returned invalid {field}")
                            message[field] += delta
                            pending[field] += delta
                        calls = chunk.get("tool_calls") or []
                        if not isinstance(calls, list):
                            raise ModelUnavailable("Local model returned invalid tool calls")
                        message["tool_calls"].extend(calls)
                        if time.monotonic() - last_emit >= 0.35 or sum(map(len, pending.values())) >= 400:
                            flush()
                        if body.get("done"):
                            finished = True
                            flush()
                            if on_event:
                                on_event({"event": "model_finished", "payload": {
                                    "model": model, "request_id": request_id,
                                    "duration_ms": round((time.monotonic() - started) * 1000),
                                    "output_tokens": body.get("eval_count"), "done_reason": body.get("done_reason"),
                                }})
                            break
                    if not finished:
                        raise ModelUnavailable("Local model stream ended before its completion marker")
                    return {"message": message, "model": body.get("model", model)}
    except TimeoutError as exc:
        raise ModelUnavailable(f"Local model request exceeded 15 minutes ({model})") from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise ModelUnavailable(f"Local model request failed ({model}): {exc}") from exc


async def ocr_image_text_in_session(image: bytes, *, prompt: str = "OCR:") -> str:
    """Read one page while the caller owns the shared GPU lock."""
    if not OCR_MODEL:
        raise ModelUnavailable("Configure OCR_MODEL_NAME to use the local document model")
    _validate_local_endpoint()
    try:
        async with httpx.AsyncClient(timeout=300, trust_env=False) as client:
            response = await client.post(
                f"{MODEL_URL}/api/chat",
                json={
                    "model": OCR_MODEL,
                    "messages": [{"role": "user", "content": prompt, "images": [base64.b64encode(image).decode("ascii")]}],
                    "stream": False,
                    "options": {"temperature": 0},
                    "keep_alive": "5m",
                },
            )
            response.raise_for_status()
            message = response.json().get("message", {})
            content = message.get("content", "") if isinstance(message, dict) else ""
            if not isinstance(content, str) or not content.strip():
                raise ModelUnavailable("PaddleOCR-VL returned no extracted text")
            return content.strip()
    except (httpx.HTTPError, ValueError) as exc:
        raise ModelUnavailable(f"PaddleOCR-VL request failed: {exc}") from exc


@asynccontextmanager
async def ocr_session():
    """Keep PaddleOCR loaded across page batches, then release it before other model work."""
    async with model_session():
        await unload_model(JUDGE_MODEL)
        try:
            yield ocr_image_text_in_session
        finally:
            await unload_model(OCR_MODEL)


async def ocr_image_text(image: bytes, *, prompt: str = "OCR:") -> str:
    async with ocr_session() as read_page:
        return await read_page(image, prompt=prompt)


@asynccontextmanager
async def model_session():
    """Keep a model workload exclusive across threads and application processes."""
    async with GPU_LOCK:
        acquire = asyncio.create_task(asyncio.to_thread(_lock_file))
        try:
            handle = await asyncio.shield(acquire)
        except asyncio.CancelledError:
            # A thread blocked acquiring a lock cannot be canceled; wait for it and
            # release immediately so cancellation never strands the shared GPU.
            handle = await acquire
            await asyncio.to_thread(_unlock_file, handle)
            raise
        try:
            yield
        finally:
            await asyncio.to_thread(_unlock_file, handle)


async def model_json(messages: list[dict], *, on_event=None, think: bool | None = None) -> dict:
    """Compatibility adapter for non-comparison local model tasks."""
    result = await chat_json(JUDGE_MODEL, messages, keep_alive="5m", on_event=on_event, think=think)
    content = result["message"].get("content", "")
    try:
        parsed = json.loads(content)
    except (TypeError, ValueError) as exc:
        raise ModelUnavailable("Local model returned invalid JSON") from exc
    if not isinstance(parsed, dict):
        raise ModelUnavailable("Local model JSON response must be an object")
    return parsed


async def unload_model(model: str) -> None:
    """Ask local Ollama to release one model before switching the VRAM workload."""
    if not model:
        return
    _validate_local_endpoint()
    try:
        async with httpx.AsyncClient(timeout=60, trust_env=False) as client:
            response = await client.post(
                f"{MODEL_URL}/api/generate",
                json={"model": model, "prompt": "", "stream": False, "keep_alive": 0},
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise ModelUnavailable(f"Could not release local model {model}: {exc}") from exc


async def inspect_local_models() -> dict[str, Any]:
    """Inspect exact installed Ollama tags and distinguish model artifacts by digest."""
    configured = {"judge": JUDGE_MODEL, "helper": HELPER_MODEL, "ocr": OCR_MODEL, "embedding": EMBEDDING_MODEL}
    try:
        _validate_local_endpoint()
        async with httpx.AsyncClient(timeout=15, trust_env=False) as client:
            response = await client.get(f"{MODEL_URL}/api/tags")
            response.raise_for_status()
            body = response.json()
    except (httpx.HTTPError, ValueError, ModelUnavailable) as exc:
        return {"available": False, "error": str(exc), "configured": configured, "installed": []}
    entries = body.get("models", []) if isinstance(body, dict) else []
    installed = [item for item in entries if isinstance(item, dict) and isinstance(item.get("name", item.get("model")), str)]
    by_name = {item.get("name", item.get("model")): item for item in installed}

    def locate(tag: str) -> dict | None:
        if not tag:
            return None
        candidates = (tag, tag if ":" in tag.rsplit("/", 1)[-1] else f"{tag}:latest")
        for candidate in candidates:
            if candidate in by_name:
                item = by_name[candidate]
                return {"name": candidate, "digest": item.get("digest"), "size": item.get("size")}
        return None

    judge, helper, ocr = locate(JUDGE_MODEL), locate(HELPER_MODEL), locate(OCR_MODEL)
    embedding = locate(EMBEDDING_MODEL)
    distinct_artifacts = bool(judge and helper and (judge.get("digest") and helper.get("digest") and judge["digest"] != helper["digest"]))
    return {
        "available": True,
        "configured": configured,
        "installed": sorted(by_name),
        "judge": judge,
        "helper": helper,
        "ocr": ocr,
        "embedding": embedding,
        "embedding_installed": embedding is not None,
        "judge_installed": judge is not None,
        "helper_installed": helper is not None,
        "distinct_artifacts": distinct_artifacts,
        "roles_available": bool(judge and helper),
        "shared_artifact": bool(judge and helper and judge.get("digest") and judge.get("digest") == helper.get("digest")),
        "ocr_installed": ocr is not None,
    }
