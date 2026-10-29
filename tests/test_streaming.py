"""Exercise the real stream parser and bounded tool recovery without model inference."""

import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch

import httpx

from exam_assistant.comparison_agents import run_tool_agent
from exam_assistant.model_runtime import ModelUnavailable, chat_json_in_session


class StreamingTest(unittest.TestCase):
    def test_comparison_context_setting_is_bounded(self):
        import os
        from exam_assistant.model_runtime import comparison_context_tokens

        with patch.dict(os.environ, {"COMPARISON_CONTEXT_TOKENS": "8192"}):
            self.assertEqual(comparison_context_tokens(), 8192)
        with patch.dict(os.environ, {"COMPARISON_CONTEXT_TOKENS": "999999"}):
            self.assertEqual(comparison_context_tokens(), 16384)

    def test_ollama_thinking_content_and_tool_events(self):
        chunks = [
            {"message": {"thinking": "Check the "}},
            {"message": {"thinking": "question’s scope."}},
            {"message": {"content": '{"answer":"'}},
            {"message": {"content": 'Done"}', "tool_calls": [{"function": {"name": "lookup", "arguments": {}}}]}},
            {"done": True, "done_reason": "stop", "eval_count": 12},
        ]
        events = []
        original_client = httpx.AsyncClient

        def handle(request):
            self.assertTrue(json.loads(request.content)["stream"])
            return httpx.Response(200, content="\n".join(json.dumps(chunk) for chunk in chunks))

        async def run():
            with patch("exam_assistant.model_runtime.httpx.AsyncClient", side_effect=lambda **kwargs: original_client(transport=httpx.MockTransport(handle), **kwargs)):
                response = await chat_json_in_session("test-local", [], on_event=events.append)
            self.assertEqual(response["message"]["thinking"], "Check the question’s scope.")
            self.assertEqual(json.loads(response["message"]["content"]), {"answer": "Done"})
            self.assertEqual(len(response["message"]["tool_calls"]), 1)
            self.assertEqual([event["event"] for event in events], ["thinking", "content", "model_finished"])

        asyncio.run(run())

    def test_repair_is_bounded_and_does_not_reexecute_actions(self):
        async def run():
            mutations = []
            responses = [
                {"message": {"tool_calls": [{"function": {"name": "save", "arguments": {"id": 7}}}]}},
                {"message": {"content": "invalid JSON"}},
                {"message": {"content": '{"answer":"Saved"}'}},
            ]
            with patch("exam_assistant.comparison_agents.chat_json_in_session", new=AsyncMock(side_effect=responses)) as model:
                result, trace, used = await run_tool_agent(model="test", system="test", payload={}, registry={"save": lambda args: mutations.append(args) or {"success": True}})
            self.assertEqual(result["answer"], "Saved")
            self.assertEqual(mutations, [{"id": 7}])
            self.assertEqual(len(trace), 1)
            self.assertEqual(used, ["save"])
            self.assertIsNone(model.call_args.kwargs["tools"])
            with patch("exam_assistant.comparison_agents.chat_json_in_session", new=AsyncMock(return_value={"message": {"content": "invalid"}})) as model:
                with self.assertRaises(ModelUnavailable):
                    await run_tool_agent(model="test", system="test", payload={}, registry={}, require_tool_call=False)
                self.assertEqual(model.await_count, 2)

        asyncio.run(run())

    def test_required_comparison_checks_are_requested_before_final_answer(self):
        async def run():
            calls = []
            responses = [
                {"message": {"tool_calls": [{"function": {"name": "compare", "arguments": {}}}]}},
                {"message": {"content": "premature answer"}},
                {"message": {"tool_calls": [
                    {"function": {"name": "compound", "arguments": {}}},
                    {"function": {"name": "matrix", "arguments": {}}},
                ]}},
                {"message": {"content": '{"label":"review"}'}},
            ]
            registry = {name: (lambda args, name=name: calls.append(name) or {"ok": True})
                        for name in ("compare", "compound", "matrix")}
            with patch("exam_assistant.comparison_agents.chat_json_in_session", new=AsyncMock(side_effect=responses)) as model:
                result, _, used = await run_tool_agent(
                    model="test", system="test", payload={}, registry=registry,
                    required_tools={"compare", "compound", "matrix"},
                )
            self.assertEqual(result["label"], "review")
            self.assertCountEqual(calls, ["compare", "compound", "matrix"])
            self.assertCountEqual(used, ["compare", "compound", "matrix"])
            self.assertTrue(any(
                "compound, matrix" in message.get("content", "")
                for message in model.await_args_list[2].args[1]
                if message.get("role") == "user"
            ))

        asyncio.run(run())

    def test_failed_required_tool_is_retried_before_final_answer(self):
        async def run():
            outcomes = iter([{"error": "temporary validation failure"}, {"ok": True}])
            responses = [
                {"message": {"tool_calls": [{"function": {"name": "check", "arguments": {}}}]}},
                {"message": {"content": "premature answer"}},
                {"message": {"tool_calls": [{"function": {"name": "check", "arguments": {}}}]}},
                {"message": {"content": '{"ok":true}'}},
            ]
            with patch("exam_assistant.comparison_agents.chat_json_in_session", new=AsyncMock(side_effect=responses)) as model:
                result, trace, _ = await run_tool_agent(
                    model="test", system="test", payload={}, registry={"check": lambda _: next(outcomes)},
                    required_tools={"check"},
                )
            self.assertTrue(result["ok"])
            self.assertEqual([item["result"] for item in trace], [{"error": "temporary validation failure"}, {"ok": True}])
            self.assertTrue(any(
                "check" in message.get("content", "")
                for message in model.await_args_list[2].args[1]
                if message.get("role") == "user"
            ))

        asyncio.run(run())
