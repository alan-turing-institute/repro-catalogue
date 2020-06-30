
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd

# To test, create an example namespace, e.g:
# exns = Namespace(input_data = r'C:\Users\xukev\repro-catalogue\cata_test\input_data',
#                  code=r'C:\Users\xukev\repro-catalogue\cata_test\code',
#                  catalogue_results= r'C:\Users\xukev\repro-catalogue\catalogue_results',
#                  output_data=r'C:\Users\xukev\repro-catalogue\cata_test\output_data',
#                  csv=r'exns.csv')

def config(args):

    #location of config file
    config_loc = 'C:/Users/xukev/repro-catalogue/catalogue_config.csv'



    #Check if a config file exists already. If a config file already exists, convert to dictionary and print values

    if os.path.isfile(config_loc) is False:
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = pd.read_csv(config_loc, header=None, index_col=0, squeeze=True).to_dict()
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


