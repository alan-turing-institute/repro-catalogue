import os
import hashlib


def hash_file(filepath, m=hashlib.sha512()):
    '''
    Hash the contents of a file

    Parameters
    ----------
    filepath : str
        A string pointing to the file you want to hash
    m : hashlib hash object, optional
        hash_file updates m with the contents of filepath and returns m

    Returns
    -------
    hashlib hash object
    '''
    with open(filename, 'rb') as f:
        # The following construction lets us read f in chunks,
        # instead of loading an arbitrary file in all at once.
        while True:
            b = f.read(2**10)
            if not b:
                break
            m.update(b)
    return m


def modified_walk(folder, subdirs=[], exts=[], ignore_dot_files=True):
    '''
    A wrapper on os.walk() to return a list of paths inside directory "folder"
    that do not meet the ignore criteria.

    Parameters
    ----------
    folder : str
        a filepath
    subdirs : list of str, optional
        a list of subdirectories to ignore. Must include folder in the filepath.
    exts : list of str, optional
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
            root, ext = os.path.splitext(f)[1]
            if not (
                (ext in ignore_exts) or (
                ignore_dot_files and root.startswith("."))):
                path_list.append(os.path.join(*directories, f))
        for s in sorted(dirs):
            s = os.path.join(path, s)
            if s in subdirs:
                subdirs.remove(s)
            else:
                path_list.extend(
                    modified_walk(
                        s,
                        subdirs=subdirs,
                        exts=exts,
                        ignore_dot_files=ignore_dotfiles)
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
    dict (str : bytes)
    '''
    hashes = {}
    for path in modified_walk(
            folder, **kwargs):
        hashes[path] = hash_file(path).digest()
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
    bytes
    '''
    m = hashlib.sha512()
    for path in sorted(modified_walk(
        folder, **kwargs)):
        m = hash_file(path, m)
    return m.digest()


def construct_dict(*args):
    """
    Params:
        input_data, code, output_data, timestamp
    Returns:
        dict with hashes of all inputs
    """
    pass


def get_h(*args):
    """
    Parameters:
        dictionary wish hashes (output of above function)
    Returns:
        the hash
    """
    pass


def store_hash(hash_dict, store, timestamp):
    with open(
            os.path.join(os.path.dirname(store), "{}.json".format(timestamp)),
            "w") as f:
        json.dump(hash_dict, f)


def load_hash(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
