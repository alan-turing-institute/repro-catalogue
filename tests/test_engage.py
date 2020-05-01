
import os
import glob
import pytest

from catalogue.engage import engage, disengage

def test_engage(test_args, fixtures_dir, capsys):

    # engage
    engage(test_args)
    assert os.path.exists(os.path.join("catalogue_results", ".lock"))

    # already engaged
    engage(test_args)
    captured = capsys.readouterr()
    assert "Already engaged" in captured.out

    # call disengage - output_data path does not exist
    setattr(test_args, "output_data", "results")
    with pytest.raises(AssertionError):
        disengage(test_args)

    # disengage
    setattr(test_args, "output_data", fixtures_dir)
    disengage(test_args)
    output_file = glob.glob("catalogue_results/*.json")
    assert len(output_file) == 1

    # already disengaged
    disengage(test_args)
    captured = capsys.readouterr()
    assert "Not currently engaged" in captured.out

    # clean up: delete files
    os.remove(output_file[0])
    os.rmdir("catalogue_results")

    # call engage - input_data path does not exist
    setattr(test_args, "input_data", "data")
    with pytest.raises(AssertionError):
        engage(test_args)
