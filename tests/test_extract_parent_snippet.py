"""Characterization tests for _extract_parent_snippet in parent_context.py.

Pins the AST extraction behavior so refactoring can be done safely.
"""

import sys
from pathlib import Path

import pytest

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / ".claude" / "code-quality" / "scripts"
sys.path.insert(0, str(_SCRIPTS_DIR / "code_quality_loop"))

from parent_context import _extract_parent_snippet


class TestExtractParentSnippet:

    def _write_source(self, tmp_path, code: str) -> Path:
        p = tmp_path / "source.py"
        p.write_text(code, encoding="utf-8")
        return p

    def test_extracts_matching_method(self, tmp_path):
        code = '''\
class Foo:
    def __init__(self):
        self.x = 1

    def bar(self):
        return self.x
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"__init__"})
        assert "class Foo:" in result
        assert "def __init__" in result
        assert "self.x = 1" in result

    def test_excludes_non_matching_methods(self, tmp_path):
        code = '''\
class Foo:
    def __init__(self):
        self.x = 1

    def bar(self):
        return self.x

    def baz(self):
        return 42
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"__init__"})
        assert "def __init__" in result
        assert "def bar" not in result
        assert "def baz" not in result

    def test_multiple_methods(self, tmp_path):
        code = '''\
class Foo:
    def __init__(self):
        self.x = 1

    def bar(self):
        return self.x

    def baz(self):
        return 42
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"__init__", "baz"})
        assert "def __init__" in result
        assert "def baz" in result
        assert "def bar" not in result

    def test_class_not_found_returns_empty(self, tmp_path):
        code = '''\
class Foo:
    def bar(self):
        pass
'''
        path = self._write_source(tmp_path, code)
        assert _extract_parent_snippet(path, "NotFoo", {"bar"}) == ""

    def test_no_matching_methods_returns_empty(self, tmp_path):
        code = '''\
class Foo:
    def bar(self):
        pass
'''
        path = self._write_source(tmp_path, code)
        assert _extract_parent_snippet(path, "Foo", {"nonexistent"}) == ""

    def test_syntax_error_returns_empty(self, tmp_path):
        code = "def broken(:\n  pass"
        path = self._write_source(tmp_path, code)
        assert _extract_parent_snippet(path, "Foo", {"bar"}) == ""

    def test_contains_relevant_methods_comment(self, tmp_path):
        code = '''\
class Foo:
    def bar(self):
        pass
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"bar"})
        assert "only relevant methods shown" in result

    def test_async_method(self, tmp_path):
        code = '''\
class Foo:
    async def fetch(self):
        return await something()
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"fetch"})
        assert "async def fetch" in result

    def test_preserves_method_body(self, tmp_path):
        code = '''\
class Foo:
    def compute(self):
        x = 1
        y = 2
        return x + y
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"compute"})
        assert "x = 1" in result
        assert "y = 2" in result
        assert "return x + y" in result

    def test_nested_class_ignored(self, tmp_path):
        """Only top-level classes are searched."""
        code = '''\
class Outer:
    class Inner:
        def method(self):
            pass
'''
        path = self._write_source(tmp_path, code)
        # Inner is nested, so searching for it at module level should fail
        assert _extract_parent_snippet(path, "Inner", {"method"}) == ""

    def test_class_with_bases(self, tmp_path):
        code = '''\
class Foo(Bar, Baz):
    def method(self):
        pass
'''
        path = self._write_source(tmp_path, code)
        result = _extract_parent_snippet(path, "Foo", {"method"})
        assert "class Foo(Bar, Baz):" in result
