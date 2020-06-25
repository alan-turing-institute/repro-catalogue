
import os.path
import csv
import argparse
from argparse import Namespace
import pandas as pd




def config(args):

    config_loc = 'catalogue_config.csv'

    #Check if a config file exists already, mention and print all values

    if os.path.isfile(config_loc) is False:
        print('No previous config file found')
        print('Creating config file')

    else:
        dict = pd.read_csv(config_loc, header=None, index_col=0, squeeze=True).to_dict()
        print('Previous config file found with values:')
        for key in dict:
            print('{}:{} '.format(key, dict[key]))

    print('Now generating new csv file')

    test_dict = {'input_data': 2, 'code': 3, 'catalogue_results': 4, 'output_data': 5, 'csv': 7}

    with open('dict.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in test_dict.items():
            writer.writerow([key, value])
    print('New config file values:')
    for key in test_dict:
        print('{}:{}'.format(key, test_dict[key]))













    # #opens existing catalogue config file and prints the values
    # with open(config_loc, 'wb') as f:
    #     w = csv.writer(f)
    #     w.writerows(vars(args).items())
    # print('Writing catalogue_config.csv with config values:')
    # print(vars(args))
    #
    #
    # #Write args as config file
    #
    # with open(config_loc, 'w') as f:
    #     for key in vars(args).keys():
    #         f.write("%s, %s\n" % (key, vars(args)[key]))
    #

#



