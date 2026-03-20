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

from common import CYAML, cyaml_load, cyaml_save, cyaml_add_field, APF_INFO_FILEPATH, \
    InvalidInputException, ALLOW_ALL_FIELDS, warn


class Status(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class Logger(ABC):
    """JSONL event logger whose fields and enabled state are managed via a config yaml"""

    def __init__(
        self, *,
        config_key: str,
        logfile: str,
        field_definitions: str | list[tuple[str, bool, str]] = ALLOW_ALL_FIELDS,
        config_filepath: str = APF_INFO_FILEPATH,
        field_indent: int = 4,
        sentinel_filepath: str | None = None,
    ) -> None:
        """TODO: Write docstring explaining each parameter
        including: A value of ALLOW_ALL_FIELDS ("*") in field_definitions means: match all fields
        """
        self.config_key = config_key
        self.logfile = logfile
        self.field_definitions = field_definitions
        self.config_filepath = Path(config_filepath)
        if not self.config_filepath.exists():
            raise FileNotFoundError(self.config_filepath)
        self.field_indent = field_indent
        self.sentinel_filepath = Path(sentinel_filepath) if sentinel_filepath else None

    def load_config(self) -> str | set[str]:
        """Read the config section in the config file and return (enabled, enabled_fields)."""
        data = cyaml_load(self.config_filepath).get(self.config_key)
        if not data:
            print(f"Warning: {self.config_key} section missing "
                  f"from config file {self.config_filepath}, "
                  f"so no logging will occur", file=sys.stderr)
            return set()
        if data == ALLOW_ALL_FIELDS:
            return data
        enabled_fields = {name for name, enabled in data.items() if enabled is True}
        return enabled_fields

    def status(self) -> Status:
        """Return Status based on the sentinel file"""
        if not self.sentinel_filepath or not self.sentinel_filepath.exists():
            return Status.DISABLED
        if self.sentinel_filepath.read_text().strip() == "on":
            return Status.ENABLED
        else:
            return Status.DISABLED

    def _install_on_existing_section(self, existing: str | CYAML) -> bool:
        """Returns True iff there was a change"""
        if existing == ALLOW_ALL_FIELDS:
            # Match everything, so no need to mention specific fields
            return False
        if not isinstance(existing, CYAML):
            raise ValueError(f"'fields' is missing or corrupt in {self.config_filepath}")
        fields_keys = set(existing.keys())
        if not isinstance(self.field_definitions, list):
            raise RuntimeError("field_definitions is not a list")
        missing = [(n, d, c) for n, d, c in self.field_definitions if n not in fields_keys]
        if not missing:
            # No missing keys, so no need to re-write fields
            return False
        # If there are missing keys, we add them here, and save below
        for name, default, comment in missing:
            cyaml_add_field(existing, name, default, comment, indent=self.field_indent)
        return True

    def set_enabled(self, value: bool) -> None:
        """TODO: Add docstring"""
        if not self.is_installed():
            name = self.config_key.replace('_', '-')
            warn(f"You must install {name} before you can turn it on or off.\n"
                 f"Run: /name install")
            exit(1)
        if self.sentinel_filepath:
            os.makedirs(self.sentinel_filepath.parent, exist_ok=True)
            self.sentinel_filepath.write_text("on" if value else "off", encoding="utf-8")

    def install(self) -> None:
        """Add or update the sentinel and the config section in the config file"""
        # This forces the sentinel file to exist if it's defined
        if self.status() is Status.DISABLED:
            self.set_enabled(False)

        config = cyaml_load(self.config_filepath)
        existing: CYAML = config.get(self.config_key)
        if existing:
            changed = self._install_on_existing_section(existing)
            if changed:
                cyaml_save(self.config_filepath, config)
            return

        # section doesn't exist, need to create it
        if self.field_definitions == ALLOW_ALL_FIELDS:
            fields = ALLOW_ALL_FIELDS
        else:
            # Add all fields
            fields = CYAML()
            if not isinstance(self.field_definitions, list):
                raise RuntimeError("field_definitions is not a list")
            for name, default, comment in self.field_definitions:
                cyaml_add_field(fields, name, default, comment, indent=self.field_indent)
        config[self.config_key] = fields
        cyaml_save(self.config_filepath, config)

    @abstractmethod
    def get_input(self) -> dict:
        pass

    def log_event(self) -> None:
        """If logging is enabled, read JSON input and append to the log file."""
        if self.status() == Status.DISABLED:
            return
        enabled_fields = self.load_config()
        if not enabled_fields:
            warn(f"Warning: all fields are disabled in section {self.config_key} "
                 f"in config file {self.config_filepath}, so logging is effectively disabled")
            return
        data = self.get_input()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {"_timestamp_": timestamp}
        # We assume that data doesn't have a field "_timestamp_"
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
            self.set_enabled(True)
            print(Status.ENABLED.value)
        elif "--off" in sys.argv:
            self.set_enabled(False)
            print(Status.DISABLED.value)
        else:
            try:
                self.log_event()
            except InvalidInputException as e:
                print(f"{str(e)}\nUsage: {Path(sys.argv[0]).name} [--status | --on | --off | --install]",
                      file=sys.stderr)
                sys.exit(1)
