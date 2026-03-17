#!/usr/bin/env python3
"""
Install / update the Agentic Programming Framework (APF) in the current project folder.

Usage:
    python apf_install.py [--target FOLDER] [--dry-run] [--yes] [--force] [--help]

Place this script in your project root and run it from there.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# ── Configuration ────────────────────────────────────────────────────────────

REPO_URL = "https://github.com/iddolev/apf.git"
REPO_SLUG = "iddolev/apf"  # for raw.githubusercontent.com
# TODO: support cloning a specific tag/branch, not only HEAD

# Source path inside the cloned repo → destination path relative to project root.
# Directories are copied recursively; files are copied individually.
PATH_MAP: list[tuple[str, str]] = [
    # Distribution files (relevant only for the user project, not for the apf project)
    (".apf", ".apf"),
    ("dist/CLAUDE.md",        "CLAUDE.md"),
    ("dist/.claude/commands", ".claude/commands"),
    ("dist/.claude/scripts",  ".claude/scripts"),
    # More files (relevant both for the user project and for the apf project)
    (".claude/commands/apf",  ".claude/commands/apf"),
    (".claude/scripts/apf",   ".claude/scripts/apf"),
]

APF_FILE = ".apf"

GIT_IGNORE = [
    "apf_install.bat",
    "apf_install.py",
    ".claude/commands/apf/",
    ".claude/scripts/apf/",
]


# ── Core logic ───────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Install / update the APF framework into the current project folder.",
    )
    p.add_argument("--target", type=Path, default=None,
                   help="Install into FOLDER instead of the current directory.")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be done without touching any files.")
    p.add_argument("--yes", "-y", action="store_true",
                   help="Skip the confirmation prompt.")
    p.add_argument("--force", action="store_true",
                   help="Reinstall even if already at the latest version.")
    p.add_argument("--version", action="store_true",
                   help="Show the currently installed APF version and exit.")
    return p.parse_args()


def clone_repo(tmp_dir: Path) -> Path:
    """Clone the APF repo into *tmp_dir* and return the path."""
    dest = tmp_dir / "apf"
    print(f"⏳ Cloning {REPO_URL} ...")
    try:
        subprocess.run(
            [
                "git", "clone",
                # --depth=1 means shallow clone — we only need the latest files, not history
                "--depth", "1",
                REPO_URL,
                str(dest),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("❌ git is not installed or not on PATH. Please install git and try again.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone repository (check your network connection):\n{e.stderr}")
        sys.exit(1)
    print("✅ Done.")
    return dest


# Match a valid keyword, then :, then at least one character (empty values are
# intentionally rejected — every key we care about must have a non-empty value).
_YAML_LINE_RE = re.compile(r"^\w+\s*:.+$")


def naive_yaml_parser(text: str) -> dict:
    """Parse simple 'key: value' YAML lines. No pyyaml dependency."""
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('#'):
            # Comment line
            continue
        m = _YAML_LINE_RE.match(line)
        if m:
            pos = line.find(':')
            key = line[:pos].strip()
            value = line[pos+1:].strip()
            # Strip surrounding quotes (single or double).
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            result[key] = value
    return result


def read_apf_version(path: Path) -> str:
    """Read the version field from a YAML .apf file (simple key: value parsing)."""
    try:
        data = naive_yaml_parser(path.read_text())
    except (OSError, UnicodeDecodeError) as e:
        raise ValueError(f"Cannot read {path}: {e}") from e
    value = data.get('version')
    if value:
        return value
    raise ValueError(f"{path} is missing a 'version' field")


def fetch_remote_version() -> str:
    """Fetch .apf from remote repo and return version"""
    try:
        url = f"https://raw.githubusercontent.com/{REPO_SLUG}/main/{APF_FILE}"
        with urlopen(url, timeout=10) as resp:
            data = naive_yaml_parser(resp.read().decode())
    except (URLError, UnicodeDecodeError) as e:
        raise ValueError("Could not fetch remote version from GitHub (check network)") from e
    if v := data.get("version"):
        return v
    raise ValueError(f"Remote {APF_FILE} is missing a 'version' field")


def copy_file(src: Path, dest: Path, *, dry_run: bool) -> None:
    """Copy a single file from *src* to *dest*, always overwriting."""
    if dry_run:
        print(f"  [dry-run] Would copy {src.name} → {dest}")
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"  📄 Copied → {dest}")


def copy_entry(src: Path, dest: Path, *, dry_run: bool) -> None:
    """Process a path from PATH_MAP. For directories, rglob finds all files
    at every depth; parent dirs are created on demand by copy_file."""
    if src.is_dir():
        for descendant in sorted(src.rglob("*")):
            if descendant.is_file():
                rel = descendant.relative_to(src)
                copy_file(descendant, dest / rel, dry_run=dry_run)
    else:
        copy_file(src, dest, dry_run=dry_run)


def _is_apf_repo(project_dir: Path) -> bool:
    """Detect if *project_dir* is the APF repo itself."""
    return (project_dir / "installation" / "apf_install.py").exists()


GIT_IGNORE_COMMENT = "# Don't include files of APF in your repo"


def update_gitignore(project_dir: Path, *, dry_run: bool) -> None:
    """Create or update .gitignore with GIT_IGNORE entries."""
    gitignore_path = project_dir / ".gitignore"

    new_section = f"{GIT_IGNORE_COMMENT}\n" + "\n".join(GIT_IGNORE) + "\n"

    if not gitignore_path.exists():
        if dry_run:
            print(f"  [dry-run] Would create .gitignore with APF entries")
            return
        gitignore_path.write_text(new_section)
        print(f"  📄 Created .gitignore")
        return

    content = gitignore_path.read_text()
    existing_lines = content.splitlines()

    existing_ignore = [line for line in existing_lines if line.strip() in set(GIT_IGNORE)]
    missing = [line for line in GIT_IGNORE if line not in set(existing_lines)]

    if not existing_ignore:
        # None of the GIT_IGNORE lines exist — add full section
        if dry_run:
            print(f"  [dry-run] Would add APF section to .gitignore")
            return
        gitignore_path.write_text(content.rstrip() + "\n\n" + new_section)
        print(f"  📄 Updated .gitignore")
        return

    if not missing:
        return

    # Find last occurrence of any GIT_IGNORE line
    last_idx = -1
    for i, line in enumerate(existing_lines):
        if line.strip() in GIT_IGNORE:
            last_idx = i

    if dry_run:
        print(f"  [dry-run] Would add some APF entries to .gitignore")
        return

    new_lines = existing_lines[: last_idx + 1] + missing + existing_lines[last_idx + 1:]
    gitignore_path.write_text("\n".join(new_lines) + "\n")
    print(f"  📄 Updated .gitignore")


def install(repo_dir: Path, project_dir: Path, new_version: str, *, dry_run: bool) -> None:
    """Walk PATH_MAP and copy every framework file into the project."""
    print(f"\n📦 Installing APF v{new_version} into {project_dir}\n")

    for src_rel, dest_rel in PATH_MAP:
        src = repo_dir / src_rel
        dest = project_dir / dest_rel

        if not src.exists():
            print(f"  ⚠️  Source not found in repo: {src_rel} — skipping")
            continue

        copy_entry(src, dest, dry_run=dry_run)

    update_gitignore(project_dir, dry_run=dry_run)


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    project_dir = args.target.resolve() if args.target else Path.cwd()
    if not project_dir.is_dir():
        print(f"❌ Target directory does not exist: {project_dir}")
        sys.exit(1)
    existing_version_path = project_dir / APF_FILE

    # --version: show installed version and exit.
    if args.version:
        if existing_version_path.exists():
            print(f"APF v{read_apf_version(existing_version_path)}")
        else:
            print("APF is not installed in this project.")
        return

    if _is_apf_repo(project_dir):
        print("❌ Refusing to install — target directory is the APF repo itself.")
        sys.exit(1)

    # Fetch remote version (no clone) to allow early exit when up to date.
    print("⏳ Checking latest version...")
    try:
        new_version = fetch_remote_version()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    print(f"   Latest: v{new_version}")

    # Read current version once (if installed).
    current_version = None
    if existing_version_path.exists():
        try:
            current_version = read_apf_version(existing_version_path)
        except ValueError as e:
            print(f"⚠️  {e}")
            print("   Ignoring .apf and proceeding as a fresh install.")


    # Skip clone entirely if already up to date.
    if current_version == new_version and not args.force:
        print(f"ℹ️  Already at version {new_version}. Use --force to reinstall.")
        return

    if args.dry_run:
        print(f"\n📦 Installing APF v{new_version} into {project_dir}\n")
        for src_rel, dest_rel in PATH_MAP:
            print(f"  [dry-run] Would copy {src_rel} → {project_dir / dest_rel}")
        print(f"  [dry-run] Might update .gitignore")
        print("\n🏁 Dry run complete — no files were modified.")
        return

    # Confirm before cloning (skip prompt for --dry-run and --yes).
    if not args.yes:
        if current_version:
            prompt = f"This will update APF (v{current_version} → v{new_version}) in {project_dir}"
        else:
            prompt = f"This will install APF v{new_version} in {project_dir}"
        print(prompt)
        try:
            answer = input("Continue? [Y/n] ").strip().lower()
            if answer not in ("y", "yes", ""):
                print("Aborted.")
                return
        except (KeyboardInterrupt, EOFError):
            print("\nAborted.")
            return

    with tempfile.TemporaryDirectory(prefix="apf-") as tmp:
        tmp_dir = Path(tmp)
        repo_dir = clone_repo(tmp_dir)
        install(repo_dir, project_dir, new_version, dry_run=False)

    print(f"\n🏁 APF v{new_version} installed successfully.")
    print(f"⚠️  You should commit .apf to your repo, to remember the APF version.")


if __name__ == "__main__":
    main()
