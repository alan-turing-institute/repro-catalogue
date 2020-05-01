
import pytest

from catalogue.utils import check_paths_exists

def test_check_paths_exists(test_args):

    # valid inputs
    # (includes arg with value that is not a valid path but that is skipped in check)
    assert check_paths_exists(test_args) == True

    # invalid path given
    setattr(test_args, "output_data", "xyz")
    assert check_paths_exists(test_args) == False
