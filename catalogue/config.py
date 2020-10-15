import os.path
import yaml
from .utils import read_config_file, CONFIG_LOC, dictionary_printer

def config_validator(config_loc):

    """
    Validate the format of a configuration file.

    Applies the following checks, all of which are needed for the file to be
    validated:

    - config file can be read as a dictionary
    - argument keys are a subset of (`--input_data`, `--code`, `--output_data`, `-csv`
    `catalogue_results`)
    - argument values are all strings

    config_loc specifies the location of the config file. Commands that involve
    existing config files (such as the parser), will only use a validated config file.


    Parameters:
    ------------
    config_loc : str

    Returns:
    ---------
    Boolean indicating if a given config file is validated

    """

    config_dict = read_config_file(config_loc)

    valid = True

    # check config_dict is in fact a dictionary. The other checks require it to be a dictionary
    if isinstance(config_dict, dict):

        # checks that the config keys are a subset of the correct ones
        valid_keys = ['catalogue_results','code','csv','input_data','output_data']
        if not set(config_dict.keys()).issubset(valid_keys):
            valid = False
            print('Config error: invalid keys present in the yaml file')

        # check that all config file keys only have string values (i.e. no nested)
        values_list = list(config_dict.values())
        for value in values_list:
            if not isinstance(value, str) and value is not None:
                valid = False
                print('Config error: config files are not all strings')
    else:
        valid = False
        print('Config error: yaml file cannot be read as a dictionary')

    return valid



def config(args):

    """
    The `catalogue engage` command.

    The config command is used to generate config files that allow the user
    to specify argument inputs in advance. These config arguments will be used
    by the parser to parse the relevant arguments for the other commands.

    The config command:
        - Checks if there already exists a validated config file
        - Creates a new config file using specified input options
        - Saves the config file in the base repository under `catalogue_config.yaml`

    Parameters:
    ------------
    args : obj
        Command line input arguments (argparse.Namespace).

    Returns:
    ---------
    None
    """

    if not os.path.isfile(CONFIG_LOC):
        print('No previous config file found')

    else:
        print('Config file identified, checking validity')
        if config_validator(CONFIG_LOC):
            dict = read_config_file(CONFIG_LOC)
            print('Previous valid config file found with values:')
            dictionary_printer(dict)
        else:
            print('Identified config file is invalid')

    print("Now generating new config file 'catalogue_config.yaml' with config file values:")

    cata_dict = {key: value for key, value in vars(args).items() if key not in ["command", "func"]}


    with open('catalogue_config.yaml', 'w', newline='') as yaml_file:
        yaml.dump(cata_dict, yaml_file)
        dictionary_printer(cata_dict)
