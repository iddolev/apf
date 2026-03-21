"""
Logs Claude Code hook events to a JSONL file.
See: https://code.claude.com/docs/en/hooks.

Receives hook input as JSON on stdin.
"""
import json
import sys

from common import InvalidInputException, APF_FOLDER, KEY_log_claude_code_hook_event, config_key_to_log_filepath
from logger import Logger
from set_hooks_for_claude_code_event_logger import HooksInstaller


LOGFILE = config_key_to_log_filepath(KEY_log_claude_code_hook_event)

FIELD_DEFINITIONS = [
    {"name": "session_id",
     "value": True,
     "comment": "Unique identifier for the current conversation session"},
    {"name": "transcript_path",
     "value": False,
     "comment": "Path to the session's transcript JSONL file"},
    {"name": "cwd",
     "value": False,
     "comment": "Working directory at the time of the event"},
    {"name": "permission_mode",
     "value": False,
     "comment": "User's permission mode (e.g. acceptEdits)"},
    {"name": "agent_id",
     "value": True,
     "comment": "Unique identifier for this specific subagent invocation"},
    {"name": "agent_type",
     "value": True,
     "comment": "Agent type: general-purpose, Explore, Plan, or custom agent name"},
    {"name": "hook_event_name",
     "value": True,
     "comment": "SubagentStart or SubagentStop"},
    {"name": "stop_hook_active",
     "value": False,
     "comment": "Whether Claude is continuing as a result of a stop hook (SubagentStop only)"},
    {"name": "agent_transcript_path",
     "value": False,
     "comment": "Path to the agent's own transcript JSONL file (SubagentStop only)"},
    {"name": "last_assistant_message",
     "value": True,
     "comment": "The agent's final response text (SubagentStop only)"},
]


class ClaudeCodeHookLogger(Logger):
    def get_input(self) -> dict:
        # Information on the invoked hook is obtained from stdin in a JSON format
        if len(sys.argv) > 1:
            raise InvalidInputException(f"Invalid input: {sys.argv[1:]}")
        return json.load(sys.stdin)

    def install(self) -> None:
        super().install()
        HooksInstaller().install_hooks_in_settings_file()


if __name__ == "__main__":
    ClaudeCodeHookLogger(
        config_key=KEY_log_claude_code_hook_event,
        logfile=LOGFILE,
        field_definitions=FIELD_DEFINITIONS,
        sentinel_filepath=f"{APF_FOLDER}/.{KEY_log_claude_code_hook_event}",
    ).main()
