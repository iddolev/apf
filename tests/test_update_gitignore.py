"""Characterization tests for update_gitignore in apf_install.py.

Pins the .gitignore update behavior so refactoring can be done safely.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "installation"))

from apf_install import update_gitignore, GITIGNORE_ENTRIES, GIT_IGNORE_COMMENT


class TestUpdateGitignoreCreate:
    """Tests for when .gitignore does not exist."""

    def test_creates_gitignore(self, tmp_path):
        update_gitignore(tmp_path, dry_run=False)
        gitignore = tmp_path / ".gitignore"
        assert gitignore.exists()
        content = gitignore.read_text(encoding="utf-8")
        assert GIT_IGNORE_COMMENT in content
        for entry in GITIGNORE_ENTRIES:
            assert entry in content

    def test_dry_run_does_not_create(self, tmp_path, capsys):
        update_gitignore(tmp_path, dry_run=True)
        assert not (tmp_path / ".gitignore").exists()
        captured = capsys.readouterr()
        assert "dry-run" in captured.out


class TestUpdateGitignoreExisting:
    """Tests for when .gitignore already exists."""

    def test_no_entries_present_appends_full_section(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("node_modules/\n*.pyc\n", encoding="utf-8")
        update_gitignore(tmp_path, dry_run=False)
        content = gitignore.read_text(encoding="utf-8")
        assert "node_modules/" in content
        assert GIT_IGNORE_COMMENT in content
        for entry in GITIGNORE_ENTRIES:
            assert entry in content

    def test_all_entries_present_no_change(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        original = GIT_IGNORE_COMMENT + "\n" + "\n".join(GITIGNORE_ENTRIES) + "\n"
        gitignore.write_text(original, encoding="utf-8")
        update_gitignore(tmp_path, dry_run=False)
        assert gitignore.read_text(encoding="utf-8") == original

    def test_some_entries_present_adds_missing(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        # Write only the first entry
        gitignore.write_text(GITIGNORE_ENTRIES[0] + "\n", encoding="utf-8")
        update_gitignore(tmp_path, dry_run=False)
        content = gitignore.read_text(encoding="utf-8")
        for entry in GITIGNORE_ENTRIES:
            assert entry in content

    def test_dry_run_no_entries_does_not_modify(self, tmp_path, capsys):
        gitignore = tmp_path / ".gitignore"
        original = "existing content\n"
        gitignore.write_text(original, encoding="utf-8")
        update_gitignore(tmp_path, dry_run=True)
        assert gitignore.read_text(encoding="utf-8") == original
        captured = capsys.readouterr()
        assert "dry-run" in captured.out

    def test_preserves_existing_content(self, tmp_path):
        gitignore = tmp_path / ".gitignore"
        gitignore.write_text("# My ignores\nnode_modules/\n*.pyc\n", encoding="utf-8")
        update_gitignore(tmp_path, dry_run=False)
        content = gitignore.read_text(encoding="utf-8")
        assert "# My ignores" in content
        assert "node_modules/" in content
        assert "*.pyc" in content

    def test_missing_entries_inserted_after_last_existing(self, tmp_path):
        """When some entries exist, missing ones are inserted after the last existing entry."""
        gitignore = tmp_path / ".gitignore"
        # Put first entry in the middle of other content
        lines = ["# top", GITIGNORE_ENTRIES[0], "# bottom"]
        gitignore.write_text("\n".join(lines) + "\n", encoding="utf-8")
        update_gitignore(tmp_path, dry_run=False)
        content = gitignore.read_text(encoding="utf-8")
        content_lines = content.splitlines()
        # "# bottom" should come after the inserted entries
        first_entry_idx = content_lines.index(GITIGNORE_ENTRIES[0])
        bottom_idx = content_lines.index("# bottom")
        assert bottom_idx > first_entry_idx
