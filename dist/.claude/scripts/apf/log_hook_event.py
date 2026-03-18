"""
Logs Claude Code hook events to a JSONL file.
See: https://code.claude.com/docs/en/hooks.

Receives hook input as JSON on stdin.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


LOGFILE = "tmp/logs/claude_code_hook_events_log.jsonl"
APF_INFO_FILENAME = ".apf.yaml"


# Doing this with a string and not a dict so that the comments are also written to the yaml file
INITIAL_LOG_CLAUDE_CODE_EVENTS = {
    "enabled": False,
    "fields": [
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
}

CONFIG_KEY_OF_LOG_CLAUDE_CODE_EVENTS = "log_claude_code_events"
INDENT = " " * 4


def load_config() -> tuple[bool, set[str]]:
    """Read log_claude_code_events section in .apf.yaml
    and return: a boolean whether logging is enabled,
    and the set of fields to include in the log."""
    path = Path(APF_INFO_FILENAME)
    if not path.exists():
        raise FileNotFoundError(".apf.yaml")
    config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data = config.get("log_claude_code_events")
    if not data:
        return False, set()
    is_enabled = data.get('enabled', False)
    fields = data.get('fields', {})
    enabled_fields = {name for name, field_enabled in fields.items() if field_enabled is True}
    return is_enabled, enabled_fields


def _render_field(entry: tuple[str, bool, str]) -> str:
    """Render a single field entry."""
    return f'{INDENT}# {entry[2]}\n{INDENT}{entry[0]}: {entry[1]}'


def install() -> None:
    path = Path(APF_INFO_FILENAME)
    content = path.read_text(encoding="utf-8")
    config = yaml.safe_load(content) or {}
    existing = config.get(CONFIG_KEY_OF_LOG_CLAUDE_CODE_EVENTS)
    fields = INITIAL_LOG_CLAUDE_CODE_EVENTS["fields"]

    if not existing:
        # Append the entire section
        lines = ["",
                 "log_claude_code_events:",
                 f"  enabled: {str(INITIAL_LOG_CLAUDE_CODE_EVENTS['enabled']).lower()}",
                 "  fields:"]
        lines.extend(_render_field(entry) for entry in fields)
        content = content.rstrip() + "\n" + "\n".join(lines) + "\n"
    else:
        # Add only missing fields
        existing_fields_dict = existing.get("fields")
        if not isinstance(existing_fields_dict, dict):
            raise ValueError(f"'fields' is missing or corrupt in {APF_INFO_FILENAME}")
        existing_fields = set(existing_fields_dict.keys())
        missing = [e for e in fields if e[0] not in existing_fields]
        if not missing:
            return
        # Append missing fields at the end of the fields section
        addition = "\n".join(_render_field(e) for e in missing)
        content = content.rstrip() + "\n" + addition + "\n"

    path.write_text(content, encoding="utf-8")


def log_event() -> None:
    """If log_claude_code_events is enabled in .apf.config, add a line to the log file"""
    is_enabled, enabled_fields = load_config()
    if not is_enabled:
        return

    # Data of Claude Code's event
    data: dict = json.load(sys.stdin)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"timestamp": timestamp}
    record.update({k: v for k, v in data.items() if k in enabled_fields})

    # Create folder if does not exist
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    if "--install" in sys.argv:
        install()
    else:
        log_event()


if __name__ == '__main__':
    main()
