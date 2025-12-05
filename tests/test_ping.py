from ipmg.ping import parse_latency, validate_ip


def test_ip_validation():
    assert validate_ip("8.8.8.8")
    assert not validate_ip("999.999.999.999")


def test_latency_parse():
    sample = "min/avg/max/mdev = 10.0/20.5/30.0/1.0 ms"
    assert parse_latency(sample) == 20.5
