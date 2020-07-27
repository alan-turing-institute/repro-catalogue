
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd
import yaml
from .utils import read_config_file, CONFIG_LOC, dictionary_printer


def config(args):


    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if not os.path.isfile(CONFIG_LOC):
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = read_config_file(CONFIG_LOC)
        print('Previous config file found with values:')
        dictionary_printer(dict)

    print("Now generating new config file 'catalogue_config.yaml' with config file values:")

    # write the new csv file. At the moment it uses test_dict, but in practice it will use the provided 'args'
    # dictionary. 'args' is currently a Namespace file.

    cata_dict = {key: value for key, value in vars(args).items() if key not in ["command", "func"]}
    print(cata_dict)

    with open('catalogue_config.yaml', 'w', newline='') as yaml_file:
        writer = yaml.dump(cata_dict, yaml_file)
        dictionary_printer(cata_dict)
