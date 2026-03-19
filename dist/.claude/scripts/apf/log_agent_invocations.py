"""
Logs agent invocation events to STATE/HISTORY.jsonl.

Usage: python .claude/scripts/log_agent_invocations.py "<agent-name>" "<event-type>" "<message>"
"""

import sys

from logger import Logger

LOGFILE = "logs/agents_invocations_log.jsonl"
CONFIG_KEY = "log_agent_invocations"


class AgentInvocationLogger(Logger):
    def get_input(self) -> dict:
        if len(sys.argv) != 4:
            raise ValueError(f"Invalid input: {sys.argv[1:]}")
        return dict(zip(['actor', 'event_type', 'message'], sys.argv[1:]))


if __name__ == "__main__":
    _logger = AgentInvocationLogger(
        config_key=CONFIG_KEY,
        logfile=LOGFILE)
    _logger.main()
