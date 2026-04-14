"""Characterization tests for python_static_analysis_report.py.

These tests pin the current behavior of the complex functions
(_should_ignore, _format_report, _categorize, _is_auto_fixable)
so that refactoring can be done safely.
"""

import sys
from pathlib import Path

# Make the module importable
_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "code-quality" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR / "python_static_analysis"))

from python_static_analysis_report import (
    _should_ignore,
    _is_auto_fixable,
    _categorize,
    _format_finding,
    _format_report,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _finding(*, rule="C0301", tool="pylint", description="Line too long",
             severity="suggestion", file="src/foo.py", line=10, col=0,
             **extra):
    d = {"rule": rule, "tool": tool, "description": description,
         "severity": severity, "file": file, "line": line, "col": col}
    d.update(extra)
    return d


# ===================================================================
# _should_ignore
# ===================================================================

class TestShouldIgnore:
    """Pin every branch in _should_ignore."""

    def test_yaml_ignore_true(self):
        """Rules with ignore: true in YAML are ignored."""
        f = _finding(rule="C0116", tool="pylint", description="Missing function docstring")
        assert _should_ignore(f) is True

    def test_yaml_ignore_false(self):
        """Rules with ignore: false (or absent) are NOT ignored."""
        f = _finding(rule="C0301", tool="pylint", description="Line too long")
        assert _should_ignore(f) is False

    def test_ignore_paths_match(self):
        """Rules with ignore_paths matching the file path are ignored."""
        f = _finding(rule="C0115", tool="pylint", description="Missing class docstring",
                     file="C:/project/tests/test_foo.py")
        assert _should_ignore(f) is True

    def test_ignore_paths_no_match(self):
        """Rules with ignore_paths NOT matching the file path are kept."""
        f = _finding(rule="C0115", tool="pylint", description="Missing class docstring",
                     file="C:/project/src/foo.py")
        assert _should_ignore(f) is False

    def test_pyright_text_attribute_ignored(self):
        """Pyright .text access on non-TextBlock is ignored (hardcoded)."""
        f = _finding(rule="reportAttributeAccessIssue", tool="pyright",
                     description='Cannot access attribute "text" for class "ContentBlock"')
        assert _should_ignore(f) is True

    def test_pyright_other_attribute_not_ignored(self):
        """Other pyright attribute access issues are NOT ignored."""
        f = _finding(rule="reportAttributeAccessIssue", tool="pyright",
                     description='Cannot access attribute "foo" for class "Bar"')
        assert _should_ignore(f) is False

    def test_bandit_b101_in_test_file_ignored(self):
        """Bandit B101 in test files is ignored (hardcoded)."""
        f = _finding(rule="B101:assert_used", tool="bandit",
                     description="Use of assert detected.",
                     file="C:/project/tests/test_foo.py")
        assert _should_ignore(f) is True

    def test_bandit_b101_in_non_test_file_not_ignored(self):
        """Bandit B101 in production code is NOT ignored."""
        f = _finding(rule="B101:assert_used", tool="bandit",
                     description="Use of assert detected.",
                     file="C:/project/src/utils.py")
        assert _should_ignore(f) is False

    def test_bandit_b404_always_ignored(self):
        """Bandit B404 (subprocess import) is always ignored."""
        f = _finding(rule="B404", tool="bandit",
                     description="Consider possible security implications.",
                     file="C:/project/src/runner.py")
        assert _should_ignore(f) is True

    def test_unknown_rule_not_ignored(self):
        """Rules not in YAML and not matching hardcoded patterns pass through."""
        f = _finding(rule="UNKNOWN_RULE_999", tool="some_tool",
                     description="Something unusual")
        assert _should_ignore(f) is False

    def test_ignore_paths_backslash_normalization(self):
        """Windows backslashes in file path are normalized for ignore_paths."""
        f = _finding(rule="C0115", tool="pylint", description="Missing class docstring",
                     file="C:\\project\\tests\\test_foo.py")
        assert _should_ignore(f) is True


# ===================================================================
# _is_auto_fixable
# ===================================================================

class TestIsAutoFixable:

    def test_yaml_auto_fixable_true(self):
        f = _finding(rule="C0301", tool="pylint")
        assert _is_auto_fixable(f) is True

    def test_yaml_auto_fixable_false(self):
        f = _finding(rule="W0603", tool="pylint")
        assert _is_auto_fixable(f) is False

    def test_ruff_fixable_flag(self):
        f = _finding(rule="SOME_RUFF", tool="ruff", ruff_fixable=True)
        assert _is_auto_fixable(f) is True

    def test_fixit_autofix_flag(self):
        f = _finding(rule="SomeFixitRule", tool="fixit", fixit_autofix=True)
        assert _is_auto_fixable(f) is True

    def test_unknown_rule_not_fixable(self):
        f = _finding(rule="UNKNOWN_999", tool="unknown")
        assert _is_auto_fixable(f) is False


# ===================================================================
# _categorize
# ===================================================================

class TestCategorize:

    def test_yaml_category(self):
        f = _finding(rule="C0301", tool="pylint")
        assert _categorize(f) == "formatting"

    def test_bandit_fallback(self):
        f = _finding(rule="B999_unknown", tool="bandit")
        assert _categorize(f) == "security"

    def test_radon_fallback(self):
        f = _finding(rule="CC-Z", tool="radon")
        assert _categorize(f) == "complexity"

    def test_pyright_fallback(self):
        f = _finding(rule="reportUnknownThing", tool="pyright")
        assert _categorize(f) == "type-safety"

    def test_pylint_prefix_convention(self):
        f = _finding(rule="C9999", tool="pylint")
        assert _categorize(f) == "convention"

    def test_pylint_prefix_warning(self):
        f = _finding(rule="W9999", tool="pylint")
        assert _categorize(f) == "warning"

    def test_pylint_prefix_error(self):
        f = _finding(rule="E9999", tool="pylint")
        assert _categorize(f) == "error"

    def test_pylint_prefix_refactor(self):
        f = _finding(rule="R9999", tool="pylint")
        assert _categorize(f) == "design"

    def test_uncategorized(self):
        f = _finding(rule="zzz_unknown", tool="unknown_tool")
        assert _categorize(f) == "uncategorized"


# ===================================================================
# _format_finding
# ===================================================================

class TestFormatFinding:

    def test_basic_format(self):
        f = _finding(rule="C0301", tool="pylint", description="Line too long (110/100)",
                     severity="suggestion", line=42)
        result = _format_finding(f, auto_fixable=True)
        assert "Line 42:" in result
        assert "[formatting]" in result
        assert "SUGGESTION" in result
        assert "Line too long (110/100)" in result
        assert "Tool: pylint" in result
        assert "Rule: C0301" in result
        assert "Auto-fixable: Yes" in result

    def test_not_auto_fixable(self):
        f = _finding(rule="W0603", tool="pylint", description="Global statement")
        result = _format_finding(f, auto_fixable=False)
        assert "Auto-fixable: No" in result


# ===================================================================
# _format_report
# ===================================================================

class TestFormatReport:
    """Pin the structure and content of the formatted report."""

    def test_empty_findings(self):
        report = _format_report([])
        assert "## 1. Summary" in report
        assert "Total findings: 0" in report
        assert "No auto-fixable changes found." in report
        assert "No manual review changes." in report

    def test_single_auto_fixable(self):
        findings = [_finding(rule="C0301", line=10, severity="suggestion")]
        report = _format_report(findings)
        assert "Total findings: 1" in report
        assert "Suggestion: 1" in report
        assert "## 3. Auto-fixable changes" in report
        assert "Line 10:" in report

    def test_single_manual(self):
        findings = [_finding(rule="W0603", line=20, severity="warning",
                             description="Using the global statement")]
        report = _format_report(findings)
        assert "Total findings: 1" in report
        assert "Warning: 1" in report
        assert "## 4. Manual review changes" in report

    def test_mixed_findings(self):
        findings = [
            _finding(rule="C0301", line=10, severity="suggestion",
                     file="a.py", description="Line too long"),
            _finding(rule="W0603", line=20, severity="warning",
                     file="b.py", description="Using global"),
        ]
        report = _format_report(findings)
        assert "Total findings: 2" in report
        # Both sections should have content
        assert "## 3. Auto-fixable changes" in report
        assert "## 4. Manual review changes" in report

    def test_sorted_by_file_then_line(self):
        findings = [
            _finding(file="z.py", line=5),
            _finding(file="a.py", line=20),
            _finding(file="a.py", line=10),
        ]
        report = _format_report(findings)
        # a.py should come before z.py
        pos_a = report.index("a.py")
        pos_z = report.index("z.py")
        assert pos_a < pos_z
        # Within a.py, line 10 before line 20
        section2 = report[report.index("## 2."):]
        pos_10 = section2.index("Line 10:")
        pos_20 = section2.index("Line 20:")
        assert pos_10 < pos_20

    def test_file_grouping_headers(self):
        findings = [
            _finding(file="src/a.py", line=1),
            _finding(file="src/a.py", line=2),
            _finding(file="src/b.py", line=1),
        ]
        report = _format_report(findings)
        assert "### src/a.py" in report
        assert "### src/b.py" in report

    def test_severity_counts(self):
        findings = [
            _finding(severity="error", rule="W0603", line=1),
            _finding(severity="warning", rule="W0603", line=2),
            _finding(severity="warning", rule="W0603", line=3),
            _finding(severity="suggestion", rule="W0603", line=4),
        ]
        report = _format_report(findings)
        assert "Error: 1" in report
        assert "Warning: 2" in report
        assert "Suggestion: 1" in report

    def test_category_counts(self):
        findings = [
            _finding(rule="C0301", line=1),  # formatting
            _finding(rule="C0301", line=2),  # formatting
            _finding(rule="W0603", line=3),  # design
        ]
        report = _format_report(findings)
        assert "formatting: 2" in report
        assert "design: 1" in report

    def test_unparsed_section(self):
        findings = [_finding(line=1)]
        unparsed = [{"tool": "ruff", "file": "x.py",
                     "description": "Could not parse this line"}]
        report = _format_report(findings, unparsed=unparsed)
        assert "## 5. Unparsed tool output" in report
        assert "[ruff] x.py:" in report

    def test_unparsed_description_truncated(self):
        long_desc = "x" * 200
        unparsed = [{"tool": "ruff", "file": "x.py", "description": long_desc}]
        report = _format_report([_finding(line=1)], unparsed=unparsed)
        assert "..." in report

    def test_no_unparsed_section_when_empty(self):
        report = _format_report([_finding(line=1)])
        assert "## 5." not in report

    def test_uncategorized_rules_section(self):
        findings = [_finding(line=1)]
        uncategorized = [("NEW_RULE", "Some new rule description")]
        report = _format_report(findings, uncategorized_rules=uncategorized)
        assert "## 6. Uncategorized rules" in report
        assert "NEW_RULE: Some new rule description" in report

    def test_no_uncategorized_section_when_empty(self):
        report = _format_report([_finding(line=1)])
        assert "## 6." not in report

    def test_all_six_sections(self):
        findings = [
            _finding(rule="C0301", line=1),  # auto-fixable
            _finding(rule="W0603", line=2),  # manual
        ]
        unparsed = [{"tool": "t", "file": "f", "description": "d"}]
        uncategorized = [("R", "D")]
        report = _format_report(findings, unparsed=unparsed,
                                uncategorized_rules=uncategorized)
        assert "## 1. Summary" in report
        assert "## 2. Findings" in report
        assert "## 3. Auto-fixable" in report
        assert "## 4. Manual review" in report
        assert "## 5. Unparsed" in report
        assert "## 6. Uncategorized" in report
