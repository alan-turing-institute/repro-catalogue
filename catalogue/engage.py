
import os
import json
import git
from git import InvalidGitRepositoryError

from . import catalogue as ct
from .compare import compare_hashes, print_comparison
from .utils import create_timestamp, check_paths_exists, prune_files


def git_query(repo_path, catalogue_dir, commit_changes=False):
    """
    Check status of a git repository

    Checks the git status of the repository on the provided path
    - if clean, returns true
    - if there are uncommitted changes (including untracked files other than
        those held in `catalogue_dir`), and the `commit_changes` flag is
        `True`, offer the user to stage and commit all tracked (and untracked)
        files and continue (returns `True`)
        otherwise, returns `False`

    If the `commit_changes` flag is `True` and the user accepts the offer
    to commit changes, a new branch is created with the name
    `"catalogue-%Y%m%d-%H%M%S"` and all tracked files that have been
    changed & any untracked files will be staged and committed.

    Parameters:
    ------------
    repo_path : str
        path to the code directory
    catalogue_dir : str
        path to directory with catalogue output files
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

    untracked = prune_files(repo.untracked_files, catalogue_dir)

    if repo.is_dirty() or (len(untracked) != 0):
        if commit_changes:
            print("Working directory contains uncommitted changes.")
            print("Do you want to stage and commit all changes? (y/[n])")
            user_choice = input().strip().lower()
            if user_choice == "y" or user_choice == "yes":
                timestamp = create_timestamp()
                new_branch = repo.create_head("catalogue-" + timestamp)
                new_branch.checkout()
                changed_files = [ item.a_path for item in repo.index.diff(None) ]
                changed_files.extend(untracked)
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
    """
    The `catalogue engage` command.

    The engage command is used prior to running an analysis. The `args` contain
    paths to `input_data` and `code` (which must be a git repo).

    The engage command:
        - does a `git_query()` check of the `code` repo
            (engage does not proceed unless the repo is clean)
        - gets hashes for the input_data and code (from `construct_dict()`)
        - saves the hashes to a `.lock` file

    Once engaged (a `.lock` file exists), the command cannot be run again until
    `disengage` has been run.

    Parameters:
    ------------
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns:
    ---------
    None
    """
    assert check_paths_exists(args), 'Not all provided filepaths exist.'

    if git_query(args.code, args.catalogue_results, True):
        try:
            assert not os.path.exists(os.path.join(args.catalogue_results, ".lock"))
        except AssertionError:
            print("Already engaged (.lock file exists). To disengage run 'catalogue disengage...'")
            print("See 'catalogue disengage --help' for details")
        else:
            hash_dict = ct.construct_dict(create_timestamp(), args)
            ct.store_hash(hash_dict, "", args.catalogue_results, ext="lock")
            print("'catalogue engage' succeeded. Proceed with analysis")


def disengage(args):
    """
    The `catalogue disengage` command.

    The disengage command is run just after finishing an analysis. It cannot be run
    unless `engage` was run first.

    The `args` contain paths to `input_data`, `code` (must be a git repo) and `output_data`.

    The disengage command:
        - reads hashes stored in the `.lock` file created during `engage`
        - gets hashes for the `input_data`, `code` and `output_data` (from `construct_dict()`)
        - compares the two sets of hashes
            (if `input_data` and `code` hashes match, saves the hashes to a file)
        - prints the results of the comparison

    Parameters:
    ------------
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns:
    ---------
    None
    """
    assert check_paths_exists(args), 'Not all provided filepaths exist.'

    timestamp = create_timestamp()
    try:
        LOCK_FILE_PATH = os.path.join(args.catalogue_results, ".lock")
        lock_dict = ct.load_hash(LOCK_FILE_PATH)
        os.remove(LOCK_FILE_PATH)
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
            hash_dict["timestamp"].update({"engage": lock_dict["timestamp"]["engage"]})
            if args.csv is None:
                ct.store_hash(hash_dict, timestamp, args.catalogue_results)
            else:
                ct.save_csv(hash_dict, timestamp, os.path.join(args.catalogue_results, args.csv))
        print_comparison(compare)
