"""Characterization tests for FixHeadingAndListSpacing.apply.

Pins the markdown formatting behavior so refactoring can be done safely.
"""

import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "code-quality" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR / "format_markdown"))

from fix_heading_and_list_spacing import FixHeadingAndListSpacing


def _apply(text: str) -> str:
    return FixHeadingAndListSpacing().apply(text)


# ===================================================================
# Empty / trivial inputs
# ===================================================================

class TestTrivialInputs:

    def test_empty_string(self):
        assert _apply("") == ""

    def test_single_line(self):
        assert _apply("Hello") == "Hello"

    def test_only_blank_lines(self):
        # Trailing blank lines are collapsed
        assert _apply("\n\n") == "\n"


# ===================================================================
# Heading spacing (Rule 3: heading followed by exactly one blank line)
# ===================================================================

class TestHeadingSpacing:

    def test_heading_already_has_blank_line(self):
        text = "# Title\n\nContent"
        assert _apply(text) == "# Title\n\nContent"

    def test_heading_missing_blank_line(self):
        text = "# Title\nContent"
        assert _apply(text) == "# Title\n\nContent"

    def test_heading_multiple_blank_lines_not_collapsed_without_insertion(self):
        """Multiple blank lines after heading are preserved when no insertion needed."""
        text = "# Title\n\n\n\nContent"
        result = _apply(text)
        # The formatter only collapses when it inserts a blank line.
        # Pre-existing multiple blanks are left as-is.
        lines = result.split("\n")
        heading_idx = lines.index("# Title")
        assert lines[heading_idx + 1] == ""
        assert lines[heading_idx + 2] == ""
        assert lines[heading_idx + 3] == ""
        assert lines[heading_idx + 4] == "Content"

    def test_h2_heading(self):
        text = "## Subtitle\nContent"
        assert _apply(text) == "## Subtitle\n\nContent"

    def test_h6_heading(self):
        text = "###### Deep\nContent"
        assert _apply(text) == "###### Deep\n\nContent"

    def test_heading_followed_by_heading(self):
        text = "# Title\n## Subtitle"
        result = _apply(text)
        assert "# Title\n\n## Subtitle" in result

    def test_heading_at_end_of_file(self):
        """Heading at end with no following content — no blank line needed."""
        text = "Content\n\n# Title"
        result = _apply(text)
        assert result == "Content\n\n# Title"


# ===================================================================
# List spacing (Rules 4-5: blank before and after lists)
# ===================================================================

class TestListSpacing:

    def test_list_already_has_blank_before(self):
        text = "Paragraph\n\n- item 1\n- item 2"
        assert _apply(text) == "Paragraph\n\n- item 1\n- item 2"

    def test_list_missing_blank_before(self):
        text = "Paragraph\n- item 1\n- item 2"
        result = _apply(text)
        assert "Paragraph\n\n- item 1" in result

    def test_list_followed_by_text_gets_blank_after(self):
        text = "- item 1\n- item 2\nParagraph"
        result = _apply(text)
        assert "- item 2\n\nParagraph" in result

    def test_list_already_has_blank_after(self):
        text = "- item 1\n- item 2\n\nParagraph"
        assert _apply(text) == "- item 1\n- item 2\n\nParagraph"

    def test_numbered_list(self):
        text = "Paragraph\n1. first\n2. second\nMore text"
        result = _apply(text)
        assert "Paragraph\n\n1. first" in result
        assert "2. second\n\nMore text" in result

    def test_list_after_heading_no_double_blank(self):
        """After a heading, list should not get an extra blank (heading already adds one)."""
        text = "# Title\n\n- item"
        result = _apply(text)
        # Should be exactly: heading, blank, item
        lines = result.split("\n")
        assert lines == ["# Title", "", "- item"]

    def test_nested_list_no_blank_before(self):
        """Nested sub-lists should NOT get a blank line before them."""
        text = "- parent\n  - child\n  - child2"
        result = _apply(text)
        assert "- parent\n  - child" in result

    def test_asterisk_list(self):
        text = "Paragraph\n* item 1\n* item 2"
        result = _apply(text)
        assert "Paragraph\n\n* item 1" in result

    def test_plus_list(self):
        text = "Paragraph\n+ item 1\n+ item 2"
        result = _apply(text)
        assert "Paragraph\n\n+ item 1" in result

    def test_list_with_continuation_lines(self):
        """Continuation lines (indented, not list items) stay in the list."""
        text = "Paragraph\n- item 1\n  continued\n- item 2\nAfter"
        result = _apply(text)
        assert "Paragraph\n\n- item 1" in result
        assert "- item 2\n\nAfter" in result


# ===================================================================
# Code fences (should not be modified)
# ===================================================================

class TestCodeFences:

    def test_heading_inside_code_fence_unchanged(self):
        text = "```\n# Not a heading\nContent\n```"
        result = _apply(text)
        assert "# Not a heading\nContent" in result

    def test_list_inside_code_fence_unchanged(self):
        text = "```\n- not a list\nfoo\n```"
        result = _apply(text)
        assert "- not a list\nfoo" in result

    def test_tilde_fence(self):
        text = "~~~\n# Not a heading\n~~~"
        result = _apply(text)
        assert "# Not a heading" in result


# ===================================================================
# Frontmatter
# ===================================================================

class TestFrontmatter:

    def test_yaml_frontmatter_preserved(self):
        text = "---\ntitle: Test\n---\n# Heading\nContent"
        result = _apply(text)
        assert result.startswith("---\ntitle: Test\n---\n")
        assert "# Heading\n\nContent" in result

    def test_no_frontmatter(self):
        text = "# Heading\nContent"
        result = _apply(text)
        assert result == "# Heading\n\nContent"


# ===================================================================
# Combined scenarios
# ===================================================================

class TestCombined:

    def test_heading_then_list(self):
        text = "# Title\n- item 1\n- item 2\nParagraph"
        result = _apply(text)
        lines = result.split("\n")
        assert lines[0] == "# Title"
        assert lines[1] == ""
        assert lines[2] == "- item 1"

    def test_multiple_sections(self):
        text = "# Section 1\n\nText\n- a\n- b\n\n# Section 2\n\nMore text"
        result = _apply(text)
        assert "# Section 1\n\nText" in result
        assert "# Section 2\n\nMore text" in result

    def test_idempotent(self):
        """Applying the formatter twice should give the same result."""
        text = "# Title\nParagraph\n- item\nMore text\n## Sub\nContent"
        first = _apply(text)
        second = _apply(first)
        assert first == second
