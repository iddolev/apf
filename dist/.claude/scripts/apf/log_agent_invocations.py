"""
Logs agent invocation events to STATE/HISTORY.jsonl.

Usage: python .claude/scripts/log_agent_invocations.py "<agent-name>" "<event-type>" "<message>"
"""

import sys

from common import InvalidInputException, APF_FOLDER, ALLOW_ALL_FIELDS
from logger import Logger


KEY_log_agent_invocations = "log_agent_invocations"
LOGFILE = f"logs/{KEY_log_agent_invocations[4:]}.jsonl"


class AgentInvocationLogger(Logger):
    def get_input(self) -> dict:
        if len(sys.argv) != 4:
            raise InvalidInputException(f"Invalid input: {sys.argv[1:]}")
        return dict(zip(['actor', 'event_type', 'message'], sys.argv[1:]))


AGENT_INVOCATION_LOGGER = AgentInvocationLogger(
    config_key=KEY_log_agent_invocations,
    logfile=LOGFILE,
    # We always want all the three fields: actor, event_type, message - therefore ALLOW_ALL_FIELDS
    field_definitions=ALLOW_ALL_FIELDS,
    sentinel_filepath=f"{APF_FOLDER}/.{KEY_log_agent_invocations}")


if __name__ == "__main__":
    AGENT_INVOCATION_LOGGER.main()
