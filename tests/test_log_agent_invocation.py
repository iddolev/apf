import json
import sys
from pathlib import Path

import pytest
import yaml

# Make dist/.claude/scripts/apf/ importable
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "dist" / ".claude" / "scripts" / "apf"))

from common import ALLOW_ALL_FIELDS, InvalidInputException
from log_agent_invocation import AgentInvocationLogger, KEY_log_agent_invocation, LOGFILE
from logger import Status, EVENT_ID_FIELD, EVENT_ID_VALUE

CONFIG_KEY = KEY_log_agent_invocation


def _make_logger(config_filepath: Path, sentinel_filepath: Path | None = None) -> AgentInvocationLogger:
    kwargs = dict(
        config_key=CONFIG_KEY,
        logfile=LOGFILE,
        field_definitions=ALLOW_ALL_FIELDS,
        config_filepath=str(config_filepath),
    )
    if sentinel_filepath is not None:
        kwargs["sentinel_filepath"] = str(sentinel_filepath)
    return AgentInvocationLogger(**kwargs)


def _write_base_config(path: Path) -> None:
    path.write_text(yaml.dump({"version": "0.1.0"}), encoding="utf-8")


def _write_config_with_section(path: Path) -> None:
    """Write .apf.yaml with the logger's config section using ALLOW_ALL_FIELDS."""
    section = {"do_all": False, "default": False, "fields": ALLOW_ALL_FIELDS}
    path.write_text(yaml.dump({"version": "0.1.0", CONFIG_KEY: section}), encoding="utf-8")


# ── get_input() ───────────────────────────────────────────────────────────


class TestGetInput:
    def _make_any_logger(self, tmp_path: Path) -> AgentInvocationLogger:
        config_file = tmp_path / "apf.yaml"
        _write_base_config(config_file)
        return _make_logger(config_file)

    def test_four_args_returns_dict(self, tmp_path, monkeypatch):
        """4 positional args (no invocation_id_value) returns the expected dict."""
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "Starting session", "invocation_id"])
        logger = self._make_any_logger(tmp_path)

        result = logger.get_input()

        assert result["actor"] == "claude"
        assert result["event_type"] == "start"
        assert result["message"] == "Starting session"
        assert result[EVENT_ID_FIELD] == "invocation_id"
        assert EVENT_ID_VALUE not in result

    def test_five_args_includes_invocation_id_value(self, tmp_path, monkeypatch):
        """5 positional args includes EVENT_ID_VALUE in the result."""
        monkeypatch.setattr("sys.argv", ["script", "claude", "stop", "Done", "invocation_id", "inv-abc123"])
        logger = self._make_any_logger(tmp_path)

        result = logger.get_input()

        assert result["actor"] == "claude"
        assert result["event_type"] == "stop"
        assert result["message"] == "Done"
        assert result[EVENT_ID_FIELD] == "invocation_id"
        assert result[EVENT_ID_VALUE] == "inv-abc123"

    def test_too_few_args_raises(self, tmp_path, monkeypatch):
        """Fewer than 4 positional args raises InvalidInputException."""
        monkeypatch.setattr("sys.argv", ["script", "claude", "start"])
        logger = self._make_any_logger(tmp_path)

        with pytest.raises(InvalidInputException):
            logger.get_input()

    def test_too_many_args_raises(self, tmp_path, monkeypatch):
        """More than 5 positional args raises InvalidInputException."""
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "msg", "id_field", "id_value", "extra"])
        logger = self._make_any_logger(tmp_path)

        with pytest.raises(InvalidInputException):
            logger.get_input()


# ── install() ────────────────────────────────────────────────────────────


class TestInstall:
    def test_adds_section_with_allow_all_fields(self, tmp_path):
        """install() on a file with no config section adds a section with fields='*'."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_base_config(config_file)

        _make_logger(config_file, sentinel).install()

        config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
        assert config["version"] == "0.1.0"
        section = config[CONFIG_KEY]
        assert section["do_all"] is False
        assert section["default"] is False
        assert section["fields"] == ALLOW_ALL_FIELDS

    def test_creates_sentinel_as_off(self, tmp_path):
        """install() creates the sentinel file with 'off'."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_base_config(config_file)

        _make_logger(config_file, sentinel).install()

        assert sentinel.exists()
        assert sentinel.read_text().strip() == "off"

    def test_idempotent_when_already_installed(self, tmp_path):
        """install() on an already complete config should not modify it."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        content_before = config_file.read_text(encoding="utf-8")

        _make_logger(config_file, sentinel).install()

        assert config_file.read_text(encoding="utf-8") == content_before


# ── log_event() ──────────────────────────────────────────────────────────


class TestLogEvent:
    def _make_enabled_logger(self, config_file: Path, sentinel: Path) -> AgentInvocationLogger:
        sentinel.write_text("on\n", encoding="utf-8")
        return _make_logger(config_file, sentinel)

    def test_writes_all_fields_with_generated_id(self, tmp_path, monkeypatch):
        """With 4 args (no invocation_id_value), generates an id and writes all fields."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "Session started", "invocation_id"])

        logger.log_event()

        logfile = tmp_path / "logs" / "agent_invocations.jsonl"
        assert logfile.exists()
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert "_timestamp_" in record
        assert record["actor"] == "claude"
        assert record["event_type"] == "start"
        assert record["message"] == "Session started"
        assert "invocation_id" in record
        assert len(record["invocation_id"]) == 16  # generated uuid hex[:16]

    def test_writes_provided_invocation_id(self, tmp_path, monkeypatch):
        """With 5 args (invocation_id_value given), uses that value for the id field."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv",
                            ["script", "claude", "stop", "Session ended", "invocation_id", "inv-xyz-999"])

        logger.log_event()

        logfile = tmp_path / "logs" / "agent_invocations.jsonl"
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert record["invocation_id"] == "inv-xyz-999"
        assert record["actor"] == "claude"
        assert record["event_type"] == "stop"
        assert record["message"] == "Session ended"

    def test_skips_when_not_enabled(self, tmp_path, monkeypatch):
        """When sentinel is missing (NOT_INSTALLED), nothing is written."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"  # missing → NOT_INSTALLED
        _write_config_with_section(config_file)
        logger = _make_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "msg", "invocation_id"])

        logger.log_event()

        assert not (tmp_path / "logs" / "agent_invocations.jsonl").exists()

    def test_skips_when_disabled(self, tmp_path, monkeypatch):
        """When sentinel is 'off' (DISABLED), nothing is written."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        sentinel.write_text("off\n", encoding="utf-8")
        _write_config_with_section(config_file)
        logger = _make_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "msg", "invocation_id"])

        logger.log_event()

        assert not (tmp_path / "logs" / "agent_invocations.jsonl").exists()

    def test_appends_to_existing_log(self, tmp_path, monkeypatch):
        """Multiple log_event() calls append records to the same JSONL file."""
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)

        for event_type in ("start", "stop"):
            monkeypatch.setattr("sys.argv",
                                ["script", "claude", event_type, "msg", "invocation_id", f"inv-{event_type}"])
            logger.log_event()

        logfile = tmp_path / "logs" / "agent_invocations.jsonl"
        lines = logfile.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["invocation_id"] == "inv-start"
        assert json.loads(lines[1])["invocation_id"] == "inv-stop"

    def test_timestamp_format(self, tmp_path, monkeypatch):
        import re
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        logger = self._make_enabled_logger(config_file, sentinel)
        monkeypatch.chdir(tmp_path)
        monkeypatch.setattr("sys.argv", ["script", "claude", "start", "msg", "invocation_id"])

        logger.log_event()

        logfile = tmp_path / "logs" / "agent_invocations.jsonl"
        record = json.loads(logfile.read_text(encoding="utf-8").strip())
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", record["_timestamp_"])


# ── status() ─────────────────────────────────────────────────────────────


class TestStatus:
    def test_returns_enabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        sentinel.write_text("on\n", encoding="utf-8")

        assert _make_logger(config_file, sentinel).status() == Status.ENABLED

    def test_returns_disabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        sentinel.write_text("off\n", encoding="utf-8")

        assert _make_logger(config_file, sentinel).status() == Status.DISABLED

    def test_returns_not_installed_when_sentinel_missing(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)

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
        _write_config_with_section(config_file)
        sentinel.write_text("off\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(True)

        assert logger.status() == Status.ENABLED

    def test_disables_when_enabled(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        sentinel.write_text("on\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(False)

        assert logger.status() == Status.DISABLED

    def test_exits_when_not_installed(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"  # missing → NOT_INSTALLED
        _write_config_with_section(config_file)
        logger = _make_logger(config_file, sentinel)

        with pytest.raises(SystemExit):
            logger.set_enabled(True)

    def test_on_is_idempotent(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        sentinel.write_text("on\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(True)

        assert logger.status() == Status.ENABLED

    def test_off_is_idempotent(self, tmp_path):
        config_file = tmp_path / "apf.yaml"
        sentinel = tmp_path / "sentinel"
        _write_config_with_section(config_file)
        sentinel.write_text("off\n", encoding="utf-8")
        logger = _make_logger(config_file, sentinel)

        logger.set_enabled(False)

        assert logger.status() == Status.DISABLED
