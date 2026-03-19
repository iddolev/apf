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


APF_INFO_FILE = ".apf.yaml"
KEY_log_claude_code_events = "log_claude_code_events"
SETTINGS_PATH = ".claude/settings.json"
HOOK_COMMAND = "python .claude/scripts/apf/log_claude_code_hook_event.py"

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

HOOK_ENTRY = {
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


def install_in_apf_yaml() -> None:
    # TODO: if no key claude_code_hook_event_logger in APF_INFO_FILE then add:
    data = {}
    if KEY_log_claude_code_events not in data.keys():
        data[KEY_log_claude_code_events] = {'enabled': False}



def install_in_settings_json() -> None:
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


def install() -> None:
    install_in_apf_yaml()
    install_in_settings_json()


if __name__ == "__main__":
    install()
