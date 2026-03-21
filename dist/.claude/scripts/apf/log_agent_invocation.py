"""
Logs agent invocation events to STATE/HISTORY.jsonl.

Usage: python .claude/scripts/log_agent_invocation.py "<agent-name>" "<event-type>" "<message>"
"""

import sys

from common import InvalidInputException, APF_FOLDER, ALLOW_ALL_FIELDS
from logger import Logger, EVENT_ID_FIELD, EVENT_ID_VALUE

KEY_log_agent_invocation = "log_agent_invocation"
LOGFILE = f"logs/{KEY_log_agent_invocation[4:]}.jsonl"


class AgentInvocationLogger(Logger):
    def get_input(self) -> dict:
        # Information on the invocation is obtained from sys.argv:
        # actor, event_type, message, invocation_id_field, optional invocation_id_value
        if not (5 <= len(sys.argv) <= 6):
            raise InvalidInputException(f"Invalid input (must have 4 or 5 args): {sys.argv[1:]}")
        ret = {'actor': sys.argv[1],
               'event_type': sys.argv[2],
               'message': sys.argv[3],
               EVENT_ID_FIELD: sys.argv[4]}
        if len(sys.argv) == 6:
            ret[EVENT_ID_VALUE] = sys.argv[5]
        return ret


AGENT_INVOCATION_LOGGER = AgentInvocationLogger(
    config_key=KEY_log_agent_invocation,
    logfile=LOGFILE,
    # We always want all the three fields: actor, event_type, message - therefore ALLOW_ALL_FIELDS
    field_definitions=ALLOW_ALL_FIELDS,
    sentinel_filepath=f"{APF_FOLDER}/.{KEY_log_agent_invocation}")


if __name__ == "__main__":
    AGENT_INVOCATION_LOGGER.main()
