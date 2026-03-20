import sys
from pathlib import Path

from ruamel.yaml import YAML, CommentedMap


CYAML = CommentedMap

ALLOW_ALL_FIELDS = "*"

APF_FOLDER = ".apf"
APF_INFO_FILENAME = ".apf.yaml"
APF_INFO_FILEPATH = f"{APF_FOLDER}/{APF_INFO_FILENAME}"


class InvalidInputException(Exception):
    pass


def warn(*args, **kwargs) -> None:
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


"""cyaml below means: yaml with comments preserved.
This is a wrapper around ruaml YAML
"""


def cyaml_load(path: Path) -> CYAML:
    """Load a yaml file, preserving comments and formatting."""
    return YAML().load(path.read_text(encoding="utf-8")) or CYAML()


def cyaml_save(path: Path, data: CYAML) -> None:
    with open(path, "w", encoding="utf-8") as f:
        YAML().dump(data, f)


def cyaml_add_field(cyaml: CYAML, key: str, value,
                    comment: str | None = None, indent: int = 4) -> None:
    """Add a field to a cyaml with a comment above the field."""
    cyaml[key] = value
    kwargs = dict(before=comment) if comment else {}
    cyaml.yaml_set_comment_before_after_key(key, indent=indent, **kwargs)
