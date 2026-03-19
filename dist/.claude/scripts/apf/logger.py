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

from common import CYAML, cyaml_load, cyaml_save, cyaml_add_field


class Status(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class Logger:
    """JSONL event logger whose fields and enabled state are managed via a config yaml"""

    def __init__(
        self, *,
        config_key: str,
        logfile: str,
        field_definitions: list[tuple[str, bool, str]] | None = None,
        config_filename: str = ".apf.yaml",
        field_indent: int = 4,
    ) -> None:
        self.config_key = config_key
        self.logfile = logfile
        self.field_definitions = field_definitions or []
        self.config_filename = config_filename
        self.field_indent = field_indent

    def load_config(self) -> tuple[bool, set[str]]:
        """Read the config section in the config file and return (enabled, enabled_fields)."""
        path = Path(self.config_filename)
        if not path.exists():
            raise FileNotFoundError(self.config_filename)
        data = cyaml_load(path).get(self.config_key)
        if not data:
            return False, set()
        is_enabled = data.get(Status.ENABLED.value, False)
        fields = data.get("fields", {})
        enabled_fields = {name for name, enabled in fields.items() if enabled is True}
        return is_enabled, enabled_fields

    def status(self) -> Status:
        """Return 'enabled' or 'disabled' based on the config file"""
        try:
            is_enabled, _ = self.load_config()
            return Status.ENABLED if is_enabled else Status.DISABLED
        except FileNotFoundError:
            return Status.DISABLED

    def install(self, enable_after_install: bool = False, apf_yaml_path: Path | None = None) -> None:
        """Add or update the config section in the config file"""
        path = apf_yaml_path or Path(self.config_filename)
        config = cyaml_load(path) if path.exists() else {}
        existing: CYAML = config.get(self.config_key)

        if not existing:
            fields_map = CYAML()
            for name, default, comment in self.field_definitions:
                cyaml_add_field(fields_map, name, default, comment)
            config[self.config_key] = CYAML([
                ("enabled", enable_after_install),
                ("fields", fields_map),
            ])
        else:
            fields_map: CYAML = existing.get("fields")
            if not isinstance(fields_map, dict):
                raise ValueError(f"'fields' is missing or corrupt in {self.config_filename}")
            fields_map_keys = set(fields_map.keys())
            missing = [(n, d, c) for n, d, c in self.field_definitions if n not in fields_map_keys]
            if not missing:
                return
            for name, default, comment in missing:
                cyaml_add_field(fields_map, name, default, comment)

        cyaml_save(path, config)

    def set_enabled(self, value: bool, apf_yaml_path: Path | None = None) -> Status:
        """Set logging to enabled or disabled. Return new status."""
        path = apf_yaml_path or Path(self.config_filename)
        if not path.exists():
            raise FileNotFoundError(f"{self.config_filename} not found. Run with --install first.")
        config = cyaml_load(path)
        section = config.get(self.config_key)
        if not section:
            raise ValueError(f"No {self.config_key} section in {self.config_filename}. Run with --install first.")
        section["enabled"] = value
        cyaml_save(path, config)
        return Status.ENABLED if value else Status.DISABLED

    def get_input(self) -> dict:
        raise NotImplementedError()

    def log_event(self) -> None:
        """If logging is enabled in the config file, read JSON input and append to the log file."""
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
