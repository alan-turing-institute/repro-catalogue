
import pytest

from catalogue.utils import check_paths_exists, create_timestamp


def test_create_timestamp():

    assert type(create_timestamp()) == str
    
    assert len(create_timestamp()) == 15


def test_check_paths_exists(test_args):

    # valid inputs
    # (includes arg with value that is not a valid path but that is skipped in check)
    assert check_paths_exists(test_args) == True

    # path does not exist
    setattr(test_args, "output_data", "xyz")
    assert check_paths_exists(test_args) == False

    # path is not a valid type
    setattr(test_args, "output_data", 123)
    assert check_paths_exists(test_args) == False
