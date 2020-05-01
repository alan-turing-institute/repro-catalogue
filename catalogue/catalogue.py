import os
import json
import hashlib
import git
from git import InvalidGitRepositoryError, RepositoryDirtyError

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
    TODO: DECIDE WHETHER WANT TO GET FULL PATH OR RELATIVE PATH TO FILE.

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
    path_list = []
    for path, directories, files in os.walk(folder):
        # loop over files in the top directory
        for f in sorted(files):
            root, ext = os.path.splitext(f)#[1]
            if not (
                (ext in ignore_exts) or (
                ignore_dot_files and root.startswith("."))):
                # path_list.append(os.path.join(*directories, f))
                path_list.append(os.path.join(path, f))
        for s in sorted(directories):
            s = os.path.join(path, s)
            if s in ignore_subdirs:
                ignore_subdirs.remove(s)
            else:
                path_list.extend(
                    modified_walk(
                        s,
                        ignore_subdirs=ignore_subdirs,
                        ignore_exts=ignore_exts,
                        ignore_dot_files=ignore_dot_files)
            )
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

def hash_code(repo_path):
    """
    Get commit digest for current HEAD commit

    Returns the current HEAD commit digest for the code that is run. If the current working
    directory is not clean, it raises a `RepositoryDirtyError`.

    Parameters
    ----------
    repo_path: str
        Path to analysis directory git repository.

    Returns
    -------
    str
        Git commit digest for the current HEAD commit of the git repository
    """

    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise InvalidGitRepositoryError("provided code directory is not a valid git repository")

    if repo.is_dirty():
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
            args.code : hash_code(args.code)
        }
    }
    if hasattr(args, 'output_data'):
        results["output_data"] = {}
        results["output_data"].update({args.output_data : hash_output(args.output_data)})
    return results


def store_hash(hash_dict, timestamp, store):
    if not os.path.exists(store):
        os.makedirs(store)
    with open(os.path.join(store, "{}.json".format(timestamp)),"w") as f:
        json.dump(hash_dict, f)


def load_hash(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
