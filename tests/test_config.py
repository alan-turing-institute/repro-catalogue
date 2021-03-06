import os
import git
import glob
import pytest
from argparse import Namespace
import yaml
from catalogue.config import config, config_validator

def test_no_config(test_args, capsys, tmpdir):

    os.chdir(tmpdir)
    config(test_args)
    captured = capsys.readouterr()
    assert "No previous config file found" in captured.out

def test_existing_config(test_args, capsys, tmpdir):

    # With existing config file
    output_dir = os.path.join(tmpdir, 'results')
    input_dir = os.path.join(tmpdir, 'data')
    setattr(test_args, "output_data", output_dir)
    os.chdir(tmpdir)

    config_example = {
    'catalogue_results': 'catalogue_results',
    'code': 'code',
    'csv': None,
    'input_data': '{}/data'.format(tmpdir),
    'output_data': '{}/results'.format(tmpdir)
    }

    with open('catalogue_config.yaml', 'w', newline='') as yaml_file:
        writer = yaml.dump(config_example, yaml_file)

    config(test_args)
    captured = capsys.readouterr()
    config_file = os.path.join(tmpdir,'catalogue_config.yaml')
    assert os.path.isfile(config_file)
    assert "Previous valid config file found with values:" in captured.out
    assert output_dir in captured.out
    assert input_dir in captured.out

def test_generate_new_config(tmpdir, test_args, capsys):

    os.chdir(tmpdir)
    weird_args = Namespace(
        command = "engage",
        catalogue_results = "catalogue_results",
        code = str(tmpdir),
        csv = None,
        input_data = str(os.path.join(tmpdir, "data_weird")),
        output_data = str(os.path.join(tmpdir, "results"))
    )
    config(weird_args)
    captured = capsys.readouterr()
    assert "No previous config file found"
    assert "Now generating new config file 'catalogue_config.yaml' with config file values:" in captured.out
    assert weird_args.input_data in captured.out
    config_file = os.path.join(tmpdir,'catalogue_config.yaml')
    assert os.path.isfile(config_file)

    with open(config_file, "r") as f:
        string = f.read()
    # assert string == 'hi'
    assert string == "catalogue_results: catalogue_results\ncode: {}\ncsv: null\ninput_data: {}/data_weird\noutput_data: {}/results\n".format(tmpdir, tmpdir, tmpdir)

def test_config_validator(tmpdir, capsys, good_config, bad_config1, bad_config2):

    # validates good config file
    assert config_validator(good_config)

    # determines config file is invalid because it is not read as a dicionatry
    assert not config_validator(bad_config2)
    captured = capsys.readouterr()
    assert 'Config error: yaml file cannot be read as a dictionary' in captured.out

    # determines config file is valid because it fails all four sub validity conditions
    assert not config_validator(bad_config1)
    captured = capsys.readouterr()
    assert 'Config error: invalid keys present in the yaml file' in captured.out
    assert 'Config error: config files are not all strings'in captured.out
