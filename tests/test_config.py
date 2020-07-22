
import os
import sys
import git
import glob
import pytest

import csv
import argparse
from argparse import Namespace
import pandas as pd
from catalogue.config import config

def test_no_config(git_repo, test_args, capsys, workspace):

    #Ensure no file
    config_file = os.path.join(git_repo,'catalogue_config.csv')

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
    config(test_args)
    #First time there should be no config file, second time one should exist
    config(test_args)
    captured = capsys.readouterr()
    config_file = os.path.join(os.getcwd(),'catalogue_config.csv')
    assert os.path.isfile(config_file)
    assert "Previous config file found with values:" in captured.out

    assert output_dir in captured.out
    assert input_dir in captured.out

def test_generate_new_config(git_repo, test_args, capsys, workspace):

    os.chdir(git_repo)
    weird_args = argparse.Namespace(
        command = "engage",
        input_data = os.path.join(git_repo, "data_weird"),
        catalogue_results = "catalogue_results",
        code = git_repo,
        output_data = os.path.join(git_repo, "results"),
        csv = None

    )
    config(weird_args)
    captured = capsys.readouterr()
    assert "Now generating new csv file 'catalogue_config.csv'" in captured.out
    assert weird_args.input_data in captured.out
    config_file = os.path.join(os.getcwd(),'catalogue_config.csv')
    assert os.path.isfile(config_file)

    with open(config_file, "r") as f:
        string = f.read()
    assert string == "input_data,{}/data_weird\ncatalogue_results,catalogue_results\ncode,{}\noutput_data,{}/results\ncsv,\n".format(git_repo, git_repo, git_repo)
