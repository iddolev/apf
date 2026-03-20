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

from common import APF_FOLDER, KEY_log_claude_code_hook_events


SETTINGS_PATH = ".claude/settings.json"
SENTINEL_FILE = f"{APF_FOLDER}/.log_claude_code_hook_event"
# The code in HOOK_COMMAND reaches activation of python only if SENTINEL_FILE exists and its content is "on".
# This is intended to prevent expensive invocation of python when SENTINEL_FILE has "off" or is missing.
# The part "|| exist 0" means that if logging is not enabled, exit with code 0 and not error.
HOOK_COMMAND = f"findstr /x \"on\" {SENTINEL_FILE} >nul 2>&1 || exit 0 && python .claude/scripts/apf/log_claude_code_hook_event.py"

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


LEGACY_SENTINEL = KEY_log_claude_code_hook_events


def divide_entries_of_hook(entries: list) -> tuple[list, list, list]:
    # Each entry in `entries` has the format:
    # {
    #     "match": <expr>    -- optional
    #     "hooks": [
    #         {
    #             "type": "command"
    #             "command": <command>
    #         }
    #     ]
    # }
    exact = []
    related = []
    unrelated = []
    for entry in entries:
        hooks_of_entry = entry.get("hooks", [])
        if any(h.get("command") == HOOK_COMMAND for h in hooks_of_entry):
            exact.append(entry)
        elif any(LEGACY_SENTINEL in h.get("command", "") for h in hooks_of_entry):
            # This is a previous version of the command - it should be removed
            related.append(entry)
        else:
            unrelated.append(entry)
    return exact, related, unrelated


def install_hooks_in_settings() -> None:
    settings = load_settings()
    hooks = settings.setdefault("hooks", {})
    existing = []
    added = []
    removed = []
    total_removed_commands = 0

    for hook_type in HOOK_TYPES:
        entries = hooks.get(hook_type, [])
        exact, related, unrelated = divide_entries_of_hook(entries)
        cleaned = unrelated + exact
        if exact:
            existing.append(hook_type)
        else:
            cleaned.append(HOOK_ENTRY)
            added.append(hook_type)
        if related:
            # This is a previous version of the command - it should be removed
            total_removed_commands += len(related)
            removed.append(hook_type)
        hooks[hook_type] = cleaned

    if added or removed:
        # At least one entry was added or removed, so need to save the modifications
        save_settings(settings)

    if removed:
        print(f"Removed {total_removed_commands} legacy command(s) "
              f"in {len(removed)} hook type(s): {', '.join(removed)}.")
    if existing:
        if len(existing) == len(HOOK_TYPES):
            print("Hook event logger already installed for all hook types.")
        else:
            print(f"The command was already installed for {len(existing)} hook type(s): {', '.join(existing)}.")
    if added:
        print(f"Installed hook event logger for {len(added)} hook type(s): {', '.join(added)}.")
    else:
        print("No command was added for any hook type.")
