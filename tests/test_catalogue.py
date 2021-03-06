
import os
import git
import hashlib
import pytest

import catalogue.catalogue as ct
from git import InvalidGitRepositoryError, RepositoryDirtyError


def test_modified_walk(fixtures_dir, fixture1, fixture2, fixture3, fixture4, good_config, bad_config1, bad_config2):

    # valid path
    paths = ct.modified_walk(fixtures_dir)
    assert paths == [bad_config1, bad_config2, fixture1, fixture2, fixture3, fixture4, good_config]

    # use ingore_exts
    paths = ct.modified_walk(fixtures_dir, ignore_exts=[".json"])
    assert paths == [bad_config1, bad_config2, fixture4, good_config]

    paths = ct.modified_walk(fixtures_dir, ignore_exts=[".json", ".csv"])
    assert paths == [bad_config1, bad_config2, good_config]

    paths = ct.modified_walk(fixtures_dir, ignore_exts=[".py"])
    assert paths == [bad_config1, bad_config2, fixture1, fixture2, fixture3, fixture4, good_config ]

    # use ignore_subdirs
    base_dir = "tests"
    subdir = os.path.join(base_dir, "fixtures")
    paths = ct.modified_walk(base_dir, ignore_subdirs=[subdir])
    assert (all(
        [os.path.join(subdir, os.path.basename(fixture)) not in paths
        for fixture in [bad_config1, bad_config2, fixture1, fixture2, fixture3, fixture4, good_config]]))

    # change ignore_dot_files to False
    paths = ct.modified_walk(".", ignore_dot_files=False)
    assert "./.gitignore" in paths

    # path does not exist or not provided
    with pytest.raises(AssertionError):
        ct.modified_walk("abc")
    with pytest.raises(AssertionError):
        ct.modified_walk(123)
    with pytest.raises(TypeError):
        ct.modified_walk()


@pytest.mark.parametrize(
    "hash_f",
    [ct.hash_file, ct.hash_dir_full, ct.hash_dir_by_file, ct.hash_input, ct.hash_output]
)
@pytest.mark.parametrize(
    "path,exp_error",
    [(None, TypeError), ("abc", AssertionError), (123, AssertionError)]
)
def test_hash_invalid_path(hash_f, path, exp_error):
    """Test calling hash_* functions with invalid paths"""

    with pytest.raises(exp_error):
        hash_f(path)


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


def test_hash_dir_by_file(fixtures_dir, copy_fixtures_dir, empty_hash, fixture1):

    # input is a directory
    assert ct.hash_dir_by_file(fixtures_dir) == ct.hash_dir_by_file(fixtures_dir)
    assert (sorted(ct.hash_dir_by_file(fixtures_dir).values()) ==
            sorted(ct.hash_dir_by_file(copy_fixtures_dir).values()))
    assert empty_hash not in ct.hash_dir_by_file(fixtures_dir).values()

    # input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_by_file(fixture1)


def test_hash_dir_full(fixtures_dir, copy_fixtures_dir, empty_hash, fixture1):

    # input is a directory
    assert ct.hash_dir_full(fixtures_dir) == ct.hash_dir_full(fixtures_dir)
    assert ct.hash_dir_full(fixtures_dir) == ct.hash_dir_full(copy_fixtures_dir)
    assert ct.hash_dir_full(fixtures_dir) != empty_hash

    # input is a file
    with pytest.raises(AssertionError):
        ct.hash_dir_full(fixture1)


def test_hash_input(fixtures_dir, copy_fixtures_dir, fixture1, empty_hash):

    # 1. input is a directory
    assert ct.hash_input(fixtures_dir) == ct.hash_input(fixtures_dir)
    assert ct.hash_input(fixtures_dir) == ct.hash_input(copy_fixtures_dir)
    assert ct.hash_input(fixtures_dir) != empty_hash

    # 2. input is a file
    assert ct.hash_input(fixture1) == ct.hash_input(fixture1)
    assert ct.hash_input(fixture1) != empty_hash


def test_hash_output(fixtures_dir, copy_fixtures_dir, fixture1, fixture2, fixture3, fixture4, empty_hash, bad_config1, bad_config2, good_config):

    # 1. input is a directory
    assert ct.hash_output(fixtures_dir) == {
        fixture1: ct.hash_file(fixture1).hexdigest(),
        fixture2: ct.hash_file(fixture2).hexdigest(),
        fixture3: ct.hash_file(fixture3).hexdigest(),
        fixture4: ct.hash_file(fixture4).hexdigest(),
        good_config: ct.hash_file(good_config).hexdigest(),
        bad_config1: ct.hash_file(bad_config1).hexdigest(),
        bad_config2: ct.hash_file(bad_config2).hexdigest()

    }
    assert (sorted(ct.hash_output(fixtures_dir).values()) ==
            sorted(ct.hash_output(copy_fixtures_dir).values()))
    assert empty_hash not in ct.hash_output(fixtures_dir).values()

    # 2. input is a file
    assert ct.hash_output(fixture1) == ct.hash_output(fixture1)
    assert fixture1 in ct.hash_output(fixture1).keys()
    assert ct.hash_output(fixture1)[fixture1] != empty_hash


def test_hash_code(git_repo, git_hash, workspace):

    # correct functioning
    assert ct.hash_code(git_repo, 'catalogue_results') == git_hash

    # directory has untracked file in `catalogue_results`
    workspace.run("mkdir catalogue_results")
    workspace.run("touch catalogue_results/test.csv")
    assert ct.hash_code(git_repo, 'catalogue_results') == git_hash

    # directory has untracked file; file path includes `catalogue_results` but
    # it is not the directory name
    workspace.run("touch catalogue_results.csv")
    with pytest.raises(RepositoryDirtyError):
        ct.hash_code(git_repo, 'catalogue_results')

    # directory has uncommited file
    workspace.run("git add .")
    with pytest.raises(RepositoryDirtyError):
        ct.hash_code(git_repo, 'catalogue_results')

    # all files committed
    repo = git.Repo(git_repo)
    repo.index.commit("Add new file")
    new_git_hash = repo.head.commit.hexsha
    assert ct.hash_code(git_repo, 'catalogue_results') != git_hash
    assert ct.hash_code(git_repo, 'catalogue_results') == new_git_hash

    # missing arguments
    with pytest.raises(TypeError):
        ct.hash_code()

    # path not a git repo
    workspace.run("rm -rf .git")
    with pytest.raises(InvalidGitRepositoryError):
        ct.hash_code(git_repo, 'catalogue_results')


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
    tmp_good_config = os.path.join(results_path, "good_config.yaml")
    tmp_bad_config1 = os.path.join(results_path, "bad_config1.yaml")
    tmp_bad_config2 = os.path.join(results_path, "bad_config2.yaml")

    assert hash_dict_2["output_data"] == {
        results_path: {
            tmp_fixture1: ct.hash_file(tmp_fixture1).hexdigest(),
            tmp_fixture2: ct.hash_file(tmp_fixture2).hexdigest(),
            tmp_fixture3: ct.hash_file(tmp_fixture3).hexdigest(),
            tmp_fixture4: ct.hash_file(tmp_fixture4).hexdigest(),
            tmp_good_config: ct.hash_file(tmp_good_config).hexdigest(),
            tmp_bad_config1: ct.hash_file(tmp_bad_config1).hexdigest(),
            tmp_bad_config2: ct.hash_file(tmp_bad_config2).hexdigest(),


            }
        }

    # invalid input - path does not exist
    setattr(test_args, "input_data", "xyz")
    with pytest.raises(AssertionError):
        ct.construct_dict(timestamp, test_args)

    # invalid input - path not valid type
    setattr(test_args, "input_data", 123)
    with pytest.raises(AssertionError):
        ct.construct_dict(timestamp, test_args)

    # missing inputs
    with pytest.raises(TypeError):
        ct.construct_dict(test_args)
    with pytest.raises(TypeError):
        ct.construct_dict()


def test_store_hash(tmpdir):

    timestamp = "20200430-000000"
    hash_dict = {"hello": "world"}
    store = "."

    # valid inputs - save to temporary file
    file = tmpdir.join('{}.json'.format(timestamp))
    ct.store_hash(hash_dict, timestamp, tmpdir.strpath)
    assert file.read() == '{"hello": "world"}'

    # save to file in a new subdirectory
    new_file = tmpdir.join("results", '{}.json'.format(timestamp))
    ct.store_hash(hash_dict, timestamp, os.path.join(tmpdir.strpath, "results"))
    assert new_file.read() == '{"hello": "world"}'

    # save to .lock file
    file = tmpdir.join('.lock')
    ct.store_hash(hash_dict, "", tmpdir.strpath, ext="lock")
    assert file.read() == '{"hello": "world"}'

    # not all inputs provided
    with pytest.raises(TypeError):
        ct.store_hash()
    with pytest.raises(TypeError):
        ct.store_hash(hash_dict, timestamp)


def test_load_hash(fixture1, fixture2):

    hash_dict_1 = ct.load_hash(fixture1)
    hash_dict_2 = ct.load_hash(fixture2)

    assert hash_dict_1 == ct.load_hash(fixture1)
    assert hash_dict_2 == ct.load_hash(fixture2)
    assert hash_dict_1 != hash_dict_2

    assert all(key in hash_dict_1.keys() for key in ["timestamp", "input_data", "code"])
    assert all(key in hash_dict_2.keys() for key in ["timestamp", "input_data", "code", "output_data"])


@pytest.mark.parametrize(
    "path,exp_error",
    [(None, TypeError), ("abc", FileNotFoundError), (123, OSError)]
)
def test_load_hash_invalid_path(path, exp_error):
    with pytest.raises(exp_error):
        ct.load_hash(path)


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

    # invalid path
    with pytest.raises(FileNotFoundError):
        ct.load_csv("abc.csv", timestamp)


@pytest.mark.parametrize(
    "timestamp,exp_error",
    [("abc", AssertionError), (1, AssertionError), ("20200430-120000", EOFError)]
)
def test_load_csv_bad_timestamp(timestamp, exp_error, fixture4):
    """
    Test load csv with timestamp that is: badly formatted, bad type, not in file.
    """
    with pytest.raises(exp_error):
        ct.load_csv(fixture4, timestamp)
