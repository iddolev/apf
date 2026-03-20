"""
Installs the hook event logger into a project's .claude/settings.json.

For each known hook type, ensures an entry exists that runs log_claude_code_hook_event.py.
Loads the existing settings.json, merges in the hook entries (preserving any
existing hooks), and writes it back.

Usage:
    python .claude/scripts/apf/install_claude_code_hook_event_logger.py
"""

import json
import os

from common import APF_FOLDER

SETTINGS_PATH = ".claude/settings.json"
SENTINEL_FILE = f"{APF_FOLDER}/.log_claude_code_hook_event"
# The code in HOOK_COMMAND reaches activation of python only if SENTINEL_FILE exists
# and its content is "on".
# This is intended to prevent expensive invocation of python when SENTINEL_FILE has "off" or is missing
HOOK_COMMAND = f"findstr /x \"on\" {SENTINEL_FILE} >nul 2>&1 && python .claude/scripts/apf/log_claude_code_hook_event.py"

HOOK_TYPES = [
    "ConfigChange",
    "InstructionsLoaded",
    "Notification",
    "PermissionRequest",
    "PostToolUse",
    "PostToolUseFailure",
    "PreCompact",
    "PreToolUse",
    "SessionEnd",
    "SessionStart",
    "Stop",
    "SubagentStart",
    "SubagentStop",
    "TaskCompleted",
    "TeammateIdle",
    "UserPromptSubmit",
    "WorktreeCreate",
    "WorktreeRemove",
]

"""
Background info to help understand HOOK_ENTRY below:
The schema of settings.json of Claude Code has a top-level keyword "hooks" with:
"hooks": {
    <hook_type>: [
        {
            "matcher": <expression>
            "hooks": [
                {
                    "type": "command",
                    "command": <actual_command>
                }
            ]
        },
        { ... }
    ],
    <hook_type2>: [ ... ]
}
For more info, see: https://code.claude.com/docs/en/hooks
"""

HOOK_ENTRY = {
    # not mentioning a matcher on the next line is the same as "*" i.e. match everything
    # "matcher": "*"
    "hooks": [
        {
            "type": "command",
            "command": HOOK_COMMAND,
        }
    ]
}


def load_settings() -> dict:
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_settings(settings: dict) -> None:
    os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")


def hook_already_installed(hook_list: list) -> bool:
    """Check if any entry in the hook list already runs our command."""
    return any(hook.get("command") == HOOK_COMMAND
               for entry in hook_list
               for hook in entry.get("hooks", []))


def install_hooks_in_settings() -> None:
    settings = load_settings()
    hooks = settings.setdefault("hooks", {})
    added = []

    for hook_type in HOOK_TYPES:
        existing = hooks.get(hook_type, [])
        if not hook_already_installed(existing):
            existing.append(HOOK_ENTRY)
            hooks[hook_type] = existing
            added.append(hook_type)

    if added:
        save_settings(settings)
        print(f"Installed hook event logger for {len(added)} hook type(s): {', '.join(added)}")
    else:
        print("Hook event logger already installed for all hook types.")
