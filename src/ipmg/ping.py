import ipaddress
import platform
import re
import subprocess
from typing import Optional, Tuple


def validate_ip(ip: str) -> bool:
    """Strict IP validation."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def parse_latency(output: str) -> Optional[float]:
    """Extract latency from ping output."""
    system = platform.system().lower()

    if system == "windows":
        match = re.search(r"Average = (\d+)ms", output)
    else:
        match = re.search(r"min/avg/max/[^=]+=\s*[\d.]+/([\d.]+)/", output)

    return float(match.group(1)) if match else None


def ping_ip(ip: str, timeout: int = 2, count: int = 1) -> Tuple[str, Optional[float]]:
    """Ping a single IP with OS-aware parameters."""

    if not validate_ip(ip):
        return ("Invalid IP", None)

    system = platform.system().lower()
    param = "-n" if system == "windows" else "-c"
    timeout_param = "-w" if system == "windows" else "-W"
    timeout_val = str(timeout * (1000 if system == "windows" else 1))

    cmd = ["ping", param, str(count), timeout_param, timeout_val, ip]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout + 1,
        )

        latency = parse_latency(result.stdout)

        if result.returncode == 0:
            return ("Active", latency)

        out = result.stdout.lower()
        if "unreachable" in out:
            return ("Unreachable", None)
        if "timed out" in out:
            return ("Timeout", None)

        return ("Inactive", None)

    except subprocess.TimeoutExpired:
        return ("Timeout", None)
