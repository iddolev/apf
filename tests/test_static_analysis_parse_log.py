"""Characterization tests for _collect_unparsed in python_static_analysis_parse_log.py.

Pins the filtering behavior so refactoring can be done safely.
"""

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "code-quality" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR / "python_static_analysis"))

from python_static_analysis_parse_log import _collect_unparsed


FILE_ID = "C:/project/src/foo.py"
TOOL_ID = "pylint"


class TestCollectUnparsed:

    def test_empty_lines_returns_empty(self):
        assert _collect_unparsed([], FILE_ID, TOOL_ID) == []

    def test_blank_lines_only_returns_empty(self):
        assert _collect_unparsed(["", "  ", "\t"], FILE_ID, TOOL_ID) == []

    def test_real_unparsed_content_returns_finding(self):
        lines = ["Some unexpected output from the tool"]
        result = _collect_unparsed(lines, FILE_ID, TOOL_ID)
        assert len(result) == 1
        assert result[0]["file"] == FILE_ID
        assert result[0]["tool"] == TOOL_ID
        assert result[0]["rule"] == "unparsed"
        assert result[0]["severity"] == "warning"
        assert result[0]["line"] == 0
        assert "Some unexpected output" in result[0]["description"]

    def test_multiple_unparsed_lines_joined(self):
        lines = ["First unparsed line", "Second unparsed line"]
        result = _collect_unparsed(lines, FILE_ID, TOOL_ID)
        assert len(result) == 1
        assert " | " in result[0]["description"]
        assert "First unparsed line" in result[0]["description"]
        assert "Second unparsed line" in result[0]["description"]

    def test_pyright_summary_filtered(self):
        """Pyright summary lines like '8 errors, 0 warnings, 0 informations' are noise."""
        lines = ["8 errors, 0 warnings, 0 informations"]
        assert _collect_unparsed(lines, FILE_ID, "pyright") == []

    def test_pyright_summary_variations(self):
        lines = ["1 error, 2 warnings, 3 informations"]
        assert _collect_unparsed(lines, FILE_ID, "pyright") == []

    def test_pyright_file_header_filtered(self):
        """Pyright file path headers (e.g. 'C:\\project\\foo.py') are noise."""
        lines = ["C:\\project\\foo.py"]
        assert _collect_unparsed(lines, FILE_ID, "pyright") == []

    def test_pyright_file_header_with_finding_kept(self):
        """Pyright lines that contain ' - ' are findings, not headers."""
        lines = ["C:\\project\\foo.py - error: something"]
        result = _collect_unparsed(lines, FILE_ID, "pyright")
        assert len(result) == 1

    def test_pyright_continuation_lines_filtered(self):
        """Pyright continuation lines starting with 'Attribute ', 'Type "', '"' are noise."""
        lines = ['Attribute "foo" is unknown', 'Type "int" is incompatible', '"str"']
        assert _collect_unparsed(lines, FILE_ID, "pyright") == []

    def test_ruff_line_number_markers_filtered(self):
        """Ruff context lines like '10 | some_code()' are noise."""
        lines = ["10 | some_code()", "11  | more_code()"]
        assert _collect_unparsed(lines, FILE_ID, "ruff") == []

    def test_ruff_pointer_lines_filtered(self):
        """Ruff pointer lines (just | and ^ characters) are noise."""
        lines = ["   |   ^^^^", "  | ^"]
        assert _collect_unparsed(lines, FILE_ID, "ruff") == []

    def test_bandit_source_context_filtered(self):
        """Bandit source context lines (line_num<tab>code) are noise."""
        lines = ["56\tresult = subprocess.run(cmd, shell=True)"]
        assert _collect_unparsed(lines, FILE_ID, "bandit") == []

    def test_mixed_noise_and_real(self):
        """Only real content survives after all filters."""
        lines = [
            "",                                   # blank -> noise
            "8 errors, 0 warnings, 0 informations",  # pyright summary -> noise
            "10 | some_code()",                    # ruff context -> noise
            "Real unparsed output here",           # real content
        ]
        result = _collect_unparsed(lines, FILE_ID, TOOL_ID)
        assert len(result) == 1
        assert "Real unparsed output" in result[0]["description"]

    def test_all_noise_returns_empty(self):
        """When every line is noise, nothing is returned."""
        lines = [
            "",
            "  ",
            "10 | code",
            "   | ^^^^",
            "56\tcode_line",
        ]
        assert _collect_unparsed(lines, FILE_ID, TOOL_ID) == []
