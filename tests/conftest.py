
import os
import git
import argparse
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

@pytest.fixture
def git_hash():
    """Git commit digest for the current HEAD commit of the git repository"""
    repo = git.Repo(".", search_parent_directories=True)
    return repo.head.commit.hexsha

@pytest.fixture
def test_args(fixtures_dir):
    args = argparse.Namespace(
        command = "engage",
        input_data = fixtures_dir,
        code = ".",
    )
    return args
