
import os
import json
import git
from git import InvalidGitRepositoryError

from . import catalogue as ct

from datetime import datetime

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
        repo = git.Repo(repo_path)
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


def lock(timestamp, input_data, code):
    """
    Create dictionary with hashed inputs and save to .lock file in CATALOGUE_DIR.

    Parameters
    ----------
    timestamp : str
        Datetime.
    input_data : str
        Path to input data directory.
    code : str
        Path to analysis directory.
    """
    hash_dict = ct.construct_dict(timestamp, input_data, code)
    if not os.path.exists(CATALOGUE_DIR):
        os.makedirs(CATALOGUE_DIR)
    with open(CATALOGUE_LOCK_PATH, "w") as f:
        json.dump(hash_dict, f)


def unlock():
    """
    Read .loc file in CATALOGUE_DIR.

    Returns
    -------
    dict: (str : str)
     File contents.
    """
    return ct.load_hash(CATALOGUE_LOCK_PATH)


def check_hashes(dict1, dict2, param):
    """
    Compare values (hashes) of dict1[param] and dict2[param].

    Parameters
    ----------
    dict1 : dict
        Dictionary of file/directory hashes.
    dict2: dict
        Dictionary of file/directory hashes.
    param: str
        Key in both dict1 and dict2, the hash to retrieve.

    Returns
    -------
    boolean, str
    """
    get_h = lambda x: list(x.values())[0]
    passed = (get_h(dict1[param]) == get_h(dict2[param]))

    if not passed:
        return passed, "Hashes of {} failed the check".format(param)
    elif passed:
        return passed, "Hashes of {} passed the check".format(param)


def check_against_lock(dict1, dict2):
    """
    Indicate whether two dictionaries contain same hashes of input_data and code.

    Parameters
    ----------
    dict1 : dict
        Dictionary of file/directory hashes (contains keys: ["code", "input_data"]).
    dict2: dict
        Dictionary of file/directory hashes (contains keys: ["code", "input_data"]).

    Returns
    -------
    boolean, str
    """
    check_input, msg_input = check_hashes(dict1, dict2, "input_data")
    check_code, msg_code = check_hashes(dict1, dict2, "code")

    return (check_input and check_code), "\n".join([
        "===========================",
        "CATALOGUE RESULTS",
        "===========================",
        msg_input,
        msg_code,
        "==========================="]
        )


def create_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def engage(args):
    timestamp = create_timestamp()
    if git_query(args.code, True):
        try:
            lock(timestamp, args.input_data, args.code)
            print("'catalogue engage' succeeded. Proceed with analysis")
        except:
            print("Already engaged. To disengage run 'catalogue disengage...'")
            print("See 'catalogue disengage --help' for details")


def disengage(args):
    timestamp = create_timestamp()
    try:
        lock_dict = unlock()
    except FileNotFoundError:
        print("Not currently engaged. To engage run 'catalogue engage...'")
        print("See 'catalogue engage --help' for details")
    hash_dict = ct.construct_dict(
        timestamp,
        args.input_data,
        args.code,
        args.output_data,
        mode = "disengage",
    )
    lock_match, messages = check_against_lock(hash_dict, lock_dict)
    if lock_match:
        # add engage timestamp to hash_dict
        hash_dict["timestamp"].update({"engage": lock_dict["timestamp"]})
        ct.store_hash(hash_dict, timestamp, CATALOGUE_DIR)
        os.remove(CATALOGUE_LOCK_PATH)
    print(messages)
