import json
import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

# Make distribution/.claude/apf/scripts/ importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "distribution" / ".claude" / "apf" / "scripts"))

from common import KEY_LOG_CLAUDE_CODE_HOOK_EVENT, ALLOW_ALL_FIELDS
from log_claude_code_hook_event import ClaudeCodeHookLogger, FIELD_DEFINITIONS, LOGFILE
from logger import Status

CONFIG_KEY = KEY_LOG_CLAUDE_CODE_HOOK_EVENT


def _make_logger(
    config_filepath: Path, sentinel_filepath: Path | None = None,
) -> ClaudeCodeHookLogger:
    kwargs = {
        "config_key": CONFIG_KEY,
        "logfile": LOGFILE,
        "field_definitions": FIELD_DEFINITIONS,
        "config_filepath": str(config_filepath),
    }
    if sentinel_filepath is not None:
        kwargs["sentinel_filepath"] = str(sentinel_filepath)
    return ClaudeCodeHookLogger(**kwargs)


def _write_base_config(path: Path) -> None:
    path.write_text(yaml.dump({"version": "0.1.0"}), encoding="utf-8")


def _write_config_with_section(path: Path, *, default: bool = False, do_all: bool = False,
                                fields: dict | None = None) -> None:
    """Write .apf.yaml with the logger's config section."""
    section: dict = {"do_all": do_all, "default": default}
    section["fields"] = [{"name": k, "value": v, "comment": ""} for k, v in (fields or {}).items()]
    path.write_text(yaml.dump({"version": "0.1.0", CONFIG_KEY: section}), encoding="utf-8")


# ── install() ────────────────────────────────────────────────────────────


class TestInstall:
    def test_adds_section(self, tmp_path):
        """install() on a file with no config section should add the full section."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_base_config(config_file)

        with patch(
            "set_hooks_for_claude_code_event_logger.HooksInstaller.install_hooks_in_settings_file",
        ):
            _make_logger(config_file, sentinel).install()

        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        assert config["version"] == "0.1.0"
        section = config[CONFIG_KEY]
        assert section["do_all"] is False
        assert section["default"] is False
        fields = section["fields"]
        assert isinstance(fields, list)
        field_names = [f["name"] for f in fields]
        assert field_names == [fd["name"] for fd in FIELD_DEFINITIONS]
        for fd in FIELD_DEFINITIONS:
            match = next(f for f in fields if f["name"] == fd["name"])
            assert match["value"] is fd["value"]

    def test_creates_sentinel_as_off(self, tmp_path):
        """install() should create the sentinel file with 'off'."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_base_config(config_file)

        with patch(
            "set_hooks_for_claude_code_event_logger.HooksInstaller.install_hooks_in_settings_file",
        ):
            _make_logger(config_file, sentinel).install()

        assert sentinel.exists()
        assert sentinel.read_text().strip() == "off"

    def test_idempotent_when_all_fields_present(self, tmp_path):
        """install() on a complete config should not modify the config file."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        all_fields = {fd["name"]: fd["value"] for fd in FIELD_DEFINITIONS}
        _write_config_with_section(config_file, fields=all_fields)
        content_before = config_file.read_text(encoding="utf-8")

        with patch(
            "set_hooks_for_claude_code_event_logger.HooksInstaller.install_hooks_in_settings_file",
        ):
            _make_logger(config_file, sentinel).install()

        assert config_file.read_text(encoding="utf-8") == content_before

    def test_adds_missing_fields_to_existing_section(self, tmp_path):
        """install() should add only missing fields to an existing section."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        partial_fields = {FIELD_DEFINITIONS[0]["name"]: True, FIELD_DEFINITIONS[1]["name"]: False}
        _write_config_with_section(config_file, fields=partial_fields)

        with patch(
            "set_hooks_for_claude_code_event_logger.HooksInstaller.install_hooks_in_settings_file",
        ):
            _make_logger(config_file, sentinel).install()

        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        fields = config[CONFIG_KEY]["fields"]
        field_map = {f["name"]: f["value"] for f in fields}
        for fd in FIELD_DEFINITIONS:
            assert fd["name"] in field_map
        assert field_map[FIELD_DEFINITIONS[0]["name"]] is True
        assert field_map[FIELD_DEFINITIONS[1]["name"]] is False


# ── load_config() ────────────────────────────────────────────────────────


class TestLoadConfig:
    def test_returns_fields_dict(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        _write_config_with_section(config_file, fields={"session_id": True, "cwd": False})

        default, fields = _make_logger(config_file).load_config()

        assert default is False
        assert fields == {"session_id": True, "cwd": False}

    def test_do_all_returns_allow_all(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        _write_config_with_section(config_file, do_all=True)

        result = _make_logger(config_file).load_config()

        assert result == ALLOW_ALL_FIELDS

    def test_missing_section_returns_empty(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        _write_base_config(config_file)

        default, fields = _make_logger(config_file).load_config()

        assert default is False
        assert fields == {}

    def test_default_true_with_exclusions(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        _write_config_with_section(config_file, default=True, fields={"cwd": False})

        default, fields = _make_logger(config_file).load_config()

        assert default is True
        assert fields == {"cwd": False}

    def test_all_fields_enabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        all_fields = {fd["name"]: True for fd in FIELD_DEFINITIONS}
        _write_config_with_section(config_file, fields=all_fields)

        default, fields = _make_logger(config_file).load_config()

        assert default is False
        assert fields == all_fields


# ── log_event() ──────────────────────────────────────────────────────────


class TestLogEvent:
    def _make_enabled_logger(self, config_file: Path, sentinel: Path) -> ClaudeCodeHookLogger:
        sentinel.write_text("on\n", encoding="utf-8")
        return _make_logger(config_file, sentinel)

    def test_writes_enabled_fields_only(self, tmp_path, monkeypatch):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(
            config_file, fields={"session_id": True, "agent_type": True, "cwd": False},
        )
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", [""])
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps({
            "session_id": "sess-123",
            "agent_type": "Explore",
            "cwd": "/should/be/excluded",
            "extra_field": "also excluded",
        })))

        logger.log_event()

        logfile = tmp_path / "logs" / "claude_code_hook_events.jsonl"
        assert logfile.exists()
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert "_timestamp_" in record
        assert record["session_id"] == "sess-123"
        assert record["agent_type"] == "Explore"
        assert "cwd" not in record
        assert "extra_field" not in record

    def test_skips_when_not_enabled(self, tmp_path, monkeypatch):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"  # missing → NOT_INSTALLED
        _write_config_with_section(config_file, fields={"session_id": True})
        logger = _make_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", [""])

        logger.log_event()

        assert not (tmp_path / "logs" / "claude_code_hook_events.jsonl").exists()

    def test_appends_to_existing_log(self, tmp_path, monkeypatch):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", [""])

        for sid in ("sess-1", "sess-2"):
            monkeypatch.setattr("sys.stdin", StringIO(json.dumps({"session_id": sid})))
            logger.log_event()

        logfile = tmp_path / "logs" / "claude_code_hook_events.jsonl"
        lines = logfile.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["session_id"] == "sess-1"
        assert json.loads(lines[1])["session_id"] == "sess-2"

    def test_timestamp_format(self, tmp_path, monkeypatch):
        import re
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", [""])
        monkeypatch.setattr("sys.stdin", StringIO(json.dumps({"session_id": "s1"})))

        logger.log_event()

        logfile = tmp_path / "logs" / "claude_code_hook_events.jsonl"
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["_timestamp_"])


# ── status() ─────────────────────────────────────────────────────────────


class TestStatus:
    def test_returns_enabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("on\n", encoding="utf-8")

        assert _make_logger(config_file, sentinel).status() == Status.ENABLED

    def test_returns_disabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("off\n", encoding="utf-8")

        assert _make_logger(config_file, sentinel).status() == Status.DISABLED

    def test_returns_not_installed_when_sentinel_missing(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})

        assert _make_logger(config_file, sentinel).status() == Status.NOT_INSTALLED

    def test_returns_not_installed_when_section_missing(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_base_config(config_file)
        sentinel.write_text("on\n", encoding="utf-8")

        assert _make_logger(config_file, sentinel).status() == Status.NOT_INSTALLED


# ── set_enabled() ─────────────────────────────────────────────────────────


class TestSetEnabled:
    def test_enables_when_disabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("off\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(True)

        assert logger.status() == Status.ENABLED

    def test_disables_when_enabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("on\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(False)

        assert logger.status() == Status.DISABLED

    def test_exits_when_not_installed(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"  # missing → NOT_INSTALLED
        _write_config_with_section(config_file, fields={"session_id": True})
        logger = _make_logger(config_file, sentinel)

        with pytest.raises(SystemExit):
            logger.set_enabled(True)

    def test_on_is_idempotent(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("on\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(True)

        assert logger.status() == Status.ENABLED

    def test_off_is_idempotent(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file, fields={"session_id": True})
        sentinel.write_text("off\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(False)

        assert logger.status() == Status.DISABLED
