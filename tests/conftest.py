
import os
import hashlib
import pytest

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
_FIXTURES_DIR = os.path.join(_ROOT_DIR, "fixtures")

@pytest.fixture
def fixtures_dir():
    return _FIXTURES_DIR

@pytest.fixture
def fixture1():
    return os.path.join(_FIXTURES_DIR, "fixture1.json")

@pytest.fixture
def fixture2():
    return os.path.join(_FIXTURES_DIR, "fixture2.json")

@pytest.fixture
def empty_hash():
    """Hash produced if no input is provided"""
    return hashlib.sha512().hexdigest()
