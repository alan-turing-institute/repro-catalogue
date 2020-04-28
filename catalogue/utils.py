
import os

from datetime import datetime


def create_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def check_paths_exists(args):
    """
    Check whether all provided paths to catalogue exist.
    """
    attributes = vars(args)
    inputs = [arg for arg in attributes if arg not in ["command", "func"]]
    path_checks = [os.path.exists(attributes[i]) for i in inputs]
    return all(path_checks)
