"""
Configurable JSONL event logger backed by .apf.yaml.

Provides status/install/on/off management and field-filtered event logging.
Instantiate with a key from a config yaml, log file path, and field definitions,
then call methods or wire up main() to sys.argv.
"""

import json
import os
import sys
from abc import abstractmethod, ABC
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path

from common import CYAML, cyaml_load, cyaml_save, cyaml_add_field, APF_INFO_FILENAME, \
    InvalidInputException, ALLOW_ALL_FIELDS


class Status(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class Logger(ABC):
    """JSONL event logger whose fields and enabled state are managed via a config yaml"""

    def __init__(
        self, *,
        config_key: str,
        logfile: str,
        field_definitions: str | None | list[tuple[str, bool, str]] = ALLOW_ALL_FIELDS,
        config_filepath: str = APF_INFO_FILENAME,
        field_indent: int = 4,
    ) -> None:
        self.config_key = config_key
        self.logfile = logfile
        # A value of ALLOW_ALL_FIELDS ("*") in field_definitions means: match all fields
        self.field_definitions = ALLOW_ALL_FIELDS if field_definitions is None else field_definitions
        self.config_filepath = Path(config_filepath)
        if not self.config_filepath.exists():
            raise FileNotFoundError(self.config_filepath)

        self.field_indent = field_indent

    def load_config(self) -> tuple[bool, str | set[str]]:
        """Read the config section in the config file and return (enabled, enabled_fields)."""
        data = cyaml_load(self.config_filepath).get(self.config_key)
        if not data:
            return False, set()
        is_enabled = data.get(Status.ENABLED.value, False)
        fields = data.get("fields", {})
        if fields == ALLOW_ALL_FIELDS:
            enabled_fields = fields
        else:
            enabled_fields = {name for name, enabled in fields.items() if enabled is True}
        return is_enabled, enabled_fields

    def status(self) -> Status:
        """Return 'enabled' or 'disabled' based on the config file"""
        try:
            is_enabled, _ = self.load_config()
            return Status.ENABLED if is_enabled else Status.DISABLED
        except FileNotFoundError:
            return Status.DISABLED

    def install(self, enable_after_install: bool = False) -> None:
        """Add or update the config section in the config file"""
        config = cyaml_load(self.config_filepath)
        existing: CYAML = config.get(self.config_key)
        changed = False

        if existing:
            if enable_after_install and existing.get("enabled") is False:
                existing["enabled"] = True
                changed = True
            fields = existing.get("fields")
            if fields == ALLOW_ALL_FIELDS:
                # Match everything, so no need to mention specific fields
                if not changed:
                    return
            if not isinstance(fields, CYAML):
                raise ValueError(f"'fields' is missing or corrupt in {self.config_filepath}")
            fields_keys = set(fields.keys())
            missing = [(n, d, c) for n, d, c in self.field_definitions if n not in fields_keys]
            if not missing:
                # No missing keys, so no need to re-write fields
                if not changed:
                    return
            else:
                # If there are missing keys, we add them here, and save below
                for name, default, comment in missing:
                    cyaml_add_field(fields, name, default, comment)
        else:
            # section doesn't exist, need to create it
            if self.field_definitions == ALLOW_ALL_FIELDS:
                fields = ALLOW_ALL_FIELDS
            else:
                # Add all fields
                fields = CYAML()
                for name, default, comment in self.field_definitions:
                    cyaml_add_field(fields, name, default, comment)
            config[self.config_key] = CYAML([
                ("enabled", enable_after_install),
                ("fields", fields),
            ])

        cyaml_save(self.config_filepath, config)

    def set_enabled(self, value: bool) -> Status:
        """Set logging to enabled or disabled. Return new status."""
        config = cyaml_load(self.config_filepath)
        section = config.get(self.config_key)
        if not section:
            raise ValueError(f"No {self.config_key} section in {self.config_filepath}. Run with --install first.")
        section["enabled"] = value
        cyaml_save(self.config_filepath, config)
        return Status.ENABLED if value else Status.DISABLED

    @abstractmethod
    def get_input(self) -> dict:
        pass

    def log_event(self) -> None:
        """If logging is enabled in the config file, read JSON input and append to the log file."""
        is_enabled, enabled_fields = self.load_config()
        if not is_enabled:
            return
        data = self.get_input()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {"timestamp": timestamp}
        if enabled_fields == ALLOW_ALL_FIELDS:
            record.update(data)
        else:
            record.update({k: v for k, v in data.items() if k in enabled_fields})
        if dirname := os.path.dirname(self.logfile):
            os.makedirs(dirname, exist_ok=True)
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
        else:
            try:
                self.log_event()
            except InvalidInputException as e:
                print(str(e))
                print(f"Usage: {Path(sys.argv[0]).name} [--status | --on | --off | --install]",
                      file=sys.stderr)
                sys.exit(1)
