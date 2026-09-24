"""The agent loop main.py calls: pydantic-ai over gpt-6-astra through Portkey."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic_ai import Agent, NativeToolCallPart, ToolCallPart
from pydantic_ai.capabilities import NativeTool
from pydantic_ai.messages import ModelResponse, ThinkingPart, ToolReturnPart
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import AgentResult
from tools import build_web_search_tool, search_courses

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# The .env may sit in this Lecture 7 folder or one level up (e.g. MGT409/.env).
load_dotenv(ROOT / ".env")
load_dotenv(ROOT.parent / ".env")

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-6-astra")
PORTKEY_BASE_URL = os.getenv("PORTKEY_BASE_URL", "https://api.portkey.ai/v1")

PROMPT_PATH = ROOT / "prompts" / "prompt.md"
AUDIT_PATH = ROOT / "output" / "audit_trail.json"

MAX_RESULT_CHARS = 400


def load_system_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def build_agent() -> Agent[None, str]:
    """Build the agent once and reuse it across requests."""
    api_key = os.getenv("PORTKEY_API_KEY")
    if not api_key:
        raise RuntimeError(
            "PORTKEY_API_KEY is not set. Put it in Lecture 7/.env or the parent folder's .env."
        )

    provider = OpenAIProvider(base_url=PORTKEY_BASE_URL, api_key=api_key)
    model = OpenAIResponsesModel(MODEL_NAME, provider=provider)

    return Agent(
        model,
        instructions=load_system_prompt(),
        tools=[search_courses],
        capabilities=[NativeTool(build_web_search_tool())],
    )


def _short(value: Any) -> str:
    """Trim a tool result down to something worth keeping in the audit trail."""
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    if len(text) > MAX_RESULT_CHARS:
        return text[:MAX_RESULT_CHARS] + f"... [{len(text)} chars total]"
    return text


def _tool_label(part: ToolCallPart | NativeToolCallPart) -> str:
    """Report OpenAI's hosted search under the name the prompt uses."""
    name = part.tool_name
    if isinstance(part, NativeToolCallPart) and "search" in name:
        return "web_search"
    return name


def _walk(messages: list[Any]) -> tuple[list[str], list[str], list[dict[str, Any]], str]:
    """Pull tool names, thoughts, per-call detail and a stop reason out of a run."""
    tools_used: list[str] = []
    thoughts: list[str] = []
    calls: dict[str, dict[str, Any]] = {}
    ordered: list[dict[str, Any]] = []
    finish_reason = "unknown"

    for message in messages:
        for part in getattr(message, "parts", []):
            if isinstance(part, ThinkingPart) and part.content:
                thoughts.append(part.content)
            elif isinstance(part, (ToolCallPart, NativeToolCallPart)):
                label = _tool_label(part)
                if label not in tools_used:
                    tools_used.append(label)
                entry: dict[str, Any] = {
                    "tool": label,
                    "args": _short(part.args),
                    "result": None,
                }
                ordered.append(entry)
                if part.tool_call_id:
                    calls[part.tool_call_id] = entry
            elif isinstance(part, ToolReturnPart):
                entry = calls.get(part.tool_call_id or "")
                if entry is not None:
                    entry["result"] = _short(part.content)
        if isinstance(message, ModelResponse):
            finish_reason = str(getattr(message, "finish_reason", None) or finish_reason)

    return tools_used, thoughts, ordered, finish_reason


def append_audit(entry: dict[str, Any]) -> None:
    """Append one run to output/audit_trail.json without dropping earlier rows."""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    rows: list[Any] = []
    if AUDIT_PATH.exists():
        try:
            existing = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
            if isinstance(existing, list):
                rows = existing
        except json.JSONDecodeError:
            # A corrupt file must not cost us the new row, nor silently vanish.
            AUDIT_PATH.rename(AUDIT_PATH.with_suffix(".corrupt.json"))
    rows.append(entry)
    AUDIT_PATH.write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")


def run_agent(message: str) -> dict:
    """Answer one user message. Returns {"reply": str, "tools_used": list[str]}."""
    started = datetime.now(timezone.utc).isoformat()
    agent = build_agent()

    try:
        run = agent.run_sync(message)
    except Exception as exc:  # surfaced to the user rather than a blank 500
        append_audit(
            {
                "time": started,
                "user_message": message,
                "thoughts": [],
                "tool_calls": [],
                "stopped_because": f"error: {type(exc).__name__}: {exc}",
                "reply": "",
            }
        )
        raise

    tools_used, thoughts, calls, finish_reason = _walk(list(run.all_messages()))
    reply = run.output if isinstance(run.output, str) else str(run.output)

    append_audit(
        {
            "time": started,
            "user_message": message,
            "model": MODEL_NAME,
            "thoughts": thoughts,
            "tool_calls": calls,
            "tools_used": tools_used,
            "stopped_because": finish_reason,
            "reply": reply,
        }
    )

    return AgentResult(reply=reply, tools_used=tools_used).model_dump()
