"""
Logs Claude Code events to a JSONL file.

Receives hook input as JSON on stdin.
"""

import json
import re
import sys
from datetime import datetime, timezone
from typing import Optional

LOGFILE = "sandbox/tmp/claude-code-events.jsonl"
FIELDS_TO_INCLUDE = {
    # Unique identifier for the current conversation session
    "session_id": True,
    # Path to the session's transcript JSONL file
    "transcript_path": False,
    # Working directory when the agent was spawned
    "cwd": False,
    # User's permission mode (e.g. "acceptEdits")
    "permission_mode": False,
    # Unique identifier for this specific subagent invocation
    "agent_id": True,
    # Agent type: "general-purpose", "Explore", "Plan", or custom agent name
    "agent_type": True,
    # "SubagentStart" or "SubagentStop"
    "hook_event_name": True,
    # Whether Claude is continuing as a result of a stop hook (SubagentStop only)
    "stop_hook_active": False,
    # Path to the subagent's own transcript JSONL file (SubagentStop only)
    "agent_transcript_path": False,
    # The subagent's final response text (SubagentStop only)
    "last_assistant_message": True,
}

data: dict = json.load(sys.stdin)
record = {k: data[k] for k, include in FIELDS_TO_INCLUDE.items() if include and k in data}

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Temporarily try for debugging:
record = {}
record["_timestamp_"] = timestamp
exclude_fields = {"session_id", "transcript_path", "cwd"}
record.update({k: v for k, v in data.items() if k not in exclude_fields})

with open(LOGFILE, "a", encoding="utf-8") as f:
    f.write(json.dumps(record, ensure_ascii=False) + "\n")


_AGENT_NAME_PATTERN = re.compile(r"Run:?\s+([\w-]+)")


def _extract_agent_name(text: str) -> Optional[str]:
    """Extract agent name from a TaskCreate subject like 'Run demo2-agent (first invocation)'."""
    match = _AGENT_NAME_PATTERN.match(text)
    return match.group(1) if match else None


meaningful_event = {"timestamp": timestamp}
errors = []
if data.get("tool_name") == "Agent":
    # This catches the high level request of the user from Claude Code
    if "tool_input" not in data.keys():
        errors.append("tool_name=='Agent' but 'tool_input' is not in data")
    elif not isinstance(data["tool_input"], dict):
        errors.append("tool_name=='Agent' but 'tool_input' is not in a dict")
    else:
        tool_input = data["tool_input"]
        fields = [
            ("subagent_type", "agent_name"),
            ("description", "description"),
            ("prompt", "prompt"),
        ]
        for f1, f2 in fields:
            if f1 in tool_input.keys():
                meaningful_event[f2] = tool_input[f1]
            else:
                errors.append(f"'{f1}' not in tool_input")
elif data.get("tool_name") == "TaskCreate" and data.get("hook_event_name") == "PostToolUse":
    tool_input_subject = data.get("tool_input", {}).get("subject")
    if tool_input_subject:
        meaningful_event["agent_name"] = _extract_agent_name(tool_input_subject)
    else:
        errors.append("tool_name=='TaskCreate' but tool_input.subject is empty")
    fields = ["permission_mode", "tool_input", "tool_response"]
    meaningful_event.update({f: data[f] for f in fields})

