
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd
import yaml
from .utils import read_config_file, CONFIG_LOC, dictionary_printer

def config_validator(config_loc):
    config_dict = read_config_file(config_loc)

    valid = True

    # check config_dict is in fact a dictionary. The other checks require it to be a dictionary
    if isinstance(config_dict, dict):

        # checks that the config keys are a subset of the correct ones
        valid_keys = ['catalogue_results','code','csv','input_data','output_data']
        if not set(config_dict.keys()).issubset(valid_keys):
            valid = False
            print('Config error: invalid keys present in the yaml file')

        # check that any csv configurations have the .csv extension
        if 'csv' in config_dict.keys() and config_dict['csv'] is not None:
            filename = config_dict['csv']
            extension = filename[-4:]
            if extension != '.csv':
                valid = False
                print('Config error: csv argument has an invalid extension')

        # check that all config file keys only have string values (i.e. no nested)
        values_list = list(config_dict.values())
        for value in values_list:
            if not isinstance(value, str) and value is not None:
                valid = False
                print('Config error: config files are not all strings')

        # check that there are no double keys

    else:
        valid = False
        print('Config error: yaml file cannot be read as a dictionary')


    return valid



def config(args):

    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if not os.path.isfile(CONFIG_LOC):
        print('No previous config file found')
        print('Creating config file')

    else:
        print('Config file identified, checking validity')
        config_validator(CONFIG_LOC)
        if config_validator(CONFIG_LOC):
            dict = read_config_file(CONFIG_LOC)
            print('Previous valid config file found with values:')
            dictionary_printer(dict)
        else:
            print('Identified config file is invalid')
            print('Creating config file')

    print("Now generating new config file 'catalogue_config.yaml' with config file values:")

    # write the new csv file. At the moment it uses test_dict, but in practice it will use the provided 'args'
    # dictionary. 'args' is currently a Namespace file.

    cata_dict = {key: value for key, value in vars(args).items() if key not in ["command", "func"]}


    with open('catalogue_config.yaml', 'w', newline='') as yaml_file:
        writer = yaml.dump(cata_dict, yaml_file)
        dictionary_printer(cata_dict)
