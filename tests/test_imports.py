"""Smoke tests to verify that casperfpga and key submodules import cleanly."""


def test_import_casperfpga():
    import casperfpga
    assert hasattr(casperfpga, "CasperFpga")


def test_import_utils():
    from casperfpga import utils
    assert callable(utils.parse_fpg)


def test_import_transport():
    from casperfpga import transport_katcp, transport_tapcp
    assert hasattr(transport_katcp, "KatcpTransport")
    assert hasattr(transport_tapcp, "TapcpTransport")


def test_import_memory_devices():
    from casperfpga import register, sbram, snap, qdr


def test_import_network():
    from casperfpga import tengbe, fortygbe, network
