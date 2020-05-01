
import os
import glob
import pytest

from catalogue.engage import engage, disengage

def test_engage(git_repo, test_args, capsys):

    # NOTE: all catalogue_results directory and files are created in CWD

    # engage
    engage(test_args)
    lock_file = os.path.join("catalogue_results", ".lock")
    assert os.path.exists(lock_file)

    # already engaged
    engage(test_args)
    captured = capsys.readouterr()
    assert "Already engaged" in captured.out

    # call disengage - output_data path does not exist
    setattr(test_args, "output_data", "results")
    with pytest.raises(AssertionError):
        disengage(test_args)

    # disengage
    results_path = os.path.join(git_repo, "results")
    setattr(test_args, "output_data", results_path)
    disengage(test_args)
    output_file = glob.glob("catalogue_results/*.json")
    assert len(output_file) == 1

    # already disengaged
    disengage(test_args)
    captured = capsys.readouterr()
    assert "Not currently engaged" in captured.out

    # clean up: delete files created in CWD
    os.remove(output_file[0])
    os.rmdir("catalogue_results")

    # call engage - input_data path does not exist
    setattr(test_args, "input_data", "data")
    with pytest.raises(AssertionError):
        engage(test_args)
