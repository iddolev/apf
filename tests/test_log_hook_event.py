import sys
from pathlib import Path

import pytest
from ruamel.yaml import YAML, CommentedMap

# Make dist/.claude/scripts/apf/log_hook_event.py importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dist" / ".claude" / "scripts" / "apf"))

from log_hook_event import install, FIELD_DEFINITIONS


_yaml = YAML()


def _extract_comments(fields: CommentedMap) -> dict[str, str]:
    """Extract the 'before' comment for each field key.

    ruamel.yaml stores before-comments with an offset:
    - The first key's comment is in fields.ca.comment[1]
    - Each later key's comment is at index [2] of the *previous* key's ca.items entry
    """
    keys = list(fields.keys())
    comments = {}

    # First key: comment is on the map itself
    if fields.ca.comment and fields.ca.comment[1]:
        comments[keys[0]] = fields.ca.comment[1][0].value

    # Remaining keys: comment is stored as "after" on the previous key
    for i, key in enumerate(keys[:-1]):
        token = fields.ca.items.get(key)
        if token and token[2]:
            comments[keys[i + 1]] = token[2].value

    return comments


def test_install_adds_section_with_comments(tmp_path):
    """install() on a file with no log_claude_code_events section
    should add the full section with a comment above each field."""
    apf_yaml = tmp_path / ".apf.yaml"
    apf_yaml.write_text("version: 0.1.0\n", encoding="utf-8")

    install(apf_yaml)

    config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))

    # Original content preserved
    assert config["version"] == "0.1.0"

    # Section structure
    section = config["log_claude_code_events"]
    assert section["enabled"] is False
    fields = section["fields"]
    assert isinstance(fields, CommentedMap)

    # All fields present with correct defaults, in order
    assert list(fields.keys()) == [name for name, _, _ in FIELD_DEFINITIONS]
    for name, default, _ in FIELD_DEFINITIONS:
        assert fields[name] is default, f"{name} should be {default}, got {fields[name]}"

    # Each field has its description as a comment above it
    comments = _extract_comments(fields)
    for name, _, expected_comment in FIELD_DEFINITIONS:
        assert name in comments, f"No comment for {name}"
        assert expected_comment in comments[name], (
            f"Comment for {name}: expected '{expected_comment}' in '{comments[name]}'"
        )

    assert False # try