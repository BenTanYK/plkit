import importlib


def test_plkit():
    assert importlib.import_module("plkit") is not None
