"""
Configurable JSONL event logger backed by .apf.yaml.

Provides status/install/on/off management and field-filtered event logging.
Instantiate with a key from a config yaml, log file path, and field definitions,
then call methods or wire up main() to sys.argv.
"""

import json
import os
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from ruamel.yaml import CommentedMap, YAML


class Status(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class Logger:
    """JSONL event logger whose fields and enabled state are managed via .apf.yaml."""

    def __init__(
        self, *,
        config_key: str,
        logfile: str,
        field_definitions: list[tuple[str, bool, str]] | None = None,
        info_filename: str = ".apf.yaml",
        field_indent: int = 4,
    ) -> None:
        self.config_key = config_key
        self.logfile = logfile
        self.field_definitions = field_definitions or []
        self.info_filename = info_filename
        self.field_indent = field_indent
        self._yaml = YAML()
        self._yaml.preserve_quotes = True

    # ── YAML helpers ──────────────────────────────────────────────────

    def _load_yaml(self, path: Path) -> CommentedMap:
        """Load .apf.yaml, preserving comments and formatting."""
        return self._yaml.load(path.read_text(encoding="utf-8")) or CommentedMap()

    def _add_field(self, fields_map: CommentedMap, name: str, value, comment: str) -> None:
        """Add a field to a ruamel.yaml CommentedMap with a comment above."""
        fields_map[name] = value
        fields_map.yaml_set_comment_before_after_key(name, before=comment, indent=self.field_indent)

    # ── Public API ────────────────────────────────────────────────────

    def load_config(self) -> tuple[bool, set[str]]:
        """Read the config section in the info file and return (enabled, enabled_fields)."""
        path = Path(self.info_filename)
        if not path.exists():
            raise FileNotFoundError(self.info_filename)
        data = self._load_yaml(path).get(self.config_key)
        if not data:
            return False, set()
        is_enabled = data.get("enabled", False)
        fields = data.get("fields", {})
        enabled_fields = {name for name, enabled in fields.items() if enabled is True}
        return is_enabled, enabled_fields

    def status(self) -> Status:
        """Return 'enabled' or 'disabled' based on .apf.yaml."""
        try:
            is_enabled, _ = self.load_config()
            return Status.ENABLED if is_enabled else Status.DISABLED
        except FileNotFoundError:
            return Status.DISABLED

    def install(self, enable_after_install: bool = False, apf_yaml_path: Path | None = None) -> None:
        """Add or update the config section in .apf.yaml."""
        path = apf_yaml_path or Path(self.info_filename)
        config = self._load_yaml(path) if path.exists() else {}
        existing: CommentedMap = config.get(self.config_key)

        if not existing:
            fields_map = CommentedMap()
            for name, default, comment in self.field_definitions:
                self._add_field(fields_map, name, default, comment)
            config[self.config_key] = CommentedMap([
                ("enabled", enable_after_install),
                ("fields", fields_map),
            ])
        else:
            fields_map: CommentedMap = existing.get("fields")
            if not isinstance(fields_map, dict):
                raise ValueError(f"'fields' is missing or corrupt in {self.info_filename}")
            fields_map_keys = set(fields_map.keys())
            missing = [(n, d, c) for n, d, c in self.field_definitions if n not in fields_map_keys]
            if not missing:
                return
            for name, default, comment in missing:
                self._add_field(fields_map, name, default, comment)

        with open(path, "w", encoding="utf-8") as f:
            self._yaml.dump(config, f)

    def set_enabled(self, value: bool, apf_yaml_path: Path | None = None) -> Status:
        """Set logging to enabled or disabled. Return new status."""
        path = apf_yaml_path or Path(self.info_filename)
        if not path.exists():
            raise FileNotFoundError(f"{self.info_filename} not found. Run with --install first.")
        config = self._load_yaml(path)
        section = config.get(self.config_key)
        if not section:
            raise ValueError(f"No {self.config_key} section in {self.info_filename}. Run with --install first.")
        section["enabled"] = value
        with open(path, "w", encoding="utf-8") as f:
            self._yaml.dump(config, f)
        return Status.ENABLED if value else Status.DISABLED

    def get_input(self) -> dict:
        raise NotImplementedError()

    def log_event(self) -> None:
        """If logging is enabled in the info file, read JSON input and append to the log file."""
        is_enabled, enabled_fields = self.load_config()
        if not is_enabled:
            return
        data = self.get_input()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {"timestamp": timestamp}
        record.update({k: v for k, v in data.items()
                       if (not enabled_fields) or k in enabled_fields})
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)
        with open(self.logfile, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def main(self) -> None:
        """CLI entry point: dispatch --status, --install, --on, --off, or log from stdin."""
        if "--status" in sys.argv:
            print(self.status().value)
        elif "--install" in sys.argv:
            self.install()
            print("installed")
        elif "--on" in sys.argv:
            print(self.set_enabled(True).value)
        elif "--off" in sys.argv:
            print(self.set_enabled(False).value)
        elif self.log_event():
            # Successfully activated
            pass
        else:
            print(f"Usage: {Path(sys.argv[0]).name} [--status | --on | --off | --install]",
                  file=sys.stderr)
            sys.exit(1)
