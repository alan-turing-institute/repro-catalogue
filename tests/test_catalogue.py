
import os
import git
import filecmp
import hashlib
import pytest
import argparse

import catalogue.catalogue as ct


def test_hash_file(fixtures_dir, empty_hash):

    # input is a directory
    with pytest.raises(IsADirectoryError):
        ct.hash_file(fixtures_dir)

    # input is a file
    for path, directories, files in os.walk(fixtures_dir):
        for f in files:
            file_path = os.path.join(path, f)
            assert ct.hash_file(file_path).hexdigest() == ct.hash_file(file_path).hexdigest()
            assert ct.hash_file(file_path).hexdigest() != empty_hash

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_file()
    with pytest.raises(FileNotFoundError):
        ct.hash_file("abc")


def test_modified_walk(fixtures_dir, fixture1, fixture2):

    paths = ct.modified_walk(fixtures_dir)
    assert paths == [fixture1, fixture2]


def test_hash_dir_by_file(fixtures_dir, fixture1, empty_hash):

    # input is a directory
    assert ct.hash_dir_by_file(fixtures_dir) == ct.hash_dir_by_file(fixtures_dir)
    assert ct.hash_dir_by_file(fixtures_dir) != empty_hash

    # input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file(fixture1)

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_dir_by_file()
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file("abc")


def test_hash_dir_full(fixtures_dir, fixture1, empty_hash):

    # input is a directory
    assert ct.hash_dir_full(fixtures_dir) == ct.hash_dir_full(fixtures_dir)
    assert ct.hash_dir_full(fixtures_dir) != empty_hash

    # input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_full(fixture1)

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_dir_full()
    with pytest.raises(AssertionError):
        ct.hash_dir_full("abc")


def test_hash_input(fixtures_dir, fixture1, empty_hash):

    # input is a directory
    assert ct.hash_input(fixtures_dir) == ct.hash_input(fixtures_dir)
    assert ct.hash_input(fixtures_dir) == ct.hash_dir_full(fixtures_dir)
    assert ct.hash_input(fixtures_dir) != empty_hash

    # input is a file
    assert ct.hash_input(fixture1) == ct.hash_input(fixture1)
    assert ct.hash_input(fixture1) == ct.hash_file(fixture1).hexdigest()
    assert ct.hash_input(fixture1) != empty_hash

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_input()
    # with pytest.raises(AssertionError):
    #     ct.hash_input("abc")


def test_hash_output(fixtures_dir, fixture1, fixture2, empty_hash):

    # input is a directory
    hashes = ct.hash_output(fixtures_dir)
    assert hashes == ct.hash_dir_by_file(fixtures_dir)

    assert hashes == {
        fixture1: ct.hash_file(fixture1).hexdigest(),
        fixture2: ct.hash_file(fixture2).hexdigest(),
    }

    # input is a file
    hashes = ct.hash_output(fixture1)
    assert hashes == ct.hash_output(fixture1)
    assert fixture1 in hashes.keys()
    assert ct.hash_output(fixture1)[fixture1] != empty_hash

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_output()
    # with pytest.raises(AssertionError):
    #     ct.hash_output("abc")


def test_hash_code():

    git_hash = ct.hash_code(".")
    repo = git.Repo(".", search_parent_directories=True)
    assert git_hash == repo.head.commit.hexsha


def test_construct_dir(fixtures_dir):

    # TODO

    # args = argparse.Namespace(
    #     command = "engage",
    #     input_data = fixtures_dir,
    #     code = "."
    # )
    #
    # hash_dict = ct.construct_dict("TIMESTAMP", args)
    # assert type(hash_dict) == dict
    #
    # keys = ["timestamp", "input_data", "code"]
    # assert sorted(hash_dict.keys()) == sorted(keys)

    pass


def test_store_hash():

    # TODO
    pass


def test_load_hash(fixture1, fixture2):

    assert ct.load_hash(fixture1) == ct.load_hash(fixture1)
    assert ct.load_hash(fixture2) == ct.load_hash(fixture2)
    assert ct.load_hash(fixture1) != ct.load_hash(fixture2)

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.load_hash()
    with pytest.raises(FileNotFoundError):
        ct.load_hash("abc")
