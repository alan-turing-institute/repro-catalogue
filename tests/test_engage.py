
import os
import glob
import pytest

import catalogue.engage as ct_eng

def test_engage(test_args, fixtures_dir, capsys):

    # engage
    ct_eng.engage(test_args)
    assert os.path.exists(os.path.join("catalogue_results", ".lock"))

    # already engaged
    ct_eng.engage(test_args)
    captured = capsys.readouterr()
    assert "Already engaged" in captured.out

    # disengage
    test_args.output_data = fixtures_dir
    ct_eng.disengage(test_args)
    output_file = glob.glob("catalogue_results/*.json")
    assert len(output_file) == 1

    # already disengaged
    ct_eng.disengage(test_args)
    captured = capsys.readouterr()
    assert "Not currently engaged" in captured.out

    # delete files
    os.remove(output_file[0])
    os.rmdir("catalogue_results")
