"""
Sets up GitHub CI/CD: Actions workflow for tests + branch protection rules.

Detects the project's test setup, generates a workflow file, and configures
branch protection via the GitHub CLI.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)


def check_gh_installed() -> bool:
    """Return True if the GitHub CLI (gh) is installed and accessible."""
    result = run("gh --version", check=False)
    return result.returncode == 0


def detect_github_remote() -> tuple[str, str] | None:
    """Return (owner, repo) if a GitHub remote is found, else None."""
    result = run("git remote -v", check=False)
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        m = re.search(r"github\.com[:/]([^/]+)/([^/\s]+?)(?:\.git)?(?:\s|$)", line)
        if m:
            return m.group(1), m.group(2)
    return None


def detect_main_branch() -> str:
    """Detect the main branch name (main or master)."""
    result = run("git symbolic-ref refs/remotes/origin/HEAD", check=False)
    if result.returncode == 0:
        ref = result.stdout.strip()
        return ref.split("/")[-1]
    # Fallback: check which branch exists
    for name in ("main", "master"):
        r = run(f"git rev-parse --verify origin/{name}", check=False)
        if r.returncode == 0:
            return name
    return "main"


def detect_test_setup() -> dict:
    """Detect language, dependencies install command, and test command.

    Returns a dict with keys:
        runtime_name, runtime_version, setup_action, install_cmd, test_cmd
    """
    # Python — pyproject.toml
    if Path("pyproject.toml").exists():
        content = Path("pyproject.toml").read_text(encoding="utf-8")
        has_pytest = "pytest" in content
        has_deps = "[project.dependencies]" in content or "dependencies" in content

        python_version = _detect_python_version(content)

        if has_deps:
            install_cmd = "pip install . && pip install pytest"
        elif Path("requirements.txt").exists():
            install_cmd = "pip install -r requirements.txt && pip install pytest"
        else:
            install_cmd = "pip install pytest"

        if has_pytest:
            return {
                "runtime_name": "python",
                "runtime_version": python_version,
                "setup_action": "actions/setup-python@v5",
                "install_cmd": install_cmd,
                "test_cmd": "pytest -v",
            }

    # Python — requirements.txt only
    if Path("requirements.txt").exists():
        content = Path("requirements.txt").read_text(encoding="utf-8")
        python_version = "3.12"
        install_cmd = "pip install -r requirements.txt"
        if "pytest" not in content:
            install_cmd += " && pip install pytest"
        return {
            "runtime_name": "python",
            "runtime_version": python_version,
            "setup_action": "actions/setup-python@v5",
            "install_cmd": install_cmd,
            "test_cmd": "pytest -v",
        }

    # Python — pytest.ini or setup.cfg
    if Path("pytest.ini").exists() or (
        Path("setup.cfg").exists() and "pytest" in Path("setup.cfg").read_text(encoding="utf-8")
    ):
        return {
            "runtime_name": "python",
            "runtime_version": "3.12",
            "setup_action": "actions/setup-python@v5",
            "install_cmd": "pip install pytest",
            "test_cmd": "pytest -v",
        }

    # Node.js — package.json with test script
    if Path("package.json").exists():
        try:
            pkg = json.loads(Path("package.json").read_text(encoding="utf-8"))
            if pkg.get("scripts", {}).get("test"):
                node_version = _detect_node_version()
                lock = "package-lock.json"
                install_cmd = "npm ci" if Path(lock).exists() else "npm install"
                return {
                    "runtime_name": "node",
                    "runtime_version": node_version,
                    "setup_action": "actions/setup-node@v4",
                    "install_cmd": install_cmd,
                    "test_cmd": "npm test",
                }
        except (json.JSONDecodeError, KeyError):
            pass

    return {}


def _detect_python_version(pyproject_content: str) -> str:
    m = re.search(r'requires-python\s*=\s*">=(\d+\.\d+)"', pyproject_content)
    if m:
        return m.group(1)
    return "3.12"


def _detect_node_version() -> str:
    if Path(".nvmrc").exists():
        return Path(".nvmrc").read_text(encoding="utf-8").strip()
    return "20"


def generate_workflow(main_branch: str, setup: dict) -> str:
    """Generate the GitHub Actions workflow YAML content."""
    runtime_name = setup["runtime_name"]
    runtime_version = setup["runtime_version"]
    setup_action = setup["setup_action"]
    install_cmd = setup["install_cmd"]
    test_cmd = setup["test_cmd"]

    if runtime_name == "python":
        version_key = "python-version"
    elif runtime_name == "node":
        version_key = "node-version"
    else:
        version_key = "version"

    return f"""name: Tests

on:
  pull_request:
    branches: [{main_branch}]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: {setup_action}
        with:
          {version_key}: "{runtime_version}"

      - name: Install dependencies
        run: {install_cmd}

      - name: Run tests
        run: {test_cmd}
"""


def write_workflow(main_branch: str, setup: dict) -> Path:
    """Write the workflow file and return its path."""
    workflow_dir = Path(".github/workflows")
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_path = workflow_dir / "tests.yml"
    content = generate_workflow(main_branch, setup)
    workflow_path.write_text(content, encoding="utf-8")
    return workflow_path


def set_branch_protection(owner: str, repo: str, main_branch: str) -> bool:
    """Set branch protection rules via gh CLI. Returns True on success."""
    if not check_gh_installed():
        print("Error: GitHub CLI (gh) is not installed.", file=sys.stderr)
        return False

    payload = json.dumps({
        "required_status_checks": {
            "strict": True,
            "contexts": ["test"],
        },
        "enforce_admins": False,
        "required_pull_request_reviews": {
            "required_approving_review_count": 1,
        },
        "restrictions": None,
    })

    result = subprocess.run(
        f'gh api repos/{owner}/{repo}/branches/{main_branch}/protection -X PUT --input -',
        shell=True, capture_output=True, text=True, input=payload,
    )

    if result.returncode != 0:
        print(f"Error setting branch protection: {result.stderr}", file=sys.stderr)
        return False
    return True


def main() -> dict:
    """Run detection steps and print results as JSON for the LLM to use.

    Returns a dict with all detected info and actions taken.
    """
    result = {"success": False}

    # Step 0: Check gh CLI
    result["gh_installed"] = check_gh_installed()

    # Step 1: Detect GitHub
    remote = detect_github_remote()
    if not remote:
        result["error"] = "not_github"
        result["message"] = (
            "This repository does not appear to be hosted on GitHub. "
            "This skill currently supports only GitHub CI/CD setup."
        )
        print(json.dumps(result, indent=2))
        return result

    owner, repo = remote
    result["owner"] = owner
    result["repo"] = repo

    # Step 2: Detect main branch
    main_branch = detect_main_branch()
    result["main_branch"] = main_branch

    # Step 3: Detect test setup
    setup = detect_test_setup()
    result["test_setup"] = setup

    if not setup:
        result["error"] = "no_test_setup"
        result["message"] = "Could not auto-detect a test setup."
        print(json.dumps(result, indent=2))
        return result

    # Step 4: Generate workflow (but don't write yet — let LLM confirm with user)
    result["workflow_content"] = generate_workflow(main_branch, setup)
    result["success"] = True
    result["message"] = "Detection complete. Ready to set up CI/CD."

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    if "--detect" in sys.argv:
        main()
    elif "--write-workflow" in sys.argv:
        remote = detect_github_remote()
        if not remote:
            sys.exit("Not a GitHub repo")
        main_branch = detect_main_branch()
        setup = detect_test_setup()
        if not setup:
            sys.exit("No test setup detected")
        path = write_workflow(main_branch, setup)
        print(f"Wrote {path}")
    elif "--protect" in sys.argv:
        remote = detect_github_remote()
        if not remote:
            sys.exit("Not a GitHub repo")
        owner, repo = remote
        main_branch = detect_main_branch()
        ok = set_branch_protection(owner, repo, main_branch)
        if ok:
            print(f"Branch protection set on {main_branch}")
        else:
            sys.exit("Failed to set branch protection")
    elif "--all" in sys.argv:
        remote = detect_github_remote()
        if not remote:
            sys.exit("Not a GitHub repo")
        owner, repo = remote
        main_branch = detect_main_branch()
        setup = detect_test_setup()
        if not setup:
            sys.exit("No test setup detected")
        path = write_workflow(main_branch, setup)
        print(f"Wrote {path}")
        ok = set_branch_protection(owner, repo, main_branch)
        if ok:
            print(f"Branch protection set on {main_branch}")
        else:
            sys.exit("Failed to set branch protection")
    else:
        print("Usage: setup_github_ci.py [--detect | --write-workflow | --protect | --all]")
        sys.exit(1)
