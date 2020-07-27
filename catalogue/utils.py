
import os

import yaml
from datetime import datetime

CONFIG_LOC = 'catalogue_config.yaml'

def create_timestamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def check_paths_exists(args):
    """
    Check whether all filepaths provided to catalogue exist.

    Parameters:
    ------------
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns:
    ---------
    Boolean indicating if all filepaths exist.
    """
    print(args)
    paths = [value for key, value in vars(args).items()
            if key not in ["command", "func", "csv", "catalogue_results"]]
    path_checks = [os.path.exists(path) for path in paths]
    print(path_checks)
    return all(path_checks)


def prune_files(files, dir):
    """
    Return files that do not have `dir` as last directory in the file path.

    Parameters:
    ------------
    files : list of str
        list of file paths
    dir : str
        directory name, files in this directory are removed

    Returns:
    ---------
    list of str
    """
    return [f for f in files if dir != os.path.basename(os.path.dirname(f))]



def read_config_file(config_file):
    with open(config_file) as f:
        config_data = yaml.load(f, Loader = yaml.FullLoader)
    return config_data


def dictionary_printer(dict):
    for key, value in dict.items():
        print('{}:{}'.format(key, value))

def config_validator(config_loc):
    print('Validating config')
    config_dict = read_config_file(config_loc)

    valid = True

    # check config_dict is in fact a dictionary
    if not isinstance(config_dict, dict):
        valid = False

    valid_keys = ['catalogue_results','code','csv','input_data','output_data']

    # checks that the config keys are a subset of the correct ones
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

    # check that there are no duplicate keys
    if valid:
        print('Config file is valid')
    else:
        print('Config file is invalid')

    return valid
