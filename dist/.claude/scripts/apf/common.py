import os
import sys
from pathlib import Path

import yaml


ALLOW_ALL_FIELDS = "*"

APF_FOLDER = ".apf"
APF_INFO_FILENAME = ".apf.yaml"
APF_INFO_FILEPATH = f"{APF_FOLDER}/{APF_INFO_FILENAME}"

KEY_log_claude_code_hook_event = "log_claude_code_hook_event"


class InvalidInputException(Exception):
    pass


def warn(*args, **kwargs) -> None:
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def save_text(text: str, filepath: Path) -> None:
    os.makedirs(filepath.parent, exist_ok=True)
    filepath.write_text(text, encoding="utf-8")


def yaml_load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def yaml_save(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True)
