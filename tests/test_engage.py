
import os
import sys
import git
import glob
import pytest

from git import InvalidGitRepositoryError
from catalogue.engage import engage, disengage, git_query


def test_git_query(git_repo, capsys, workspace, monkeypatch):

    repo = git.Repo(git_repo)

    #==================================================
    # 1: use with default commit_changes=False
    #==================================================

    # repo is clean
    assert git_query(git_repo) == True

    # create new file -- untracked
    workspace.run("touch test.csv")
    assert git_query(git_repo) == True

    # git add file without commit
    workspace.run("git add .")
    assert git_query(git_repo) == False

    # commit new file
    repo.index.commit("Add new file")
    assert git_query(git_repo) == True

    #==================================================
    # 2: use with commit_changes=True
    # --> user will get asked to commit changes
    #==================================================

    # repo is clean
    assert git_query(git_repo, True) == True

    # create new file -- untracked
    workspace.run("touch test2.csv")
    assert git_query(git_repo, True) == True

    # git add file without commit -> will ask for user input
    workspace.run("git add .")

    # A: user responds no
    monkeypatch.setattr('builtins.input', lambda: "n")
    git_query(git_repo, True)

    captured = capsys.readouterr()
    assert "uncommitted changes" in captured.out

    assert git_query(git_repo, True) == False

    # B: user responds yes
    monkeypatch.setattr('builtins.input', lambda: "y")
    git_query(git_repo, True)

    captured = capsys.readouterr()
    assert "uncommitted changes" in captured.out

    assert git_query(git_repo, True) == True

    #==================================================
    # 3: invalid or missing repo path
    #==================================================

    # make temp directory no longer a git repo
    workspace.run("rm -rf .git")

    with pytest.raises(InvalidGitRepositoryError):
        git_query(git_repo)
    with pytest.raises(TypeError):
        git_query()


def test_engage(git_repo, test_args, capsys):

    # NOTE: all catalogue_results directory and files are created in CWD

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
