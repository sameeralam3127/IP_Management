import logging

_DISCLAIMER_SHOWN = False

DISCLAIMER_TEXT = """
⚠️  IPMG Network Use Notice

This tool sends network ICMP ping requests and may be detected by
enterprise monitoring systems.

Only run ipmg on networks and hosts where you have explicit permission
from your organization's Cybersecurity / Network Security team.

Unauthorized use may violate internal policies or law.
"""


def print_disclaimer_once() -> None:
    """
    Print a security/caution disclaimer only once per process.
    """
    global _DISCLAIMER_SHOWN
    if _DISCLAIMER_SHOWN:
        return

    _DISCLAIMER_SHOWN = True
    logging.warning("IPMG disclaimer displayed to user.")
    print(DISCLAIMER_TEXT)
