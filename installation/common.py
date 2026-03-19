from pathlib import Path

from ruamel.yaml import YAML, CommentedMap

CYAML = CommentedMap


APF_INFO_FILENAME = ".apf.yaml"


class InvalidInputException(Exception):
    pass


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
