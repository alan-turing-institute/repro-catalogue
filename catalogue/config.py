
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd

# The given args is a Namespace object
# to test, create an example Namespace, e.g:
# exns = Namespace(input_data = 'C:/Users/xukev/TuringDataStories/cata_test/input_data',
#                  code='C:/Users/xukev/TuringDataStories/cata_test/code',
#                  catalogue_results= 'C:/Users/xukev/TuringDataStories/catalogue_results',
#                  output_data='C:/Users/xukev/TuringDataStories/cata_test/output_data',
#                  csv='exns.csv')


def config(args):

    #location of config file
    config_loc = 'C:/Users/xukev/repro-catalogue/catalogue_config.csv'

    config_keys = ['input_data', 'code', 'catalogue_results', 'output_data', 'csv']
    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if os.path.isfile(config_loc) is False:
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = pd.read_csv(config_loc, header=None, index_col=0, squeeze=True).to_dict()
        print('Previous config file found with values:')
        for key in dict:
            print('{}:{}'.format(key, dict[key]))

    print("Now generating new csv file 'catalogue_config.csv' ")

    # write the new csv file. At the moment it uses test_dict, but in practice it will use the provided 'args'
    # dictionary. 'args' is currently a Namespace file.
    with open(config_loc, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in vars(args).items():
            if key in config_keys:
                writer.writerow([key, value])
    print('New config file values:')

    for key in config_keys:
        print('{}:{}'.format(key, vars(args)[key]))

