import os
import sys
import argparse
import textwrap
from argparse import Namespace
import pandas as pd
from .engage import engage, disengage
from .compare import compare
from .config import config



def main():
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    common_parser = argparse.ArgumentParser(add_help=False)

    # default dictionary is used for comparisons against the default. main_dict will represent the arguments used
    default_dict = {'input_data': None, 'code': None, 'catalogue_results': None, 'output_data': None, 'csv': None}
    main_dict = {'input_data': None, 'code': None, 'catalogue_results': None, 'output_data': None, 'csv': None}

    common_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the input data. Default value is data."),
        default=default_dict['input_data'])

    common_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent("This argument should be the path (full or relative) to the code directory." +
                             " The code directory must be a git repository, or must have a parent directory" +
                             " that is a git repository. Default is the current working directory."),
        default=default_dict['code'])

    common_parser.add_argument(
        '--catalogue_results',
        type=str,
        metavar='catalogue_results',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory where any" +
                             " files created by catalogue should be stored. It cannot be the same as the `code`" +
                             " directory. Default is catalogue_results."),
        default= default_dict['catalogue_results']
    )
    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '--output_data',
        type=str,
        metavar='output_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the analysis output data. Default value is results."),
        default= default_dict['output_data'])

    output_parser.add_argument(
        "--csv",
        type=str,
        metavar="csv",
        help=textwrap.dedent("If output to CSV is desired, set this to the desired filename (the file " +
                             "will be placed in the 'catalogue_results' directory). Optional, default is None " +
                             "for no CSV output"),
        default=default_dict['csv'])

    common_args = common_parser.parse_args()
    output_args = output_parser.parse_args()

    # location of the configuration file that will be compared against
    config_file_loc = 'catalogue_config.csv'

    # if a config file exists, we read the config file and convert it into a dictionary. We then set our main_dict as
    # equal to the config file dictionary. I.e config args > default args
    if os.path.isfile(config_file_loc):
        config_dict = pd.read_csv(config_file_loc, header=None, index_col=0, squeeze=True).to_dict()
        assert config_dict.keys() == main_dict.keys()
        for key in main_dict.keys():
            main_dict[key] = config_dict[key]

    # here we implement given args > config args > default args. If the given arg is different to default args then it
    # will take priority. If it is not different then this usually means the specific argument was not provided and thus
    # it is set to default.
    for key in vars(common_args):
        if vars(common_args)[key] is not default_dict[key]:
            main_dict[key] = vars(common_args)[key]

    for key in vars(output_args):
        if vars(output_args)[key] is not default_dict[key]:
            main_dict[key] = vars(output_args)[key]

    # the main dictionary is now complete, and we update the arguments.
    #

    for key in vars(common_args):
        vars(common_args)[key] = main_dict[key]

    for key in vars(output_args):
        vars(output_args)[key] = main_dict[key]

    # so now my common and output parsers should be correct and I should be able to use the remaining code

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

    # We need to add an additional subparser here

    config_parser = subparsers.add_parser("config", parents = [common_parser, output_parser], description="", help="")
    config_parser.set_defaults(func=config)

    args = parser.parse_args()
    assert args.code != args.catalogue_results, "The 'catalogue_results' and 'code' paths cannot be the same"
    args.func(args)


if __name__ == "__main__":
    main()











