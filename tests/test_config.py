
import os
import sys
import git
import glob
import pytest

import csv
import argparse
from argparse import Namespace
import pandas as pd
import yaml
from catalogue.config import config

def test_no_config(git_repo, test_args, capsys, workspace):

    #Ensure no file
    config_file = os.path.join(git_repo,'catalogue_config.yaml')

    os.chdir(git_repo)
    config(test_args)
    captured = capsys.readouterr()
    assert "No previous config file found" in captured.out



def test_existing_config(git_repo, test_args, capsys, workspace):

    # With existing config file
    output_dir = os.path.join(git_repo, 'results')
    input_dir = os.path.join(git_repo, 'data')
    setattr(test_args, "output_data", output_dir)
    os.chdir(git_repo)

    #TODO: manually create something (e.g. a fixture) instead of just running it twice
    config_example = {
    'catalogue_results': 'catalogue_results',
    'code': 'code',
    'csv': 'null',
    'input_data': '{}/data'.format(git_repo),
    'output_data': '{}/results'.format(git_repo)
    }

    with open('catalogue_config.yaml', 'w', newline='') as yaml_file:
        writer = yaml.dump(config_example, yaml_file)

    config(test_args)
    captured = capsys.readouterr()
    config_file = os.path.join(git_repo,'catalogue_config.yaml')
    assert os.path.isfile(config_file)
    assert "Previous config file found with values:" in captured.out

    assert output_dir in captured.out
    assert input_dir in captured.out


def test_generate_new_config(git_repo, test_args, capsys, workspace):

    os.chdir(git_repo)
    weird_args = argparse.Namespace(
        command = "engage",
        catalogue_results = "catalogue_results",
        code = str(git_repo),
        csv = None,
        input_data = str(os.path.join(git_repo, "data_weird")),
        output_data = str(os.path.join(git_repo, "results"))
    )
    config(weird_args)
    captured = capsys.readouterr()
    assert "Now generating new config file 'catalogue_config.yaml'" in captured.out
    assert weird_args.input_data in captured.out
    config_file = os.path.join(git_repo,'catalogue_config.yaml')
    assert os.path.isfile(config_file)

    with open(config_file, "r") as f:
        string = f.read()
    # assert string == 'hi'
    assert string == "catalogue_results: catalogue_results\ncode: {}\ncsv: null\ninput_data: {}/data_weird\noutput_data: {}/results\n".format(git_repo, git_repo, git_repo)

def test_csv_file_format():
    pass
