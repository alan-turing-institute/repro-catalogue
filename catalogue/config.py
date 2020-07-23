
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd
from .utils import read_config_file


def config(args):

    #location of config file
    config_loc = 'catalogue_config.csv'

    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if os.path.isfile(config_loc) is False:
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = read_config_file(config_loc)
        print('Previous config file found with values:')
        for key in dict:
            print('{}:{}'.format(key, dict[key]))

    print("Now generating new csv file 'catalogue_config.csv' with config file values:")

    # write the new csv file. At the moment it uses test_dict, but in practice it will use the provided 'args'
    # dictionary. 'args' is currently a Namespace file.
    with open('catalogue_config.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in vars(args).items():
            if key not in ["command", "func"]:
                writer.writerow([key, value])
                print('{}:{}'.format(key, vars(args)[key]))
