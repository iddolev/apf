"""
Logs Claude Code hook events to a JSONL file.
See: https://code.claude.com/docs/en/hooks.

Receives hook input as JSON on stdin.
"""

import json
import os
import sys
from datetime import datetime, timezone

# To turn on / off this script, set value of ACTIVE:
# ACTIVE = False
ACTIVE = True

LOGFILE = "tmp/logs/hook_events_log.jsonl"
# You can exclude fields (e.g. they don't add interesting information)
EXCLUDE_FIELDS = {"session_id", "transcript_path", "cwd"}


# ----------------------------------------

if not ACTIVE:
    exit(0)


def run() -> None:
    data: dict = json.load(sys.stdin)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"timestamp": timestamp}

    record.update({k: v for k, v in data.items() if k not in EXCLUDE_FIELDS})

    # Create folder if does not exist
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == '__main__':
    run()
