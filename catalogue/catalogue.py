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


def hash_input(input_data):
    """
    TODO: IMPLEMENT!

    Hash input data
    """
    pass


def hash_output(output_data):
    """
    TODO: IMPLEMENT!

    Hash output data
        - uses hash_dir_by_file()
    """
    pass


def hash_code(code):
    """
    TODO: IMPLEMENT!

    Hash code files
    """
    pass


def construct_dict(timestamp, input_data, code, output_data=None, mode = "engage"):
    """
    Create dictionary with hashes of input files.

    Parameters
    ----------
    timestamp : str

    input_data : str
        Path to input data file.
    code : str
        Path to analysis file.
    output_data : str
        Path to analysis results directory.
    mode : str
        Either of engage/disengage. Indicates what mode catalogue tool is in.

    Returns
    -------
    dict
        A dictionary with hashes of all inputs.
    """
    results = {
        "timestamp": {
            mode: timestamp
        },
        "input_data": {
            input_data : hash_input(input_data)
        },
        "code": {
            code : hash_code(code)
        }
    }
    if output_data is not None:
        results["output_data"] = {}
        for file in output_data:
            results["output_data"].update({file : hash_output(file)})
    return results


def store_hash(hash_dict, timestamp):
    with open(
            os.path.join(os.path.dirname(store), "{}.json".format(timestamp)),
            "w") as f:
        json.dump(hash_dict, f)


def load_hash(filepath):
    with open(filepath, "r") as f:
        return json.load(f)
