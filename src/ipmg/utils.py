import logging
import socket
from datetime import datetime
from typing import Optional


def configure_logging(verbose: bool = False, logfile: str = "ipmg.log") -> None:
    """
    Configure root logger for the tool.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=logfile,
    )


def resolve_hostname(ip: str) -> str:
    """
    Resolve an IP to hostname. Safe and failure-tolerant.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unresolvable"


def current_timestamp() -> datetime:
    """
    Get current UTC/local timestamp. Can be mocked in tests.
    """
    return datetime.now()


def timestamp_str(fmt: str = "%Y%m%d_%H%M%S") -> str:
    """
    Return a filesystem-safe timestamp string.
    """
    return current_timestamp().strftime(fmt)


def clamp_int(value: int, minimum: Optional[int] = None, maximum: Optional[int] = None) -> int:
    """
    Clamp an integer between optional min/max boundaries.
    Useful to prevent extreme thread counts, etc.
    """
    if minimum is not None:
        value = max(value, minimum)
    if maximum is not None:
        value = min(value, maximum)
    return value
