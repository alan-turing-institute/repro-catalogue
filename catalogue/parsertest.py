import os
import sys
import argparse
import textwrap
from argparse import Namespace
import pandas as pd
# from .engage import engage, disengage
# from .compare import compare

parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

common_parser = argparse.ArgumentParser(add_help=False)
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
    default=default_dict['catalogue_results']
)


common_args = common_parser.parse_args()

config_file_loc = 'C:/Users/xukev/repro-catalogue2/catalogue_config.csv'

if os.path.isfile(config_file_loc):
    config_dict = pd.read_csv(config_file_loc, header=None, index_col=0, squeeze=True).to_dict()
    assert config_dict.keys() == main_dict.keys()
    for key in main_dict.keys():
        main_dict[key] = config_dict[key]
print(main_dict)

for key in vars(common_args):
    if vars(common_args)[key] is not default_dict[key]:
        main_dict[key] = vars(common_args)[key]



print(common_args)
print(main_dict)
for key in vars(common_args):
    vars(common_args)[key] = main_dict[key]

print(common_args)

subparsers = parser.add_subparsers(dest="command")

engage_parser = subparsers.add_parser(
    "engage", parents=[common_parser], description="", help=""
)

print(vars(engage_parser.parse_args()))

compare_parser = subparsers.add_parser("compare", parents=[common_parser, output_parser],
                                       description="", help="")

print(vars(common_parser.parse_args()))

