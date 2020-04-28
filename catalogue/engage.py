
import os
import json
import git
from git import InvalidGitRepositoryError

from . import catalogue as ct
from .compare import compare_hashes, print_comparison
from .utils import create_timestamp, check_paths_exists

CATALOGUE_DIR = "catalogue_results"
CATALOGUE_LOCK_PATH = os.path.join(CATALOGUE_DIR, ".lock")

def git_query(repo_path, commit_changes=False):
    """
    Check status of a git repository

    Checks the git status of the repository on the provided path
    - if clean, returns true
    - if there are uncommitted changes, and the `commit_changes` flag is
        `True`, ask for the users offer to stage and commit all and continue
        (returning `True`)
        otherwise, returns `False`

    If the `commit_changes` flag is `True` and the user accepts the offer
    to commit changes, a new branch is created with the name
    `"catalogue-%Y%m%d-%H%M%S"` and all tracked files that have been
    changed will be staged and committed.

    Parameters:
    ------------
    repo_path : str
        path to the code directory
    commit_changes : bool
        boolean indicating if the user should be prompted to stage and commit changes
        (optional, default is False)

    Returns:
    ---------
    Boolean indicating if git directory is clean
    """

    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise InvalidGitRepositoryError("provided code directory is not a valid git repository")

    if repo.is_dirty():
        if commit_changes:
            print("Working directory contains uncommitted changes.")
            print("Do you want to stage and commit all changes? (y/[n])")
            user_choice = input().strip().lower()
            if user_choice == "y" or user_choice == "yes":
                timestamp = create_timestamp()
                new_branch = repo.create_head("catalogue-" + timestamp)
                new_branch.checkout()
                changed_files = [ item.a_path for item in repo.index.diff(None) ]
                repo.index.add(changed_files)
                repo.index.commit("repro-catalogue tool auto commit at " + timestamp)
                return True
            elif user_choice == "n" or user_choice == "no" or user_choice == "":
                return False
            else:
                print("Unrecognized response, leaving repository unchaged")
                return False
        else:
            return False
    else:
        return True


def engage(args):
    assert check_paths_exists(args), 'Not all provided filepaths exist.'

    if git_query(args.code, True):
        try:
            assert not os.path.exists(CATALOGUE_LOCK_PATH)
        except AssertionError:
            print("Already engaged (.lock file exists). To disengage run 'catalogue disengage...'")
            print("See 'catalogue disengage --help' for details")
        else:
            if not os.path.exists(CATALOGUE_DIR):
                os.makedirs(CATALOGUE_DIR)

            hash_dict = ct.construct_dict(create_timestamp(), args)
            with open(CATALOGUE_LOCK_PATH, "w") as f:
                json.dump(hash_dict, f)
            print("'catalogue engage' succeeded. Proceed with analysis")


def disengage(args):
    assert check_paths_exists(args), 'Not all provided filepaths exist.'

    timestamp = create_timestamp()
    try:
        lock_dict = ct.load_hash(CATALOGUE_LOCK_PATH)
        os.remove(CATALOGUE_LOCK_PATH)
    except FileNotFoundError:
        print("Not currently engaged (could not find .lock file). To engage run 'catalogue engage...'")
        print("See 'catalogue engage --help' for details")
    else:
        hash_dict = ct.construct_dict(timestamp, args)
        compare = compare_hashes(hash_dict, lock_dict)
        # check if 'input_data' and 'code' were in matches
        assert "matches" in compare.keys(), "Error in constructing comparison dictionary"
        if 'input_data' in compare["matches"] and 'code' in compare["matches"]:
            # add engage timestamp to hash_dict
            hash_dict["timestamp"].update({"engage": lock_dict["timestamp"]})
            ct.store_hash(hash_dict, timestamp, CATALOGUE_DIR)
        print_comparison(compare)
