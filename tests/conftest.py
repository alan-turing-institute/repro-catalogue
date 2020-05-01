
import os
import git
import argparse
import hashlib
import pytest

pytest_plugins = ['pytest_shutil']

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
def git_repo(workspace, fixtures_dir):
    """
    Create git repository in temporary workspace (from pytest-shutil).
    Add and commit files from fixtures.
    Return path to repo.
    """
    repo = git.Repo.init(workspace.workspace)
    workspace.run("cp -R {} data/".format(fixtures_dir))
    workspace.run("cp -R {} results/".format(fixtures_dir))
    workspace.run("git add .")
    repo.index.commit("Initial commit")
    return workspace.workspace

@pytest.fixture
def git_hash(git_repo):
    """
    Git commit digest for the current HEAD commit of the temp git repository.
    """
    repo = git.Repo(git_repo)
    return repo.head.commit.hexsha

@pytest.fixture
def test_args(git_repo):
    args = argparse.Namespace(
        command = "engage",
        input_data = os.path.join(git_repo, "data"),
        code = git_repo,
        csv = None
    )
    return args
