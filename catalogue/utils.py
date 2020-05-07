
import os

from datetime import datetime


def create_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def check_paths_exists(args):
    """
    Check whether all filepaths provided to catalogue exist.

    Parameters:
    ------------
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns:
    ---------
    Boolean indicating if all filepaths exist.
    """
    paths = [value for key, value in vars(args).items()
            if key not in ["command", "func", "csv", "catalogue_results"]]
    path_checks = [os.path.exists(path) for path in paths]
    return all(path_checks)
