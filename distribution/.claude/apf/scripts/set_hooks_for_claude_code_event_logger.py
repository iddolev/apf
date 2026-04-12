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

from common import KEY_log_claude_code_hook_event, APF_FOLDER


SETTINGS_PATH = ".claude/settings.json"
SENTINEL_FILEPATH = f"{APF_FOLDER}/.{KEY_log_claude_code_hook_event}"
# The code in HOOK_COMMAND activates a .bat script instead of python log_claude_code_hook_event.py
# to prevent expensive invocation of python when SENTINEL_FILENAME has "off" or is missing.
# Only when logging is enabled, the python script is invoked.
HOOK_COMMAND = fr".claude\\scripts\\apf\\{KEY_log_claude_code_hook_event}.bat"

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


LEGACY_DETECTOR = KEY_log_claude_code_hook_event


class HooksInstaller:
    def __init__(self, field_indent: int = 2):
        self._field_indent = field_indent
        self._settings: dict | None = None
        self._hooks: dict | None = None
        self._existing = []
        self._added = []
        self._removed = []
        self._total_removed_commands = 0

    def _load_settings(self) -> None:
        if os.path.exists(SETTINGS_PATH):
            with open(SETTINGS_PATH, encoding="utf-8") as f:
                self._settings = json.load(f)
        else:
            self._settings = {}

    def _save_settings(self) -> None:
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(self._settings, f, indent=self._field_indent, ensure_ascii=False)
            f.write("\n")

    @staticmethod
    def _divide_entries_of_hook(entries: list) -> tuple[list, list, list]:
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
            elif any(LEGACY_DETECTOR in h.get("command", "") for h in hooks_of_entry):
                # This is a previous version of the command - it should be removed
                related.append(entry)
            else:
                unrelated.append(entry)
        return exact, related, unrelated

    def _process_hook_type(self, hook_type: str) -> None:
        entries = self._hooks.get(hook_type, [])
        exact, related, unrelated = self._divide_entries_of_hook(entries)
        cleaned = unrelated + exact
        if exact:
            self._existing.append(hook_type)
        else:
            cleaned.append(HOOK_ENTRY)
            self._added.append(hook_type)
        if related:
            # This is a previous version of the command - it should be removed
            self._total_removed_commands += len(related)
            self._removed.append(hook_type)
        self._hooks[hook_type] = cleaned

    def _print_summary(self) -> None:
        if self._removed:
            print(f"Removed {self._total_removed_commands} legacy command(s) "
                  f"in {len(self._removed)} hook type(s): {', '.join(self._removed)}.")
        if self._existing:
            if len(self._existing) == len(HOOK_TYPES):
                print("Hook event logger already installed for all hook types.")
            else:
                print(f"The command was already installed for {len(self._existing)} hook type(s): {', '.join(self._existing)}.")
        if self._added:
            print(f"Installed hook event logger for {len(self._added)} hook type(s): {', '.join(self._added)}.")
        else:
            print("No command was added for any hook type.")

    def install_hooks_in_settings_file(self) -> None:
        self._load_settings()
        self._hooks = self._settings.setdefault("hooks", {})
        for hook_type in HOOK_TYPES:
            self._process_hook_type(hook_type)
        if self._added or self._removed:
            # At least one entry was added or removed, so need to save the modifications
            self._save_settings()
        self._print_summary()
