
import pytest
import argparse

import catalogue.catalogue as ct
from catalogue.compare import compare, compare_hashes


def test_compare(fixture1, fixture2, capsys, test_args):

    # if provide 1 file, will try to hash default paths that don't exist
    setattr(test_args, "output_data", "results")
    setattr(test_args, "hashes", [fixture1])
    with pytest.raises(AssertionError):
        compare(test_args)

    # provide valid file paths for comparison
    args = argparse.Namespace(
        hashes = [fixture1, fixture2]
    )
    compare(args)

    captured = capsys.readouterr()
    assert "differ in 1 places" in captured.out
    assert "match in 2 places" in captured.out
    assert "could not be compared in 2 places" in captured.out


def test_compare_hashes(fixture1, fixture2):

    # dict1 contains timestamp, input_data, code but is missing output_data
    # --> the missing keyword should lead to a failure
    dict1 = ct.load_hash(fixture1)
    same_output1 = compare_hashes(dict1, dict1)
    assert len(same_output1["matches"]) == 3
    assert len(same_output1["differs"]) == 0
    assert len(same_output1["failures"]) == 1

    # dict2 contains: timestamp, input_data, code and 2 results files
    dict2 = ct.load_hash(fixture2)
    same_output2 = compare_hashes(dict2, dict2)
    assert len(same_output2["matches"]) == 5
    assert len(same_output2["differs"]) == 0
    assert len(same_output2["failures"]) == 0

    # the timestamps between the two files differ
    diff_output = compare_hashes(dict1, dict2)
    assert len(diff_output["matches"]) == 2
    assert len(diff_output['differs']) == 1
    assert len(diff_output["failures"]) == 2
