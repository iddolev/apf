# Fix Bugs in format_markdown.py

Bugs found in `.claude/scripts/apf/format_markdown.py`.

## Bug 1 — `wrap_long_lines`: `initial_indent` computed but never used (High)

`initial_indent = _detect_indent(line)` is computed at line 126 but `""` is passed to
`textwrap.fill` instead. Because `textwrap.fill` uses `drop_whitespace=True` by default, the
leading whitespace of the input text is stripped. The first wrapped line therefore loses its
original indentation, breaking nested list items and other indented content.

**Fix:**

```python
wrapped = textwrap.fill(
    line.lstrip(),
    width=MAX_LINE_LENGTH,
    initial_indent=initial_indent,
    subsequent_indent=subsequent_indent,
    break_long_words=False,
    break_on_hyphens=False,
)
```

## Bug 2 — Rule 3 does not remove extra blank lines after headings (Medium)

The heading rule in `fix_heading_and_list_spacing` fires only when `result[-1]` is a heading.
Once the first blank line is appended, `result[-1]` is `""` and the rule never fires again for
subsequent blanks. Extra blank lines after a heading are therefore left intact, violating the
"exactly one blank line" guarantee.

**Trace for `# Heading`, `""`, `""`, `content`:**

- Process 1st blank: `result[-1]` is heading, `trailing_blanks=0`, not `>=1` → blank appended
- Process 2nd blank: `result[-1]` is `""` → heading check skipped → blank appended unchanged

**Fix:** After appending a heading, strip any excess blank lines when a non-blank line is
encountered (i.e., enforce the invariant at the point the content line arrives, not only at the
first blank).

## Bug 3 — `_is_url_line`: only the longest URL is removed when checking (Low)

When a line contains multiple URLs, only the longest is removed before measuring the non-URL
length. If two medium-length URLs together make the line long, removing only the longest may
still leave `without_url` over the limit, causing the line to be (incorrectly) wrapped and
splitting a URL.

**Fix:** Remove all found URLs before measuring:

```python
without_urls = line
for url in urls:
    without_urls = without_urls.replace(url, "", 1)
return len(without_urls) <= MAX_LINE_LENGTH
```

## Minor — O(n²) in `_is_inside_code_fence`

`_is_inside_code_fence` re-scans from line 0 on every call. Called once per line in
`wrap_long_lines`, this is O(n²) for large files. Not a logic bug, but should be replaced with
a stateful pass.
