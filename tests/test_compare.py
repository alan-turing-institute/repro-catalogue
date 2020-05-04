
import pytest
import argparse

import catalogue.catalogue as ct
from catalogue.compare import compare, compare_hashes


def test_compare_json(fixture1, fixture2, fixtures_dir, capsys, git_repo):
    """
    Test compare function with json inputs.
    """

    args = argparse.Namespace(
        hashes = [fixture2],
        command = "compare",
        input_data = "data",
        output_data = "results",
        code = git_repo,
        csv = None
    )

    # provide 1 file
    # -> catalogue will try to hash default paths that do not exist
    with pytest.raises(AssertionError):
        compare(args)

    # provide 1 file & set valid paths to a directory to hash
    setattr(args, "input_data", fixtures_dir)
    setattr(args, "output_data", fixtures_dir)
    compare(args)

    # the file hashes and are not the same as current state -->
    # expect no matches & different timestamp, code and data
    # also, files in "output_data" are different --> expect no comparison (2+4 files)
    captured = capsys.readouterr()
    assert "differ in 3 places" in captured.out
    assert "match in 0 places" in captured.out
    assert "could not be compared in 6 places" in captured.out

    # provide 2 valid file paths for comparison
    setattr(args, "hashes", [fixture1, fixture2])
    compare(args)

    captured = capsys.readouterr()
    assert "differ in 1 places" in captured.out
    assert "match in 2 places" in captured.out
    assert "could not be compared in 2 places" in captured.out

    # provide 1 file that does not exist
    setattr(args, "hashes", ["my_output.json"])
    with pytest.raises(FileNotFoundError):
        compare(args)

    # provide more than 2 files
    setattr(args, "hashes", [fixture1, fixture2, fixture2])
    with pytest.raises(AssertionError):
        compare(args)


def test_compare_csv(fixture4, fixtures_dir, git_repo, workspace, capsys):
    """
    Test compare function with csv inputs.
    """

    args = argparse.Namespace(
        hashes = ["20200430-172025"],
        command = "compare",
        input_data = "data",
        output_data = "results",
        code = git_repo,
        csv = fixture4
    )

    # provide 1 correct timestamp
    # -> catalogue will try to hash default paths that do not exist
    with pytest.raises(AssertionError):
        compare(args)

    # provide 1 timestamp & set valid paths to a directory to hash
    setattr(args, "input_data", fixtures_dir)
    setattr(args, "output_data", fixtures_dir)
    compare(args)

    # the hashes associated with timestamp are not the same as current state -->
    # expect no matches & different timestamp, code and data
    # also, files in "output_data" are different --> expect no comparison (3+4 files)
    captured = capsys.readouterr()
    assert "differ in 3 places" in captured.out
    assert "match in 0 places" in captured.out
    assert "could not be compared in 7 places" in captured.out

    # provide 2 valid timestamps
    setattr(args, "hashes", ["20200430-172025", "20200430-172025"])
    compare(args)

    captured = capsys.readouterr()
    assert "differ in 0 places" in captured.out
    assert "match in 6 places" in captured.out
    assert "could not be compared in 0 places" in captured.out

    # provided timestamp not in file
    setattr(args, "hashes", ["20200503-120000"])
    with pytest.raises(EOFError):
        compare(args)

    # provide more than 2 timestamps
    setattr(args, "hashes", ["20200430-172025", "20200430-172025", "20200430-172025"])
    with pytest.raises(AssertionError):
        compare(args)


def test_compare_hashes(fixture1, fixture2):

    # dict1 contains timestamp, input_data, code but is missing output_data
    # --> the missing keyword leads to 1 failure
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

    # the timestamps between the two dicts differ, dict2 has 2 extra files
    diff_output = compare_hashes(dict1, dict2)
    assert len(diff_output["matches"]) == 2
    assert len(diff_output['differs']) == 1
    assert len(diff_output["failures"]) == 2
