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

from ruamel.yaml import CommentedMap, YAML

LOGFILE = "tmp/logs/claude_code_hook_events_log.jsonl"
APF_INFO_FILENAME = ".apf.yaml"
CONFIG_KEY = "log_claude_code_events"
FIELD_INDENT = 4
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


_yaml = YAML()
_yaml.preserve_quotes = True


def _load_yaml(path: Path) -> CommentedMap:
    """Load .apf.yaml, preserving comments and formatting."""
    return _yaml.load(path.read_text(encoding="utf-8")) or {}


def load_config() -> tuple[bool, set[str]]:
    """Read log_claude_code_events section in .apf.yaml
    and return: a boolean whether logging is enabled,
    and the set of fields to include in the log."""
    path = Path(APF_INFO_FILENAME)
    if not path.exists():
        raise FileNotFoundError(".apf.yaml")
    data = _load_yaml(path).get(CONFIG_KEY)
    if not data:
        return False, set()
    is_enabled = data.get('enabled', False)
    fields = data.get('fields', {})
    enabled_fields = {name for name, enabled in fields.items() if enabled is True}
    return is_enabled, enabled_fields


def _add_field(fields_map: CommentedMap, name: str, default: bool, comment: str) -> None:
    """Add a field to a ruamel.yaml CommentedMap with a comment above."""
    fields_map[name] = default
    fields_map.yaml_set_comment_before_after_key(name, before=comment, indent=FIELD_INDENT)


def install(apf_yaml_path: Path | None = None) -> None:
    # `apf_yaml_path` is used for testing
    path = apf_yaml_path or Path(APF_INFO_FILENAME)
    config = _load_yaml(path)
    existing = config.get(CONFIG_KEY)

    if not existing:
        fields_map = CommentedMap()
        for name, default, comment in FIELD_DEFINITIONS:
            _add_field(fields_map, name, default, comment)
        config[CONFIG_KEY] = CommentedMap([
            ("enabled", False),
            ("fields", fields_map),
        ])
    else:
        fields_map = existing.get("fields")
        if not isinstance(fields_map, dict):
            raise ValueError(f"'fields' is missing or corrupt in {APF_INFO_FILENAME}")
        fields_map_keys = set(fields_map.keys())
        missing = [(n, d, c) for n, d, c in FIELD_DEFINITIONS if n not in fields_map_keys]
        if not missing:
            return
        for name, default, comment in missing:
            _add_field(fields_map, name, default, comment)

    with open(path, "w", encoding="utf-8") as f:
        _yaml.dump(config, f)


def log_event() -> None:
    """If log_claude_code_events is enabled in .apf.yaml, add a line to the log file."""
    is_enabled, enabled_fields = load_config()
    if not is_enabled:
        return

    # Data of Claude Code's event
    try:
        data: dict = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"log_hook_event: failed to parse JSON from stdin: {e}", file=sys.stderr)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"timestamp": timestamp}
    record.update({k: v for k, v in data.items() if k in enabled_fields})

    # Create folder if does not exist
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def status() -> str:
    """Return 'enabled' or 'disabled' based on .apf.yaml."""
    try:
        is_enabled, _ = load_config()
        return "enabled" if is_enabled else "disabled"
    except FileNotFoundError:
        return "disabled"


def main() -> None:
    if "--status" in sys.argv:
        print(status())
    elif "--install" in sys.argv:
        install()
    else:
        log_event()


if __name__ == '__main__':
    main()
