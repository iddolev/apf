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

from common import yaml_load, yaml_save, APF_INFO_FILEPATH, \
    InvalidInputException, ALLOW_ALL_FIELDS, warn, save_text


def debug(item) -> None:
    with open("logs/debug.txt", "a") as f:
        f.write(f"{datetime.now()}\n{item}\n")


class Status(Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    NOT_INSTALLED = "not_installed"


class Logger(ABC):
    """JSONL event logger whose fields and enabled state are managed via a config yaml"""

    def __init__(
        self, *,
        config_key: str,
        logfile: str,
        field_definitions: str | list[dict] = ALLOW_ALL_FIELDS,
        config_filepath: str = APF_INFO_FILEPATH,
        sentinel_filepath: str | None = None,
    ) -> None:
        """
        :param config_key: Key in the config YAML file that holds this logger's fields settings.
        :param logfile: Path to the JSONL file where events are appended.
        :param field_definitions: Either ALLOW_ALL_FIELDS ("*") to log every field in the input,
            or a list of dicts with "name", "value", and "comment" keys that
            define which fields are available and their enabled state in the config file.
        :param config_filepath: Path to the YAML config file (default: .apf/.apf.yaml).
        :param sentinel_filepath: Optional path to a file whose content ("on"/"off") controls
            whether logging is active. If None, the logger has no sentinel and is always
            considered enabled once installed.
        """
        self.config_key = config_key
        self.logfile = logfile
        self.field_definitions = field_definitions
        self.config_filepath = Path(config_filepath)
        if not self.config_filepath.exists():
            raise FileNotFoundError(self.config_filepath)
        self.sentinel_filepath = Path(sentinel_filepath) if sentinel_filepath else None

    def load_config(self) -> str | tuple[bool, dict[str, bool]]:
        """Read the config section and return the field selection config.

        Returns:
            ALLOW_ALL_FIELDS if do_all is true.
            (default, fields) otherwise, where:
                default=False: include only fields with value=true in fields
                default=True:  include all fields except those with value=false in fields
        """
        data = yaml_load(self.config_filepath).get(self.config_key)
        if not data:
            print(f"Warning: {self.config_key} section missing "
                  f"from config file {self.config_filepath}, "
                  f"so no logging will occur", file=sys.stderr)
            return False, {}
        if data.get("do_all"):
            return ALLOW_ALL_FIELDS
        default = bool(data.get("default"))
        fields = data.get("fields")
        if fields is None:
            print(f"Warning: 'fields' missing from {self.config_key} section "
                  f"in config file {self.config_filepath}, "
                  f"so no logging will occur", file=sys.stderr)
            return False, {}
        if fields == ALLOW_ALL_FIELDS:
            return ALLOW_ALL_FIELDS
        fields_as_dict = {item['name']: item['value'] for item in fields}
        return default, fields_as_dict

    def status(self) -> Status:
        """Return ENABLED, DISABLED, or NOT_INSTALLED."""
        if self.sentinel_filepath and not self.sentinel_filepath.exists():
            return Status.NOT_INSTALLED
        if self.config_key not in yaml_load(self.config_filepath):
            return Status.NOT_INSTALLED
        if self.sentinel_filepath and self.sentinel_filepath.read_text().strip() == "on":
            return Status.ENABLED
        return Status.DISABLED

    def _install_on_existing_section(self, existing) -> bool:
        """Returns True iff there was a change"""
        if not isinstance(existing, dict):
            raise ValueError(f"Section '{self.config_key}' is missing or corrupt in {self.config_filepath}")
        fields = existing.get("fields")
        if fields == ALLOW_ALL_FIELDS:
            # Match everything, so no need to mention specific fields
            return False
        if not isinstance(fields, list):
            raise ValueError(f"'fields' is missing or corrupt in {self.config_filepath}")
        if not isinstance(self.field_definitions, list):
            raise RuntimeError("field_definitions is not a list")
        existing_names = {f["name"] for f in fields}
        missing = [f for f in self.field_definitions if f["name"] not in existing_names]
        if not missing:
            # No missing keys, so no need to re-write fields
            return False
        # If there are missing keys, we add them here, and save below
        fields.extend(missing)
        return True

    def set_enabled(self, value: bool) -> None:
        """Enable or disable logging by writing "on"/"off" to the sentinel file.
        Exits with an error if the logger has not been installed yet.
        Has no effect if no sentinel_filepath was configured.
        """
        if self.status() == Status.NOT_INSTALLED:
            name = self.config_key.replace('_', '-')
            warn(f"You must install {name} before you can turn it on or off.\n"
                 f"Run: /{name} install")
            exit(1)
        if self.sentinel_filepath:
            save_text("on\n" if value else "off\n", self.sentinel_filepath)

    def install(self) -> None:
        """Add or update the sentinel and the config section in the config file"""
        # Ensure the sentinel file exists (defaulting to "off") if it's defined but missing
        if self.sentinel_filepath and not self.sentinel_filepath.exists():
            save_text("off\n", self.sentinel_filepath)

        config = yaml_load(self.config_filepath)
        existing = config.get(self.config_key)
        if existing:
            changed = self._install_on_existing_section(existing)
            if changed:
                yaml_save(self.config_filepath, config)
            return

        # section doesn't exist, need to create it
        if self.field_definitions == ALLOW_ALL_FIELDS:
            fields = ALLOW_ALL_FIELDS
        else:
            if not isinstance(self.field_definitions, list):
                raise RuntimeError("field_definitions is not a list")
            fields = list(self.field_definitions)
        section = {"do_all": False, "default": False, "fields": fields}
        config[self.config_key] = section
        yaml_save(self.config_filepath, config)

    @abstractmethod
    def get_input(self) -> dict:
        pass

    def log_event(self) -> None:
        """If logging is enabled, read JSON input and append to the log file."""
        if self.status() != Status.ENABLED:
            return
        config = self.load_config()
        data = self.get_input()
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        record = {"_timestamp_": timestamp}
        # We assume that data doesn't have a field "_timestamp_"
        if config == ALLOW_ALL_FIELDS:
            record.update(data)
        else:
            assert isinstance(config, tuple) and len(config) == 2
            default, fields = config
            if not default and not fields:
                warn(f"Warning: all fields are disabled in section {self.config_key} "
                     f"in config file {self.config_filepath}, so logging is effectively disabled")
                return
            if default:
                # All keys missing from the config file should be included
                record.update({k: v for k, v in data.items() if fields.get(k, True)})
            else:
                # All keys missing from the config file should be excluded
                record.update({k: v for k, v in data.items() if fields.get(k, False)})
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
