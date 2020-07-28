
import os
import sys
import git
import glob
import pytest

from git import InvalidGitRepositoryError
from catalogue.engage import engage, disengage, git_query


def test_git_query(git_repo, capsys, workspace, monkeypatch):

    repo = git.Repo(git_repo)
    git_hash_0 = repo.head.commit.hexsha
    catalogue_results = 'catalogue_results'

    #==================================================
    # 1: use with default commit_changes=False
    #==================================================

    # repo is clean
    assert git_query(git_repo, catalogue_results) == True

    # create new file -- untracked; file path includes `catalogue_results` but
    # it is not the directory name
    workspace.run("touch catalogue_results.json")
    assert git_query(git_repo, catalogue_results) == False

    # git add file without commit
    workspace.run("git add .")
    assert git_query(git_repo, catalogue_results) == False

    # commit new file
    repo.index.commit("Add new file")
    git_hash_1 = repo.head.commit.hexsha
    assert git_hash_0 != git_hash_1
    assert git_query(git_repo, catalogue_results) == True

    # create new file in `catalogue_results` dir
    workspace.run("mkdir catalogue_results")
    workspace.run("touch catalogue_results/test.json")
    assert git_query(git_repo, catalogue_results) == True

    #==================================================
    # 2: use with commit_changes=True
    # --> user will get asked to commit changes
    #==================================================

    # repo is clean
    assert git_query(git_repo, catalogue_results, True) == True

    # create new file (untracked) --> wil ask for user input
    # file path includes `catalogue_results` but it is not the directory name
    workspace.run("touch new_catalogue_results.json")

    # user responds no
    monkeypatch.setattr('builtins.input', lambda: "n")
    assert git_query(git_repo, catalogue_results, True) == False

    # git add file without commit -> will ask for user input
    workspace.run("git add .")

    # A: user responds no
    monkeypatch.setattr('builtins.input', lambda: "n")
    assert git_query(git_repo, catalogue_results, True) == False

    captured = capsys.readouterr()
    assert "uncommitted changes" in captured.out
    assert "Unrecognized response" not in captured.out

    # B: user gives other response
    monkeypatch.setattr('builtins.input', lambda: "x")
    assert git_query(git_repo, catalogue_results, True) == False

    captured = capsys.readouterr()
    assert "uncommitted changes" in captured.out
    assert "Unrecognized response" in captured.out

    # C: user responds yes
    monkeypatch.setattr('builtins.input', lambda: "y")
    assert git_query(git_repo, catalogue_results, True) == True

    captured = capsys.readouterr()
    assert "uncommitted changes" in captured.out

    git_hash_2 = repo.head.commit.hexsha
    assert git_hash_1 != git_hash_2

    #==================================================
    # 3: invalid or missing repo path
    #==================================================

    # make temp directory no longer a git repo
    workspace.run("rm -rf .git")

    with pytest.raises(InvalidGitRepositoryError):
        git_query(git_repo, catalogue_results)
    with pytest.raises(TypeError):
        git_query()

def test_git_query_new_repo(git_repo_no_commits, capsys, workspace, monkeypatch):

    # Check that git_query correctly determines that the repo is not currently clean
    assert git_query(git_repo_no_commits, "catalogue_results") == False

    # Select "no" when asked whether to commit local changes; repo will still not be clean
    monkeypatch.setattr('builtins.input', lambda: "n")
    assert git_query(git_repo_no_commits, "catalogue_results", True) == False

    # Select "yes" when asked whether to commit local changes
    # This should throw a sensible error, as a branch can't be generated yet (no initial commit)
    monkeypatch.setattr('builtins.input', lambda: "y")
    assert git_query(git_repo_no_commits, "catalogue_results", True) == False
    captured = capsys.readouterr()
    assert "Cannot create branch as there are no existing commits.\nMake a commit manually, then run catalogue engage again." in captured.out

def test_engage(git_repo, test_args, capsys):
    """
    Test engage and disengage commands.

    NOTE: the catalogue_results directory and files are created in CWD
    """

    # engage
    engage(test_args)
    lock_file = os.path.join("catalogue_results", ".lock")
    assert os.path.exists(lock_file)

    # already engaged
    engage(test_args)
    captured = capsys.readouterr()
    assert "Already engaged" in captured.out

    # call disengage - output_data path does not exist
    setattr(test_args, "output_data", "results")
    with pytest.raises(AssertionError):
        disengage(test_args)

    # disengage
    results_path = os.path.join(git_repo, "results")
    setattr(test_args, "output_data", results_path)
    disengage(test_args)
    output_file = glob.glob("catalogue_results/*.json")
    assert len(output_file) == 1

    # already disengaged
    disengage(test_args)
    captured = capsys.readouterr()
    assert "Not currently engaged" in captured.out

    # clean up: delete files created in CWD
    os.remove(output_file[0])
    os.rmdir("catalogue_results")

    # call engage - input_data path does not exist
    setattr(test_args, "input_data", "data")
    with pytest.raises(AssertionError):
        engage(test_args)
