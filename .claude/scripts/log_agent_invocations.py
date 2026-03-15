"""
Logs agent invocation events to STATE/HISTORY.jsonl.

Usage: python .claude/scripts/log_agent_invocations.py "<agent-name>" "<event-type>" "<message>"
"""

import json
import os
import sys
from datetime import datetime, timezone

# To turn on / off this script, set value of ACTIVE:
# ACTIVE = False
ACTIVE = True

LOGFILE = "logs/agents_invocations_log.jsonl"


# ----------------------------------------

if not ACTIVE:
    exit(0)


def main() -> None:
    if len(sys.argv) < 4:
        print('Usage: log_agent_invocations.py "<agent-name>" "<event-type>" "<message>"')
        sys.exit(1)

    record = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "actor": sys.argv[1],
        "event": sys.argv[2],
        "message": sys.argv[3],
    }

    # Create folder if it does not exist
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
