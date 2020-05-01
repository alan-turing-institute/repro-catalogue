
import pytest

from catalogue.utils import check_paths_exists

def test_check_paths_exists(test_args):

    # valid inputs
    assert check_paths_exists(test_args) == True

    # some args are ignored, check passes even if value is not a valid path
    setattr(test_args, "command", "xyz")
    assert check_paths_exists(test_args) == True

    # invalid path given
    setattr(test_args, "input_data", "xyz")
    assert check_paths_exists(test_args) == False
