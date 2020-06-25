
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd


def dictionary_printer(dict):
    for key in dict:
        print('{}:{}'.format(key, dict[key]))

def config(args):

    #location of config file
    config_loc = 'catalogue_config.csv'

    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if os.path.isfile(config_loc) is False:
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = pd.read_csv(config_loc, header=None, index_col=0, squeeze=True).to_dict()
        print('Previous config file found with values:')
        dictionary_printer(dict)

    print('Now generating new csv file')

    #example dict
    test_dict = {'input_data': 2, 'code': 3, 'catalogue_results': 4, 'output_data': 5, 'csv': 7}

    # write the new csv file. At the moment it uses test_dict, but in practice it will use the provided 'args'
    # dictionary. 'args' is currently a Namespace file.
    with open('dict.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in test_dict.items():
            writer.writerow([key, value])
    print('New config file values:')
    dictionary_printer(test_dict)

