
import pytest
import argparse

import catalogue.catalogue as ct
import catalogue.compare as comp


def test_compare():
    pass



def test_compare_hashes(fixture1, fixture2):

    # dict1 contains timestamp, input_data, code but is missing output_data
    # --> the missing keyword should lead to a failure
    dict1 = ct.load_hash(fixture1)
    same_output1 = comp.compare_hashes(dict1, dict1)
    assert len(same_output1["matches"]) == 3
    assert len(same_output1["differs"]) == 0
    assert len(same_output1["failures"]) == 1

    # dict2 contains: timestamp, input_data, code and 2 results files
    dict2 = ct.load_hash(fixture2)
    same_output2 = comp.compare_hashes(dict2, dict2)
    assert len(same_output2["matches"]) == 5
    assert len(same_output2["differs"]) == 0
    assert len(same_output2["failures"]) == 0

    # the timestamps between the two files differ
    diff_output = comp.compare_hashes(dict1, dict2)
    assert len(diff_output["matches"]) == 2
    assert len(diff_output['differs']) == 1
    assert len(diff_output["failures"]) == 2
