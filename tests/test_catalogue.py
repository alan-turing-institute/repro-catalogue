
import os
import git
import hashlib
import pytest

import catalogue.catalogue as ct


def test_hash_file(fixtures_dir, copy_fixtures_dir, empty_hash):

    # 1. input is a directory
    with pytest.raises(IsADirectoryError):
        ct.hash_file(fixtures_dir)

    # 2. input is a file
    for path, directories, files in os.walk(fixtures_dir):
        for f in files:
            file_path = os.path.join(path, f)
            assert ct.hash_file(file_path).hexdigest() == ct.hash_file(file_path).hexdigest()
            assert ct.hash_file(file_path).hexdigest() != empty_hash

            # hash of file == hash of file copy
            copy_file_path = os.path.join(copy_fixtures_dir, f)
            assert ct.hash_file(file_path).hexdigest() == ct.hash_file(copy_file_path).hexdigest()

    # 3. input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_file()
    with pytest.raises(AssertionError):
        ct.hash_file("abc")
    with pytest.raises(AssertionError):
        ct.hash_file(123)


def test_modified_walk(fixtures_dir, fixture1, fixture2, fixture3, fixture4):

    # valid path
    paths = ct.modified_walk(fixtures_dir)
    assert paths == [fixture1, fixture2, fixture3, fixture4]

    # use ingore extensions
    # paths = ct.modified_walk(fixtures_dir, ignore_exts=["json"])
    # assert paths == [fixture4]

    # path does not exist or not provided
    with pytest.raises(AssertionError):
        ct.modified_walk("abc")
    with pytest.raises(AssertionError):
        ct.modified_walk(123)
    with pytest.raises(TypeError):
        ct.modified_walk()


def test_hash_dir_by_file(fixtures_dir, copy_fixtures_dir, fixture1, empty_hash):

    # 1. input is a directory
    assert ct.hash_dir_by_file(fixtures_dir) == ct.hash_dir_by_file(fixtures_dir)
    assert ct.hash_dir_by_file(fixtures_dir) != empty_hash

    # hashes of files == hashes of file copies
    assert sorted(ct.hash_dir_by_file(fixtures_dir).values()) == sorted(ct.hash_dir_by_file(copy_fixtures_dir).values())

    # 2. input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file(fixture1)

    # 3. input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_dir_by_file()
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file("abc")
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file(123)


def test_hash_dir_full(fixtures_dir, copy_fixtures_dir, fixture1, empty_hash):

    # 1. input is a directory
    assert ct.hash_dir_full(fixtures_dir) == ct.hash_dir_full(fixtures_dir)
    assert ct.hash_dir_full(fixtures_dir) != empty_hash

    # hash of directory == hash of directory copy
    assert ct.hash_dir_full(fixtures_dir) == ct.hash_dir_full(copy_fixtures_dir)

    # 2. input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_full(fixture1)

    # 3. input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_dir_full()
    with pytest.raises(AssertionError):
        ct.hash_dir_full("abc")
    with pytest.raises(AssertionError):
        ct.hash_dir_full(123)


def test_hash_input(fixtures_dir, copy_fixtures_dir, fixture1, empty_hash):

    # 1. input is a directory
    assert ct.hash_input(fixtures_dir) == ct.hash_input(fixtures_dir)
    assert ct.hash_input(fixtures_dir) == ct.hash_dir_full(fixtures_dir)
    assert ct.hash_input(fixtures_dir) != empty_hash

    # hash of directory == hash of directory copy
    assert ct.hash_input(fixtures_dir) == ct.hash_input(copy_fixtures_dir)

    # 2. input is a file
    assert ct.hash_input(fixture1) == ct.hash_input(fixture1)
    assert ct.hash_input(fixture1) == ct.hash_file(fixture1).hexdigest()
    assert ct.hash_input(fixture1) != empty_hash

    # 3. input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_input()
    with pytest.raises(AssertionError):
        ct.hash_input("abc")
    with pytest.raises(AssertionError):
        ct.hash_input(123)


def test_hash_output(fixtures_dir, copy_fixtures_dir, fixture1, fixture2, fixture3, fixture4, empty_hash):

    # 1. input is a directory
    hashes = ct.hash_output(fixtures_dir)
    assert hashes == ct.hash_dir_by_file(fixtures_dir)
    assert hashes == {
        fixture1: ct.hash_file(fixture1).hexdigest(),
        fixture2: ct.hash_file(fixture2).hexdigest(),
        fixture3: ct.hash_file(fixture3).hexdigest(),
        fixture4: ct.hash_file(fixture4).hexdigest()
    }

    # hashes of files == hashes of file copies
    assert sorted(hashes.values()) == sorted(ct.hash_dir_by_file(copy_fixtures_dir).values())

    # 2. input is a file
    hashes = ct.hash_output(fixture1)
    assert hashes == ct.hash_output(fixture1)
    assert fixture1 in hashes.keys()
    assert ct.hash_output(fixture1)[fixture1] == ct.hash_file(fixture1).hexdigest()
    assert ct.hash_output(fixture1)[fixture1] != empty_hash

    # 3. input not provided or does not exist
    with pytest.raises(TypeError):
        ct.hash_output()
    with pytest.raises(AssertionError):
        ct.hash_output("abc")
    with pytest.raises(AssertionError):
        ct.hash_output(123)

def test_hash_code(git_repo, git_hash):

    assert ct.hash_code(git_repo) == git_hash

    with pytest.raises(TypeError):
        ct.hash_code()


def test_construct_dict(git_repo, git_hash, test_args):

    data_path = os.path.join(git_repo, "data")
    results_path = os.path.join(git_repo, "results")

    # valid inputs
    timestamp = "TIMESTAMP"
    hash_dict_1 = ct.construct_dict(timestamp, test_args)

    setattr(test_args, "output_data", results_path)
    hash_dict_2 = ct.construct_dict(timestamp, test_args)

    for hash_dict in [hash_dict_1, hash_dict_2]:
        assert hash_dict["timestamp"] == {test_args.command: timestamp}
        assert hash_dict["input_data"] == {data_path: ct.hash_input(data_path)}
        assert hash_dict["code"] == {git_repo: git_hash}

    assert "output_data" not in hash_dict_1.keys()

    tmp_fixture1 = os.path.join(results_path, "fixture1.json")
    tmp_fixture2 = os.path.join(results_path, "fixture2.json")
    tmp_fixture3 = os.path.join(results_path, "fixture3.json")
    tmp_fixture4 = os.path.join(results_path, "fixture4.csv")
    assert hash_dict_2["output_data"] == {
        results_path: {
            tmp_fixture1: ct.hash_file(tmp_fixture1).hexdigest(),
            tmp_fixture2: ct.hash_file(tmp_fixture2).hexdigest(),
            tmp_fixture3: ct.hash_file(tmp_fixture3).hexdigest(),
            tmp_fixture4: ct.hash_file(tmp_fixture4).hexdigest()
            }
        }

    # invalid input
    setattr(test_args, "input_data", "xyz")
    with pytest.raises(AssertionError):
        ct.construct_dict(timestamp, test_args)

    setattr(test_args, "input_data", 123)
    with pytest.raises(AssertionError):
        ct.construct_dict(timestamp, test_args)

    # missing inputs
    with pytest.raises(TypeError):
        ct.construct_dict()


def test_store_hash(tmpdir):

    timestamp = "TIMESTAMP"
    hash_dict = {"hello": "world"}
    store = "."

    # valid inputs - save to temporary file
    file = tmpdir.join('{}.json'.format(timestamp))
    ct.store_hash(hash_dict, timestamp, tmpdir.strpath)
    assert file.read() == '{"hello": "world"}'

    # not all inputs provided
    with pytest.raises(TypeError):
        ct.store_hash()
    with pytest.raises(TypeError):
        ct.store_hash(hash_dict, timestamp)


def test_load_hash(fixture1, fixture2):

    # valid inputs
    assert ct.load_hash(fixture1) == ct.load_hash(fixture1)
    assert ct.load_hash(fixture2) == ct.load_hash(fixture2)
    assert ct.load_hash(fixture1) != ct.load_hash(fixture2)

    # input not provided or does not exist
    with pytest.raises(TypeError):
        ct.load_hash()
    with pytest.raises(FileNotFoundError):
        ct.load_hash("abc")
    with pytest.raises(OSError):
        ct.load_hash(123)


def test_save_csv(tmpdir, fixture3, fixture4):

    hash_dict = ct.load_hash(fixture3)

    timestamp = hash_dict["timestamp"]["disengage"]

    # save to new temporary file
    file = tmpdir.join('test.csv')
    ct.save_csv(hash_dict, timestamp, file.strpath)

    with open(fixture4, 'r') as csv_expected:
        assert file.read() == csv_expected.read()

    # append to existing file
    file = tmpdir.join('test.csv')
    file.write("id,disengage,engage,input_data,input_hash,code,code_hash,output_data,output_file1,output_hash1\n")
    ct.save_csv(hash_dict, timestamp, file.strpath)

    with open(fixture4, 'r') as csv_expected:
        assert file.read() == csv_expected.read()

    # raise error if bad headers
    file = tmpdir.join('test.csv')
    file.write("id,disengage,engage,input_data\n")
    with pytest.raises(AssertionError):
        ct.save_csv(hash_dict, timestamp, file.strpath)


def test_load_csv(tmpdir, fixture3, fixture4):

    hash_dict_1 = ct.load_hash(fixture3)

    timestamp = hash_dict_1["timestamp"]["disengage"]

    # correct functioning
    hash_dict_2 = ct.load_csv(fixture4, timestamp)
    assert hash_dict_1 == hash_dict_2

    # badly formatted timestamp
    with pytest.raises(AssertionError):
        ct.load_csv(fixture4, "abc")

    # bad type for timestamp
    with pytest.raises(AssertionError):
        ct.load_csv(fixture4, 1)

    # well formatted timestamp, but not in file
    with pytest.raises(EOFError):
        ct.load_csv(fixture4, "20200430-120000")
