"""
enhance.py — Check a framework for updates and extract changes for APF review.

Usage:
    python .claude/skills/enhance/enhance.py <framework_name>
    python .claude/skills/enhance/enhance.py --list
    python .claude/skills/enhance/enhance.py --check-all

Arguments:
    framework_name   Name of a framework defined in enhance.yaml
    --list           List all tracked frameworks and their status
    --check-all      Check all frameworks for updates (version check only)

Output:
    Prints structured information for Claude to review:
    - Framework metadata
    - Latest version vs processed version
    - If updates exist: git log and diff between versions
    - If no processed version: full repo file listing and key files
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

SCRIPT_DIR: Path = Path(__file__).resolve().parent
YAML_PATH: Path = SCRIPT_DIR / "enhance.yaml"


def load_config() -> dict[str, Any]:
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_config(config: dict[str, Any]) -> None:
    with open(YAML_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def run(
    cmd: list[str] | str,
    cwd: Path | str | None = None,
    check: bool = True,
    capture: bool = True,
) -> str | None:
    """Run a shell command and return stdout."""
    result = subprocess.run(
        cmd, cwd=cwd, capture_output=capture, text=True, check=check,
        shell=isinstance(cmd, str),
    )
    return result.stdout.strip() if capture else None


def get_remote_tags(repo_url: str) -> list[str]:
    """Get all tags from a remote repo via ls-remote."""
    try:
        output = run(["git", "ls-remote", "--tags", "--sort=-v:refname", repo_url])
    except subprocess.CalledProcessError:
        return []

    tags: list[str] = []
    for line in output.splitlines():
        if not line:
            continue
        ref = line.split("\t")[1]
        # Skip ^{} dereferenced tags
        if ref.endswith("^{}"):
            continue
        tag = ref.replace("refs/tags/", "")
        tags.append(tag)
    return tags


def get_latest_tag(repo_url: str) -> str | None:
    """Get the latest tag from a remote repo."""
    tags = get_remote_tags(repo_url)
    return tags[0] if tags else None


def get_default_branch(repo_url: str) -> str:
    """Get the default branch name from a remote repo."""
    try:
        output = run(["git", "ls-remote", "--symref", "HEAD", repo_url])
        for line in output.splitlines():
            if line.startswith("ref:"):
                return line.split("\t")[0].replace("ref: refs/heads/", "")
    except subprocess.CalledProcessError:
        pass
    return "main"


def clone_repo(
    repo_url: str,
    dest: Path,
    branch: str | None = None,
    shallow: bool = True,
) -> None:
    """Clone a repo. Optionally shallow and/or a specific branch."""
    cmd: list[str] = ["git", "clone"]
    if shallow:
        cmd += ["--depth", "100"]
    if branch:
        cmd += ["--branch", branch]
    cmd += [repo_url, str(dest)]
    run(cmd)


def fetch_tag(repo_dir: Path, tag: str) -> None:
    """Fetch a specific tag in an existing clone."""
    run(["git", "fetch", "--depth", "100", "origin", f"tag {tag}"], cwd=repo_dir)


def list_repo_files(
    repo_dir: Path,
    extensions: set[str] | None = None,
) -> list[str]:
    """List files in the repo, optionally filtered by extension."""
    if extensions is None:
        extensions = {".md", ".py", ".js", ".ts", ".yaml", ".yml", ".toml", ".json", ".sh"}
    all_files: list[str] = []
    for root, dirs, files in os.walk(repo_dir):
        # Skip .git
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            fpath = Path(root) / f
            if extensions is None or fpath.suffix.lower() in extensions:
                all_files.append(str(fpath.relative_to(repo_dir)))
    return sorted(all_files)


def print_section(title: str, content: str = "") -> None:
    """Print a clearly delimited section."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    if content:
        print(content)


def handle_no_processed_version(
    framework_name: str,
    fw_config: dict[str, Any],
    repo_url: str,
) -> dict[str, str]:
    """First-time review: clone the full repo and output its contents for review."""
    latest_tag: str | None = get_latest_tag(repo_url)
    default_branch: str = get_default_branch(repo_url)
    target: str = latest_tag or default_branch

    print_section(f"FIRST-TIME REVIEW: {framework_name}")
    print(f"Repo:           {repo_url}")
    print(f"Latest tag:     {latest_tag or '(no tags found)'}")
    print(f"Default branch: {default_branch}")
    print(f"Cloning at:     {target}")

    with tempfile.TemporaryDirectory(prefix=f"apf-enhance-{framework_name}-") as tmpdir:
        clone_dir: Path = Path(tmpdir) / framework_name
        clone_repo(repo_url, clone_dir, branch=target, shallow=False)

        # List all relevant files
        files: list[str] = list_repo_files(clone_dir)
        print_section("FILE LISTING", "\n".join(files))

        # Output key files content
        key_files: list[str] = ["README.md", "CLAUDE.md", "AGENTS.md"]
        # Also look for any markdown in root or docs/
        for f in files:
            fpath = Path(f)
            if fpath.suffix.lower() == ".md" and (
                fpath.parent == Path(".") or str(fpath).startswith("docs/")
            ):
                if f not in key_files:
                    key_files.append(f)

        for kf in key_files:
            full_path: Path = clone_dir / kf
            if full_path.exists():
                try:
                    content: str = full_path.read_text(encoding="utf-8", errors="replace")
                    print_section(f"FILE: {kf}", content)
                except Exception as e:
                    print_section(f"FILE: {kf}", f"(error reading: {e})")

        # Output git log summary
        try:
            log: str | None = run(["git", "log", "--oneline", "-50"], cwd=clone_dir)
            print_section("RECENT COMMITS (up to 50)", log)
        except subprocess.CalledProcessError:
            pass

    # Output suggested version to record
    print_section("SUGGESTED VERSION TO RECORD")
    print(f"After reviewing, update processed_version to: {target}")
    print(
        f"(Run: python .claude/skills/enhance/enhance.py"
        f" --set-version {framework_name} {target})"
    )

    return {"status": "first_review", "target": target}


def _print_commit_log(clone_dir: Path, old_version: str, new_version: str) -> None:
    """Print the commit log between two versions."""
    try:
        log: str | None = run(
            ["git", "log", "--oneline", f"{old_version}..{new_version}"],
            cwd=clone_dir,
        )
        print_section(f"COMMITS: {old_version}..{new_version}", log)
    except subprocess.CalledProcessError:
        print_section("COMMITS", "(could not generate log)")


def _print_diff_stat(clone_dir: Path, old_version: str, new_version: str) -> None:
    """Print the diff stat between two versions."""
    try:
        stat: str | None = run(
            ["git", "diff", "--stat", f"{old_version}..{new_version}"],
            cwd=clone_dir,
        )
        print_section("DIFF STAT", stat)
    except subprocess.CalledProcessError:
        pass


def _print_full_diff(clone_dir: Path, old_version: str, new_version: str) -> None:
    """Print the full diff between two versions, truncated if huge."""
    try:
        diff: str | None = run(
            ["git", "diff", f"{old_version}..{new_version}"],
            cwd=clone_dir,
        )
        max_lines: int = 2000
        diff_lines: list[str] = diff.splitlines()
        if len(diff_lines) > max_lines:
            diff = "\n".join(diff_lines[:max_lines])
            diff += f"\n\n... (truncated, {len(diff_lines) - max_lines} more lines)"
        print_section("FULL DIFF", diff)
    except subprocess.CalledProcessError:
        pass


def _print_changed_markdown(clone_dir: Path, old_version: str, new_version: str) -> None:
    """Print full content of changed markdown files (they often contain methodology changes)."""
    try:
        changed_files: str | None = run(
            ["git", "diff", "--name-only", f"{old_version}..{new_version}"],
            cwd=clone_dir,
        )
        md_files: list[str] = [f for f in changed_files.splitlines() if f.endswith(".md")]
        for mf in md_files:
            full_path: Path = clone_dir / mf
            if full_path.exists():
                content: str = full_path.read_text(encoding="utf-8", errors="replace")
                print_section(f"CHANGED FILE (full): {mf}", content)
    except subprocess.CalledProcessError:
        pass


def _review_update(
    clone_dir: Path,
    old_version: str,
    new_version: str,
) -> dict[str, str] | None:
    """Clone, fetch old tag, and print all diff sections. Returns early result on failure."""
    try:
        fetch_tag(clone_dir, old_version)
    except subprocess.CalledProcessError:
        print(f"\nWARNING: Could not fetch old tag '{old_version}'. Showing full log instead.")
        log: str | None = run(["git", "log", "--oneline", "-50"], cwd=clone_dir)
        print_section("RECENT COMMITS", log)
        return {"status": "update_partial", "old": old_version, "new": new_version}

    _print_commit_log(clone_dir, old_version, new_version)
    _print_diff_stat(clone_dir, old_version, new_version)
    _print_full_diff(clone_dir, old_version, new_version)
    _print_changed_markdown(clone_dir, old_version, new_version)
    return None


def handle_update(
    framework_name: str,
    fw_config: dict[str, Any],
    repo_url: str,
    old_version: str,
    new_version: str,
) -> dict[str, str]:
    """Incremental review: show changes between old and new version."""
    print_section(f"UPDATE FOUND: {framework_name}")
    print(f"Repo:              {repo_url}")
    print(f"Processed version: {old_version}")
    print(f"Latest version:    {new_version}")

    with tempfile.TemporaryDirectory(prefix=f"apf-enhance-{framework_name}-") as tmpdir:
        clone_dir: Path = Path(tmpdir) / framework_name
        clone_repo(repo_url, clone_dir, branch=new_version, shallow=False)

        early_result: dict[str, str] | None = _review_update(clone_dir, old_version, new_version)
        if early_result is not None:
            return early_result

    print_section("SUGGESTED VERSION TO RECORD")
    print(f"After reviewing, update processed_version to: {new_version}")
    print(
        f"(Run: python .claude/skills/enhance/enhance.py"
        f" --set-version {framework_name} {new_version})"
    )

    return {"status": "update_available", "old": old_version, "new": new_version}


def set_version(framework_name: str, version: str) -> None:
    """Update the processed_version for a framework in enhance.yaml."""
    config: dict[str, Any] = load_config()
    frameworks: dict[str, Any] = config.get("frameworks", {})
    if framework_name not in frameworks:
        print(f"ERROR: Framework '{framework_name}' not found in enhance.yaml")
        sys.exit(1)
    frameworks[framework_name]["processed_version"] = version
    save_config(config)
    print(f"Updated {framework_name} processed_version to: {version}")


def check_framework(framework_name: str) -> dict[str, str]:
    """Main logic for checking a single framework."""
    config: dict[str, Any] = load_config()
    frameworks: dict[str, Any] = config.get("frameworks", {})

    if framework_name not in frameworks:
        print(f"ERROR: Framework '{framework_name}' not found in enhance.yaml")
        print(f"Available frameworks: {', '.join(frameworks.keys())}")
        sys.exit(1)

    fw: dict[str, Any] = frameworks[framework_name]
    repo_url: str | None = fw.get("repo")
    if not repo_url:
        print(f"ERROR: No repo URL for framework '{framework_name}'")
        sys.exit(1)

    processed_version: str | None = fw.get("processed_version") or None

    if processed_version is None:
        # First time — full review
        return handle_no_processed_version(framework_name, fw, repo_url)

    # Check for updates
    latest_tag: str | None = get_latest_tag(repo_url)
    if latest_tag is None:
        print_section(f"CHECK: {framework_name}")
        print("No tags found in remote repo. Cannot compare versions.")
        print(f"Repo: {repo_url}")
        print(f"Processed version: {processed_version}")
        return {"status": "no_tags"}

    if latest_tag == processed_version:
        print_section(f"UP TO DATE: {framework_name}")
        print(f"Repo:              {repo_url}")
        print(f"Current version:   {processed_version}")
        print(f"Latest version:    {latest_tag}")
        return {"status": "up_to_date"}

    return handle_update(framework_name, fw, repo_url, processed_version, latest_tag)


def list_frameworks() -> None:
    """List all tracked frameworks."""
    config: dict[str, Any] = load_config()
    frameworks: dict[str, Any] = config.get("frameworks", {})
    print_section("TRACKED FRAMEWORKS")
    for name, fw in frameworks.items():
        version: str = fw.get("processed_version") or "(not yet processed)"
        repo: str = fw.get("repo", "(no repo)")
        synonyms: str = fw.get("synonyms", "")
        syn_str: str = f" (aka {synonyms})" if synonyms else ""
        print(f"  {name}{syn_str}")
        print(f"    Repo:    {repo}")
        print(f"    Version: {version}")
        print()


def check_all() -> None:
    """Quick version check for all frameworks."""
    config: dict[str, Any] = load_config()
    frameworks: dict[str, Any] = config.get("frameworks", {})
    print_section("VERSION CHECK — ALL FRAMEWORKS")
    for name, fw in frameworks.items():
        repo_url: str | None = fw.get("repo")
        processed: str | None = fw.get("processed_version") or None
        if not repo_url:
            print(f"  {name}: (no repo URL)")
            continue
        latest: str | None = get_latest_tag(repo_url)
        if processed is None:
            status: str = "NEEDS FIRST REVIEW"
        elif latest is None:
            status = "no remote tags found"
        elif latest == processed:
            status = "up to date"
        else:
            status = f"UPDATE AVAILABLE: {processed} -> {latest}"
        print(f"  {name}: {status}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg: str = sys.argv[1]

    if arg == "--list":
        list_frameworks()
    elif arg == "--check-all":
        check_all()
    elif arg == "--set-version":
        if len(sys.argv) < 4:
            print("Usage: enhance.py --set-version <framework_name> <version>")
            sys.exit(1)
        set_version(sys.argv[2], sys.argv[3])
    else:
        check_framework(arg)


if __name__ == "__main__":
    main()
