#!/usr/bin/env python3
"""
Install / update the Agentic Programming Framework (APF) into the current project folder.

Usage:
    python install_framework.py [--dry-run] [--force] [--help]

Place this script in your project root and run it from there.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

REPO_URL = "https://github.com/iddolev/apf.git"

# Source path inside the cloned repo → destination path relative to project root.
# Directories are copied recursively; files are copied individually.
FILE_MAP: dict[str, str] = {
    "dist/.claude/commands": ".claude/commands",
    "dist/hooks":            ".claude/hooks",
    "dist/CLAUDE.md":        "CLAUDE.md",
}

# Files where we inject content between markers instead of overwriting.
# These must also appear in FILE_MAP above.
MARKER_MERGE_FILES: set[str] = {
    "CLAUDE.md",
}

MARKER_BEGIN = "<!-- BEGIN APF -->"
MARKER_END = "<!-- END APF -->"
VERSION_FILE = ".apf-version"

# ── Core logic ───────────────────────────────────────────────────────────────


VALID_FLAGS = {"--dry-run", "--force", "--help", "--target"}

HELP_TEXT = """\
Install / update the APF framework into the current project folder.

Usage:
    python apf_install.py [OPTIONS]

Options:
    --dry-run          Show what would be done without touching any files.
    --branch BRANCH    Git branch / tag to clone (default: main).
    --force            Overwrite existing files without prompting.
    --target FOLDER    Install into FOLDER instead of the current directory.
    --help             Show this help message and exit.
"""


def parse_args() -> argparse.Namespace:
    # Validate flags before letting argparse parse them.
    raw_args = sys.argv[1:]
    skip_next = False
    for arg in raw_args:
        if skip_next:
            skip_next = False
            continue
        if arg.startswith("--") and arg not in VALID_FLAGS:
            print(f"Error: Unknown flag '{arg}'.")
            print(f"Valid flags are: {', '.join(sorted(VALID_FLAGS))}")
            sys.exit(1)
        if arg == "--branch":
            skip_next = True

    if "--help" in raw_args:
        print(HELP_TEXT)
        sys.exit(0)

    p = argparse.ArgumentParser(description=__doc__, add_help=False)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--target", type=Path, default=None)
    return p.parse_args()


def clone_repo(tmp_dir: Path) -> Path:
    """Shallow-clone the framework repo into *tmp_dir* and return the path."""
    dest = tmp_dir / "apf"
    print(f"⏳ Cloning {REPO_URL} ...")
    subprocess.run(
        [
            "git", "clone",
            REPO_URL,
            str(dest),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    print("✅ Clone complete.")
    return dest


def get_new_version(repo_dir: Path) -> str:
    """Read the version string shipped with the framework repo."""
    version_path = repo_dir / VERSION_FILE
    if version_path.exists():
        return version_path.read_text().strip()
    raise FileNotFoundError(f"Cloned repo is missing version file {version_path}")


def merge_with_markers(
    source_content: str,
    dest_path: Path,
    version: str,
    *,
    dry_run: bool,
) -> None:
    """Insert *source_content* between markers in an existing file,
    or append the marked block if the file has no markers yet."""
    managed_block = (
        f"{MARKER_BEGIN}\n"
        f"<!-- managed by agentic-framework {version} — do not edit manually -->\n"
        f"{source_content}\n"
        f"{MARKER_END}"
    )

    if dest_path.exists():
        existing = dest_path.read_text()
        if MARKER_BEGIN in existing and MARKER_END in existing:
            # Replace the existing managed block.
            before = existing[: existing.index(MARKER_BEGIN)]
            after = existing[existing.index(MARKER_END) + len(MARKER_END) :]
            new_content = before + managed_block + after
            action = "update"
        else:
            # Append managed block to the end.
            new_content = existing.rstrip() + "\n\n" + managed_block + "\n"
            action = "append"
    else:
        new_content = managed_block + "\n"
        action = "create"

    if dry_run:
        print(f"  [dry-run] Would {action} managed block in {dest_path}")
    else:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(new_content)
        print(f"  ✏️  {action.capitalize()}d managed block in {dest_path}")


def copy_entry(
    src: Path,
    dest: Path,
    *,
    dry_run: bool,
    force: bool,
) -> None:
    """Copy a single file or directory tree from *src* to *dest*."""
    if src.is_dir():
        if dry_run:
            print(f"  [dry-run] Would copy directory {src.name}/ → {dest}")
            return
        if dest.exists():
            if force:
                shutil.rmtree(dest)
            else:
                # Merge: copy tree on top of existing dir.
                pass
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(f"  📁 Copied directory → {dest}")
    else:
        if dest.exists() and not force:
            print(f"  ⚠️  Skipping {dest} (exists; use --force to overwrite)")
            return
        if dry_run:
            print(f"  [dry-run] Would copy {src.name} → {dest}")
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  📄 Copied → {dest}")


def install(repo_dir: Path, project_dir: Path, new_version: str, args: argparse.Namespace) -> None:
    """Walk FILE_MAP and copy / merge everything into the project."""
    print(f"\n📦 Installing APF v{new_version} into {project_dir}\n")

    for src_rel, dest_rel in FILE_MAP.items():
        src = repo_dir / src_rel
        dest = project_dir / dest_rel

        if not src.exists():
            print(f"  ⚠️  Source not found in repo: {src_rel} — skipping")
            continue

        if dest_rel in MARKER_MERGE_FILES:
            source_content = src.read_text()
            merge_with_markers(source_content, dest, new_version, dry_run=args.dry_run)
        else:
            copy_entry(src, dest, dry_run=args.dry_run, force=args.force)

    # Write version stamp.
    version_path = project_dir / VERSION_FILE
    if args.dry_run:
        print(f"\n  [dry-run] Would write version {new_version} → {version_path}")
    else:
        version_path.write_text(new_version)
        print(f"\n✅ Installed APF version {new_version} successfully.")


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> None:
    args = parse_args()
    project_dir = args.target.resolve() if args.target else Path.cwd()

    # Confirm before proceeding.
    existing_version_path = project_dir / VERSION_FILE
    if existing_version_path.exists():
        action = "update"
    else:
        action = "install"
    print(f"This will {action} the APF framework in {project_dir}")
    while True:
        answer = input("Continue? [y/N] ").strip().lower()
        if answer in ("y", "yes"):
            break
        if answer in ("n", "no", ""):
            print("Aborted.")
            sys.exit(0)
        print(f"Invalid input: '{answer}'. Please enter y or n.")

    with tempfile.TemporaryDirectory(prefix="apf-") as tmp:
        tmp_dir = Path(tmp)
        repo_dir = clone_repo(tmp_dir)
        new_version = get_new_version(repo_dir)

        # Check if already installed at this version.
        existing_version_path = project_dir / VERSION_FILE
        if existing_version_path.exists():
            current = existing_version_path.read_text().strip()
            if current == new_version and not args.force:
                print(f"ℹ️  Already at version {new_version}. Use --force to reinstall.")
                sys.exit(0)
            print(f"🔄 Updating {current} → {new_version}")

        install(repo_dir, project_dir, new_version, args)


if __name__ == "__main__":
    main()
