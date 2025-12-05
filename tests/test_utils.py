from ipmg.utils import clamp_int, resolve_hostname, timestamp_str


def test_timestamp_str_format():
    ts = timestamp_str()
    # Basic sanity: only digits + underscore
    assert len(ts) >= 8
    assert all(ch.isdigit() or ch == "_" for ch in ts)


def test_clamp_int_min_max():
    assert clamp_int(5, minimum=1, maximum=10) == 5
    assert clamp_int(-1, minimum=0, maximum=10) == 0
    assert clamp_int(999, minimum=0, maximum=10) == 10


def test_resolve_hostname_safe():
    # Should not raise, even for nonsense IP
    host = resolve_hostname("203.0.113.123")  # TEST-NET-3, often unrouted
    assert isinstance(host, str)
    assert len(host) > 0
