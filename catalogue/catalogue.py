import os
import json
import csv
from itertools import chain
import hashlib
import git
from git import InvalidGitRepositoryError, RepositoryDirtyError
from .utils import prune_files


def hash_file(filepath, m=None):
    '''
    Hash the contents of a file

    Parameters
    ----------
    filepath : str
        A string pointing to the file you want to hash
    m : hashlib hash object, optional (default is None to create a new object)
        hash_file updates m with the contents of filepath and returns m

    Returns
    -------
    hashlib hash object
    '''
    assert os.path.exists(filepath), "Path {} does not exist".format(filepath)


    if m is None:
        m = hashlib.sha512()

    with open(filepath, 'rb') as f:
        # The following construction lets us read f in chunks,
        # instead of loading an arbitrary file in all at once.
        while True:
            b = f.read(2**10)
            if not b:
                break
            m.update(b)
    return m


def modified_walk(folder, ignore_subdirs=[], ignore_exts=[], ignore_dot_files=True):
    '''
    A wrapper on os.walk() to return a list of paths inside directory "folder"
    that do not meet the ignore criteria.

    Parameters
    ----------
    folder : str
        a filepath
    ignore_subdirs : list of str, optional
        a list of subdirectories to ignore. Must include folder in the filepath.
    ignore_exts : list of str, optional
        a list of file extensions to ignore.
    ignore_dot_files : bool

    Returns
    -------
    list[str]
        A list of accepted paths
    '''
    assert os.path.exists(folder), "Path {} does not exist".format(folder)

    path_list = []
    for path, directories, files in os.walk(folder):
        # loop over files in the top directory
        for f in sorted(files):
            root, ext = os.path.splitext(f)
            if not (
                (ext in ignore_exts) or
                (ignore_dot_files and root.startswith(".")) or
                (path in ignore_subdirs)
                ):
                path_list.append(os.path.join(path, f))

    return path_list


def hash_dir_by_file(folder, **kwargs):
    '''
    Create a dictionary mapping filepaths to hashes. Includes all files
    inside folder unless they meet some ignore criteria. See modified_walk
    for details.

    Parameters
    ----------
    folder : str
        filepath
    **kwargs : dict
        passed through to modified_walk

    Returns
    -------
    dict (str : str)
    '''
    assert os.path.exists(folder), "Path {} does not exist".format(folder)
    assert os.path.isdir(folder), "Provided input {} not a directory".format(folder)

    hashes = {}
    for path in modified_walk(folder, **kwargs):
        hashes[path] = hash_file(path).hexdigest()
    return hashes


def hash_dir_full(folder, **kwargs):
    '''
    Creates a hash and sequentially updates it with each file in folder.
    Includes all files inside folder unless they meet some ignore criteria
    detailed in :func:`modified_walk`.

    Parameters
    ----------
    folder : str
        filepath
    **kwargs : dict
        passed through to modified_walk

    Returns
    -------
    str
    '''
    assert os.path.exists(folder), "Path {} does not exist".format(folder)
    assert os.path.isdir(folder), "Provided input {} not a directory".format(folder)

    m = hashlib.sha512()
    for path in sorted(modified_walk(folder, **kwargs)):
        m = hash_file(path, m)
    return m.hexdigest()


def hash_input(input_data):
    """
    Hash directory with input data.

    Parameters
    ----------
    input_data: str
        Path to directory with input data.

    Returns
    -------
    str
        Hash of the directory.
    """
    if os.path.isdir(input_data):
        return hash_dir_full(input_data)
    elif os.path.isfile(input_data):
        return hash_file(input_data).hexdigest()
    else:
        raise AssertionError("Provided input {} is not a file or directory".format(input_data))


def hash_output(output_data):
    """
    Hash analysis output files.

    Parameters
    ----------
    output_data:
        Path to output data directory.

    Returns
    -------
    dict (str : str)
    """
    if os.path.isdir(output_data):
        return hash_dir_by_file(output_data)
    elif os.path.isfile(output_data):
        return {output_data: hash_file(output_data).hexdigest()}
    else:
        raise AssertionError("Provided input {} is not a file or directory".format(output_data))


def hash_code(repo_path, catalogue_dir):
    """
    Get commit digest for current HEAD commit

    Returns the current HEAD commit digest for the code that is run.

    If the current working directory is dirty (or has untracked files other
    than those held in `catalogue_dir`), it raises a `RepositoryDirtyError`.

    Parameters
    ----------
    repo_path: str
        Path to analysis directory git repository.
    catalogue_dir: str
        Path to directory with catalogue output files.

    Returns
    -------
    str
        Git commit digest for the current HEAD commit of the git repository
    """

    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise InvalidGitRepositoryError("provided code directory is not a valid git repository")

    untracked = prune_files(repo.untracked_files, catalogue_dir)
    if repo.is_dirty() or len(untracked) != 0:
        raise RepositoryDirtyError(repo, "git repository contains uncommitted changes")

    return repo.head.commit.hexsha


def construct_dict(timestamp, args):
    """
    Create dictionary with hashes of input files.

    Parameters
    ----------
    timestamp : str
        Datetime.
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns
    -------
    dict
        A dictionary with hashes of all inputs.
    """
    results = {
        "timestamp": {
            args.command: timestamp
        },
        "input_data": {
            args.input_data : hash_input(args.input_data)
        },
        "code": {
            args.code : hash_code(args.code, args.catalogue_results)
        }
    }
    if hasattr(args, 'output_data'):
        results["output_data"] = {}
        results["output_data"].update({args.output_data : hash_output(args.output_data)})
    return results


def store_hash(hash_dict, timestamp, store, ext="json"):
    """
    Save hash information to <timestamp.ext> file.

    Parameters
    ----------
    hash_dict: dict { str: dict }
        hash dictionary after completing analysis
    timestamp: str
        timestamp (will be used as name of file)
    store: str
        directory where to store the file
    ext: str
        the extension of the file to store the hash info in, default is "json"

    Returns
    -------
    None
    """

    os.makedirs(store, exist_ok=True)

    with open(os.path.join(store, "{}.{}".format(timestamp, ext)),"w") as f:
        json.dump(hash_dict, f)


def load_hash(filepath):
    """
    Load hashes from json file.

    Parameters
    ----------
    filepath : str
        path to json file to be loaded

    Returns
    -------
    dict { str : dict }
    """
    with open(filepath, "r") as f:
        return json.load(f)


def save_csv(hash_dict, timestamp, store):
    """
    Save hash information to CSV file

    Dumps the relevant hash information into a line in a CSV file. If the file does not
    exist, a new file is created. If the file exists, it appends the record to the existing
    file as long as the header information is consistent with the desired output format.

    Parameters
    ----------
    hash_dict: dict { str: dict }
        hash dictionary after completing analysis
    timestamp: str
        timestamp (will be used as an id for this run)
    store: str
        path to CSV file where

    Returns
    -------
    None
    """

    headers = ["id" ,"disengage", "engage", "input_data", "input_hash",
               "code", "code_hash", "output_data", "output_file1", "output_hash1"]

    os.makedirs(os.path.dirname(store), exist_ok=True)

    try:
        needs_header = False
        with open(store, 'r') as f:
            line = f.readline().strip().split(",")
            print(line)
            assert line == headers, "Existing CSV file header is not formatted correctly"
    except FileNotFoundError:
        needs_header = True
    finally:
        with open(store, 'a') as f:
            fwriter = csv.writer(f)
            if needs_header:
                fwriter.writerow(headers)
            output_key = list(hash_dict["output_data"].keys())[0]
            fwriter.writerow([timestamp, hash_dict["timestamp"]["disengage"], hash_dict["timestamp"]["engage"]] +
                        list(hash_dict["input_data"].keys()) + list(hash_dict["input_data"].values()) +
                        list(hash_dict["code"].keys())       + list(hash_dict["code"].values()) +
                        [ output_key ] +
                        list(chain.from_iterable((i, j) for (i, j) in zip(hash_dict["output_data"][output_key].keys(),
                                                                          hash_dict["output_data"][output_key].values()))))

def load_csv(filepath, timestamp):
    """
    Load hashes from a specific time stamp from a CSV file

    Load hash information from a CSV file from a specific time stamp. Returns a hash
    dictionary of the standard form outlined above.

    The timestamp must be a 15 character timestamp string. If the specific entry is not found
    in the CSV file, an EOFError is thrown. Also performs a number of checks of the length
    of the existing record, and confirms that the timestamps and hashes are of the correct
    length.

    Parameters
    ----------
    filepath : str
        path to CSV file to be loaded
    timestamp : str
        timestamp of desired analysis to be loaded. Must be a 15 character string of the form
        "%Y%m%d-%H%M%S"

    Returns
    -------
    dict { str : dict }
    """

    assert isinstance(timestamp, str)
    assert len(timestamp) == 15, "bad format for timestamp"

    found_record = None

    with open(filepath, "r") as f:
        freader = csv.reader(f)
        for line in freader:
            if line[0] == timestamp:
                found_record = list(line)
                break

    if found_record is None:
        raise EOFError("Unable to find desired record in {}".format(filepath))

    assert len(found_record) >= 9, "bad length for record {} in {}".format(timestamp, filepath)
    assert len(found_record) % 2 == 0, "bad length for record {} in {}".format(timestamp, filepath)
    for i in range(3):
        assert len(found_record[i]) == 15
    for i in [4] + list(range(9, len(found_record), 2)):
        assert len(found_record[i]) == 128
    assert len(found_record[6]) == 40

    result = {
        "timestamp": {
            "disengage": found_record[1],
            "engage" : found_record[2]
        },
        "input_data": {
            found_record[3] : found_record[4]
        },
        "code": {
            found_record[5] : found_record[6]
        },
        "output_data": {
            found_record[7]: { found_record[i]: found_record[i + 1] for i in range(8,len(found_record), 2)}
        }
    }

    return result
