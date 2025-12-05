from ipmg.discover import discover_local_subnet


def test_discover_local_subnet_with_custom_ip():
    # Using a fixed /24 subnet so behavior is deterministic
    ips = discover_local_subnet("192.168.1.10")

    # /24 -> 256 addresses, minus network + broadcast = 254 hosts
    assert len(ips) == 254
    assert "192.168.1.1" in ips
    assert "192.168.1.254" in ips
    # Edge: network/broadcast should not appear
    assert "192.168.1.0" not in ips
    assert "192.168.1.255" not in ips
