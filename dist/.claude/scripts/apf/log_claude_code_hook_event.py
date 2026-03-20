"""
Logs Claude Code hook events to a JSONL file.
See: https://code.claude.com/docs/en/hooks.

Receives hook input as JSON on stdin.
"""
import json
import sys

from common import InvalidInputException, APF_FOLDER, KEY_log_claude_code_hook_events
from logger import Logger
from set_hooks_for_claude_code_event_logger import install_hooks_in_settings


LOGFILE = f"logs/{KEY_log_claude_code_hook_events}.jsonl"
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
            raise InvalidInputException(f"Invalid input: {sys.argv[1:]}")
        return json.load(sys.stdin)

    def install(self) -> None:
        super().install()
        install_hooks_in_settings()


CLAUDE_CODE_HOOK_EVENT_LOGGER = ClaudeCodeHookLogger(
        config_key=KEY_log_claude_code_hook_events,
        logfile=LOGFILE,
        field_definitions=FIELD_DEFINITIONS,
        sentinel_filepath=f"{APF_FOLDER}/.{KEY_log_claude_code_hook_events}")


if __name__ == "__main__":
    CLAUDE_CODE_HOOK_EVENT_LOGGER.main()
