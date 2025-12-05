import ipaddress
import socket
from typing import List, Optional


def discover_local_subnet(local_ip: Optional[str] = None) -> List[str]:
    """
    Discover local /24 subnet IP hosts.

    If local_ip is provided, use that as the base; otherwise detect
    from the current host's primary IP address.
    """
    if local_ip is None:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

    network = ipaddress.ip_network(local_ip + "/24", strict=False)
    return [str(ip) for ip in network.hosts()]
