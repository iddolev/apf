"""
Logs Claude Code hook events to a JSONL file.
See: https://code.claude.com/docs/en/hooks.

Receives hook input as JSON on stdin.
"""
import json
import sys

from logger import Logger


KEY_log_claude_code_events = "log_claude_code_events"
LOGFILE = "tmp/logs/claude_code_hook_events_log.jsonl"
FIELD_DEFINITIONS = [
    ("session_id", True, "Unique identifier for the current conversation session"),
    ("transcript_path", False, "Path to the session's transcript JSONL file"),
    ("cwd", False, "Working directory at the time of the event"),
    ("permission_mode", False, "User's permission mode (e.g. acceptEdits)"),
    ("agent_id", True, "Unique identifier for this specific subagent invocation"),
    ("agent_type", True, "Agent type: general-purpose, Explore, Plan, or custom agent name"),
    ("hook_event_name", True, "SubagentStart or SubagentStop"),
    ("stop_hook_active", False, "Whether Claude is continuing as a result of a stop hook (SubagentStop only)"),
    ("agent_transcript_path", False, "Path to the agent's own transcript JSONL file (SubagentStop only)"),
    ("last_assistant_message", True, "The agent's final response text (SubagentStop only)"),
]


class ClaudeCodeHookLogger(Logger):
    def get_input(self) -> dict:
        if len(sys.argv) > 1:
            raise ValueError(f"Invalid input: {sys.argv[1:]}")
        try:
            data: dict = json.load(sys.stdin)
            return data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"log_hook_event: failed to parse JSON from stdin: {e}", file=sys.stderr)


if __name__ == "__main__":
    _logger = ClaudeCodeHookLogger(
        config_key=KEY_log_claude_code_events,
        logfile=LOGFILE,
        field_definitions=FIELD_DEFINITIONS)
    _logger.main()
