import argparse
import textwrap
import os
from .engage import engage, disengage
from .compare import compare
from .config import config, config_validator
from .utils import read_config_file, CONFIG_LOC, dictionary_printer



def main():
    """
    Main function

    This is the main function that is called when running the tool. The function parses
    the arguments supplied and calls the appropriate function (`engage`, `disengage`,
    `compare` or `config`). The details of each of these functions is described in
    the appropriate docstrings.

    engage
    -------
    When running in `engage` mode, two options can be set: `--input_data` and `--code`.
    These arguments should be strings specifing the directories where the input data
    and code reside, respectively. Defaults are assumed to be `"data"` (relative to the
    current working directory) for the input data argument, and the current directory
    for the code. The code argument must be a git repository, or a directory whose
    parent directory contains a git repository.

    disengage
    ---------
    When running in `disengage` mode, three options can be set: `--input_data`, `--code`
    and `--output_data`. The meaning and defaults for `--input_data` and `--code` are the
    same as when in `engage` mode (see above). The `--output_data` argument should also
    be a string, specifying the directory with the analysis results. The default for
    the `output_data` argument is `"results"` (relative to the current working directory).
    Optionally, to save results in a CSV file set `--csv` to the desired filename (will
    create a new file or append to an existing one). Result files are by default saved
    under a seperate `catalogue_results` directory. Optionally to specify a different location
    for the saved results, set `--catalogue_results` to the desired results directory.

    compare
    -------
    The `compare` mode is used to check if two hashes are identical, or if the corrent
    state of the input, code, and output match the state from a previous run. The
    `compare` mode accepts either 1 or 2 unnamed input arguments which are strings holding the
    path of existing json files output from the code. If 2 inputs are given, `compare` checks the
    two inputs, while if 1 input is given that input is compared to the current state.
    If 1 input is given, the usual flags for input, code, and output paths apply.
    Comparisons can also be made from a CSV file -- set the --csv flag to the desired CSV
    file where results are saved and then provide one or two timestamps as standard input.

    Note that if `compare` mode is used with 1 input, any use of flags to set data or code
    paths must come before the hash file due to how arguments are parsed.

    config
    ------
    The `config` mode is used to generate config files that aid in the use of the library
    by allowing the user to specify their input arguments in advance.
    All of the earlier input arguments can be set (`--input_data`, `--code`, `--output_data`, `-csv`
    `catalogue_results`). Any input arguments will be added to a config file located
    in the base repository.

    The parser will use the config file to parse arguments for all other modes.
    The parser parses arguments using the following priority:
    `specified arguments` > `config file arguments` (if the arguments exists) > `default arguments`.




    """
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    main_dict = {'input_data' : r'input_data',
                     'code': r'code',
                     'catalogue_results' : r'catalogue_results',
                     'output_data': r'output_data',
                     'csv' : None}

    if os.path.isfile(CONFIG_LOC):
        if config_validator(CONFIG_LOC):
            config_dict = read_config_file(CONFIG_LOC)
            for key in config_dict.keys():
                main_dict[key] = config_dict[key]

    # declare shared arguments here
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the input data. Default value is data."),
        default=main_dict['input_data'])

    common_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent("This argument should be the path (full or relative) to the code directory." +
                             " The code directory must be a git repository, or must have a parent directory" +
                             " that is a git repository. Default is the current working directory."),
        default=main_dict['code'])

    common_parser.add_argument(
        '--catalogue_results',
        type=str,
        metavar='catalogue_results',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory where any" +
                            " files created by catalogue should be stored. It cannot be the same as the `code`" +
                            " directory. Default is catalogue_results."),
        default=main_dict['catalogue_results']
    )

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '--output_data',
        type=str,
        metavar='output_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the analysis output data. Default value is results."),
        default= main_dict['output_data'])

    output_parser.add_argument(
        "--csv",
        type=str,
        metavar="csv",
        help=textwrap.dedent("If output to CSV is desired, set this to the desired filename (the file " +
                             "will be placed in the 'catalogue_results' directory). Optional, default is None "  +
                             "for no CSV output"),
        default= main_dict['csv'])

    # create subparsers
    subparsers = parser.add_subparsers(dest="command")

    engage_parser = subparsers.add_parser(
        "engage", parents=[common_parser], description="", help=""
    )
    engage_parser.set_defaults(func=engage)

    compare_parser = subparsers.add_parser("compare", parents=[common_parser, output_parser],
                                           description="", help="")
    compare_parser.set_defaults(func=compare)
    compare_parser.add_argument("hashes", type=str, nargs='+', help="")

    disengage_parser = subparsers.add_parser(
        "disengage", parents=[common_parser, output_parser], description="", help=""
    )
    disengage_parser.set_defaults(func=disengage)

    config_parser = subparsers.add_parser("config", parents=[common_parser, output_parser], description="", help="")
    config_parser.set_defaults(func=config)

    args = parser.parse_args()
    assert args.code != args.catalogue_results, "The 'catalogue_results' and 'code' paths cannot be the same"
    args.func(args)


if __name__ == "__main__":
    main()
