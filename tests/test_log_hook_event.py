import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest
from ruamel.yaml import YAML, CommentedMap

# Make dist/.claude/scripts/apf/ importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "dist" / ".claude" / "scripts" / "apf"))

from log_claude_code_hook_event import (
    FIELD_DEFINITIONS,
    CONFIG_KEY,
    install,
    load_config,
    log_event,
    status,
    toggle,
)

_yaml = YAML()


def _write_apf_yaml(path: Path, enabled: bool, fields: dict) -> None:
    """Helper: write a minimal .apf.yaml with the given enabled/fields."""
    fields_yaml = "\n".join(f"    {k}: {str(v).lower()}" for k, v in fields.items())
    path.write_text(
        f"version: 0.1.0\n\n"
        f"{CONFIG_KEY}:\n"
        f"  enabled: {str(enabled).lower()}\n"
        f"  fields:\n{fields_yaml}\n",
        encoding="utf-8",
    )


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


# ── install() ────────────────────────────────────────────────────────────


class TestInstall:
    def test_adds_section_with_comments(self, tmp_path):
        """install() on a file with no log_claude_code_events section
        should add the full section with a comment above each field."""
        apf_yaml = tmp_path / ".apf.yaml"
        apf_yaml.write_text("version: 0.1.0\n", encoding="utf-8")

        install(apf_yaml_path=apf_yaml)

        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))

        # Original content preserved
        assert config["version"] == "0.1.0"

        # Section structure
        section = config[CONFIG_KEY]
        assert section["enabled"] is False
        fields = section["fields"]
        assert isinstance(fields, CommentedMap)

        # All fields present with correct defaults, in order
        assert list(fields.keys()) == [name for name, _, _ in FIELD_DEFINITIONS]
        for name, default, _ in FIELD_DEFINITIONS:
            assert fields[name] is default, f"{name} should be {default}"

        # Each field has its description as a comment above it
        comments = _extract_comments(fields)
        for name, _, expected_comment in FIELD_DEFINITIONS:
            assert name in comments, f"No comment for {name}"
            assert expected_comment in comments[name]

    def test_enable_after_install(self, tmp_path):
        """install(enable_after_install=True) should set enabled to True."""
        apf_yaml = tmp_path / ".apf.yaml"
        apf_yaml.write_text("version: 0.1.0\n", encoding="utf-8")

        install(enable_after_install=True, apf_yaml_path=apf_yaml)

        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert config[CONFIG_KEY]["enabled"] is True

    def test_creates_file_when_missing(self, tmp_path):
        """install() should work even if .apf.yaml does not exist yet."""
        apf_yaml = tmp_path / ".apf.yaml"
        assert not apf_yaml.exists()

        install(apf_yaml_path=apf_yaml)

        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert CONFIG_KEY in config
        fields = config[CONFIG_KEY]["fields"]
        assert list(fields.keys()) == [name for name, _, _ in FIELD_DEFINITIONS]

    def test_idempotent_when_all_fields_present(self, tmp_path):
        """install() on a complete config should not modify the file."""
        apf_yaml = tmp_path / ".apf.yaml"
        all_fields = {name: default for name, default, _ in FIELD_DEFINITIONS}
        _write_apf_yaml(apf_yaml, enabled=True, fields=all_fields)
        content_before = apf_yaml.read_text(encoding="utf-8")

        install(apf_yaml_path=apf_yaml)

        assert apf_yaml.read_text(encoding="utf-8") == content_before

    def test_adds_missing_fields_to_existing_section(self, tmp_path):
        """install() should add only missing fields to an existing section."""
        apf_yaml = tmp_path / ".apf.yaml"
        # Write config with only the first two fields
        partial_fields = {FIELD_DEFINITIONS[0][0]: True, FIELD_DEFINITIONS[1][0]: False}
        _write_apf_yaml(apf_yaml, enabled=True, fields=partial_fields)

        install(apf_yaml_path=apf_yaml)

        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        fields = config[CONFIG_KEY]["fields"]
        # All fields should now be present
        for name, _, _ in FIELD_DEFINITIONS:
            assert name in fields, f"Missing field: {name}"
        # Existing fields should retain their values
        assert fields[FIELD_DEFINITIONS[0][0]] is True
        assert fields[FIELD_DEFINITIONS[1][0]] is False


# ── load_config() ────────────────────────────────────────────────────────


class TestLoadConfig:
    def test_enabled_with_fields(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=True, fields={"session_id": True, "cwd": False})
        monkeypatch.chdir(tmp_path)

        is_enabled, enabled_fields = load_config()

        assert is_enabled is True
        assert enabled_fields == {"session_id"}

    def test_disabled(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=False, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)

        is_enabled, enabled_fields = load_config()

        assert is_enabled is False
        assert enabled_fields == {"session_id"}

    def test_missing_file_raises(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        with pytest.raises(FileNotFoundError):
            load_config()

    def test_missing_section_returns_disabled(self, tmp_path, monkeypatch):
        """If .apf.yaml exists but has no log_claude_code_events section."""
        apf_yaml = tmp_path / ".apf.yaml"
        apf_yaml.write_text("version: 0.1.0\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        is_enabled, enabled_fields = load_config()

        assert is_enabled is False
        assert enabled_fields == set()

    def test_all_fields_enabled(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        all_fields = {name: True for name, _, _ in FIELD_DEFINITIONS}
        _write_apf_yaml(apf_yaml, enabled=True, fields=all_fields)
        monkeypatch.chdir(tmp_path)

        is_enabled, enabled_fields = load_config()

        assert is_enabled is True
        assert enabled_fields == {name for name, _, _ in FIELD_DEFINITIONS}


# ── log_event() ──────────────────────────────────────────────────────────


class TestLogEvent:
    def test_writes_enabled_fields_only(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(
            apf_yaml,
            enabled=True,
            fields={"session_id": True, "agent_type": True, "cwd": False},
        )
        monkeypatch.chdir(tmp_path)

        stdin_data = json.dumps({
            "session_id": "sess-123",
            "agent_type": "Explore",
            "cwd": "/should/be/excluded",
            "extra_field": "also excluded",
        })
        monkeypatch.setattr("sys.stdin", StringIO(stdin_data))

        log_event()

        logfile = tmp_path / "tmp" / "logs" / "claude_code_hook_events_log.jsonl"
        assert logfile.exists()
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert "timestamp" in record
        assert record["session_id"] == "sess-123"
        assert record["agent_type"] == "Explore"
        assert "cwd" not in record
        assert "extra_field" not in record

    def test_skips_when_disabled(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=False, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)

        log_event()

        logfile = tmp_path / "tmp" / "logs" / "claude_code_hook_events_log.jsonl"
        assert not logfile.exists()

    def test_appends_to_existing_log(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=True, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)

        # Write two events
        for sid in ("sess-1", "sess-2"):
            monkeypatch.setattr("sys.stdin", StringIO(json.dumps({"session_id": sid})))
            log_event()

        logfile = tmp_path / "tmp" / "logs" / "claude_code_hook_events_log.jsonl"
        lines = logfile.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["session_id"] == "sess-1"
        assert json.loads(lines[1])["session_id"] == "sess-2"

    def test_timestamp_format(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=True, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps({"session_id": "s1"})))

        log_event()

        logfile = tmp_path / "tmp" / "logs" / "claude_code_hook_events_log.jsonl"
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        # ISO 8601 UTC format: YYYY-MM-DDTHH:MM:SSZ
        import re
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["timestamp"])


# ── status() ─────────────────────────────────────────────────────────────


class TestStatus:
    def test_returns_enabled(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=True, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)

        assert status() == "enabled"

    def test_returns_disabled(self, tmp_path, monkeypatch):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=False, fields={"session_id": True})
        monkeypatch.chdir(tmp_path)

        assert status() == "disabled"

    def test_returns_disabled_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        assert status() == "disabled"


# ── toggle() ─────────────────────────────────────────────────────────────


class TestToggle:
    def test_enables_when_disabled(self, tmp_path):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=False, fields={"session_id": True})

        result = toggle(apf_yaml_path=apf_yaml)

        assert result == "enabled"
        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert config[CONFIG_KEY]["enabled"] is True

    def test_disables_when_enabled(self, tmp_path):
        apf_yaml = tmp_path / ".apf.yaml"
        _write_apf_yaml(apf_yaml, enabled=True, fields={"session_id": True})

        result = toggle(apf_yaml_path=apf_yaml)

        assert result == "disabled"
        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert config[CONFIG_KEY]["enabled"] is False

    def test_installs_and_enables_when_file_missing(self, tmp_path):
        apf_yaml = tmp_path / ".apf.yaml"

        result = toggle(apf_yaml_path=apf_yaml)

        assert result == "enabled"
        assert apf_yaml.exists()
        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert config[CONFIG_KEY]["enabled"] is True

    def test_installs_and_enables_when_section_missing(self, tmp_path):
        apf_yaml = tmp_path / ".apf.yaml"
        apf_yaml.write_text("version: 0.1.0\n", encoding="utf-8")

        result = toggle(apf_yaml_path=apf_yaml)

        assert result == "enabled"
        config = _yaml.load(apf_yaml.read_text(encoding="utf-8"))
        assert config[CONFIG_KEY]["enabled"] is True
