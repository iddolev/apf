"""
Project Tracker MCP Server

Manages work-breakdown tasks and test cases stored as JSONL files.
Loaded into memory at startup, indexed for fast lookup, and written
back to disk on every mutation.

Usage (stdio transport — configured in .mcp.json):
    python .claude/mcp-servers/tasks/server.py --state-dir STATE
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Data layer
# ---------------------------------------------------------------------------

TASKS_FILE = "work-breakdown.jsonl"
TESTS_FILE = "test-cases.jsonl"

VALID_TASK_STATUSES = {"not_started", "in_progress", "done", "blocked", "skipped"}
VALID_TEST_STATUSES = {"not_run", "passed", "failed", "skipped"}


@dataclass
class Store:
    """In-memory store backed by a JSONL file."""

    path: Path
    records: dict[str, dict[str, Any]] = field(default_factory=dict)
    by_status: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))
    by_phase: dict[str, list[str]] = field(default_factory=lambda: defaultdict(list))

    # -- persistence ----------------------------------------------------------

    def load(self) -> None:
        self.records.clear()
        self.by_status.clear()
        self.by_phase.clear()
        if not self.path.exists():
            return
        with open(self.path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                rid = record["id"]
                self.records[rid] = record
                self._index_add(record)

    def _flush(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            for record in self.records.values():
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # -- indexing -------------------------------------------------------------

    def _index_add(self, record: dict) -> None:
        rid = record["id"]
        status = record.get("status", "")
        if status:
            self.by_status[status].append(rid)
        phase = record.get("phase", "")
        if phase:
            self.by_phase[phase].append(rid)

    def _rebuild_indexes(self) -> None:
        self.by_status.clear()
        self.by_phase.clear()
        for record in self.records.values():
            self._index_add(record)

    # -- mutations ------------------------------------------------------------

    def upsert(self, record: dict) -> None:
        self.records[record["id"]] = record
        self._rebuild_indexes()
        self._flush()

    def get(self, rid: str) -> dict | None:
        return self.records.get(rid)

    def query(
        self,
        status: str | None = None,
        phase: str | None = None,
    ) -> list[dict]:
        ids: set[str] | None = None
        if status is not None:
            ids = set(self.by_status.get(status, []))
        if phase is not None:
            phase_ids = set(self.by_phase.get(phase, []))
            ids = phase_ids if ids is None else ids & phase_ids
        if ids is None:
            return list(self.records.values())
        return [self.records[rid] for rid in ids if rid in self.records]


# ---------------------------------------------------------------------------
# Resolve state directory from CLI args
# ---------------------------------------------------------------------------

def _parse_state_dir() -> Path:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--state-dir", default="STATE")
    args, _ = parser.parse_known_args()
    return Path(args.state_dir)


STATE_DIR = _parse_state_dir()

tasks_store = Store(path=STATE_DIR / TASKS_FILE)
tests_store = Store(path=STATE_DIR / TESTS_FILE)

tasks_store.load()
tests_store.load()

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "project-tracker",
    instructions=(
        "Manages work-breakdown tasks and test cases for the project. "
        "Use these tools to query, create, and update tasks and test cases."
    ),
)

# -- Task tools ---------------------------------------------------------------


@mcp.tool()
def get_task(task_id: str) -> dict:
    """Get a single task by its ID (e.g. 'WP-01')."""
    record = tasks_store.get(task_id)
    if record is None:
        return {"error": f"Task '{task_id}' not found"}
    return record


@mcp.tool()
def list_tasks(
    status: str | None = None,
    phase: str | None = None,
) -> list[dict]:
    """List tasks, optionally filtered by status and/or phase.

    Valid statuses: not_started, in_progress, done, blocked, skipped.
    """
    return tasks_store.query(status=status, phase=phase)


@mcp.tool()
def next_task() -> dict:
    """Return the next actionable task: the first 'not_started' task whose
    dependencies are all 'done' (or that has no dependencies)."""
    for record in tasks_store.records.values():
        if record.get("status") != "not_started":
            continue
        deps = record.get("dependencies", [])
        if all(
            (tasks_store.get(d) or {}).get("status") == "done" for d in deps
        ):
            return record
    return {"info": "No actionable tasks found"}


@mcp.tool()
def update_task(task_id: str, status: str, notes: str | None = None) -> dict:
    """Update a task's status and optionally add notes.

    Valid statuses: not_started, in_progress, done, blocked, skipped.
    """
    if status not in VALID_TASK_STATUSES:
        return {"error": f"Invalid status '{status}'. Valid: {VALID_TASK_STATUSES}"}
    record = tasks_store.get(task_id)
    if record is None:
        return {"error": f"Task '{task_id}' not found"}
    record["status"] = status
    if notes is not None:
        record["notes"] = notes
    tasks_store.upsert(record)
    return record


@mcp.tool()
def create_task(
    task_id: str,
    phase: str,
    task: str,
    dependencies: list[str] | None = None,
    assignee: str = "TBD",
    effort: str = "TBD",
    definition_of_done: str = "TBD",
) -> dict:
    """Create a new work-breakdown task."""
    if tasks_store.get(task_id) is not None:
        return {"error": f"Task '{task_id}' already exists"}
    record = {
        "id": task_id,
        "phase": phase,
        "task": task,
        "dependencies": dependencies or [],
        "assignee": assignee,
        "effort": effort,
        "definition_of_done": definition_of_done,
        "status": "not_started",
    }
    tasks_store.upsert(record)
    return record


# -- Test case tools ----------------------------------------------------------


@mcp.tool()
def get_test_case(test_id: str) -> dict:
    """Get a single test case by its ID (e.g. 'TC-01')."""
    record = tests_store.get(test_id)
    if record is None:
        return {"error": f"Test case '{test_id}' not found"}
    return record


@mcp.tool()
def list_test_cases(
    status: str | None = None,
    phase: str | None = None,
) -> list[dict]:
    """List test cases, optionally filtered by status and/or phase.

    Valid statuses: not_run, passed, failed, skipped.
    Phase here maps to the component/module the test belongs to.
    """
    return tests_store.query(status=status, phase=phase)


@mcp.tool()
def update_test_case(
    test_id: str, status: str, notes: str | None = None,
) -> dict:
    """Update a test case's status and optionally add notes.

    Valid statuses: not_run, passed, failed, skipped.
    """
    if status not in VALID_TEST_STATUSES:
        return {"error": f"Invalid status '{status}'. Valid: {VALID_TEST_STATUSES}"}
    record = tests_store.get(test_id)
    if record is None:
        return {"error": f"Test case '{test_id}' not found"}
    record["status"] = status
    if notes is not None:
        record["notes"] = notes
    tests_store.upsert(record)
    return record


@mcp.tool()
def create_test_case(
    test_id: str,
    test_case: str,
    component: str,
    category: str = "core",
    test_type: str = "unit",
    priority: str = "P1",
    expected_result: str = "TBD",
    depends_on: str = "",
    automated: str = "Yes",
) -> dict:
    """Create a new test case."""
    if tests_store.get(test_id) is not None:
        return {"error": f"Test case '{test_id}' already exists"}
    record = {
        "id": test_id,
        "test_case": test_case,
        "phase": component,  # indexed as "phase" for reuse of the same Store
        "category": category,
        "type": test_type,
        "priority": priority,
        "expected_result": expected_result,
        "depends_on": depends_on,
        "automated": automated,
        "status": "not_run",
    }
    tests_store.upsert(record)
    return record


# -- Summary tool -------------------------------------------------------------


@mcp.tool()
def project_summary() -> dict:
    """Return a high-level summary: task and test counts by status."""
    task_counts: dict[str, int] = defaultdict(int)
    for r in tasks_store.records.values():
        task_counts[r.get("status", "unknown")] += 1

    test_counts: dict[str, int] = defaultdict(int)
    for r in tests_store.records.values():
        test_counts[r.get("status", "unknown")] += 1

    return {
        "total_tasks": len(tasks_store.records),
        "tasks_by_status": dict(task_counts),
        "total_test_cases": len(tests_store.records),
        "tests_by_status": dict(test_counts),
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="stdio")
