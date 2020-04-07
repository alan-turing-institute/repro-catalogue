import argparse
from engage import engage, disengage
from compare import compare, checkhashes

parser = argparse.ArgumentParser(
    description="",
    formatter_class=argparse.RawTextHelpFormatter)


parser.add_argument(
    '--output_data',
    type=list,
    metavar='output_directories',
    help=textwrap.dedent(""),
    default=None)

parser.add_argument(
    '--input_data',
    type=str,
    metavar='input_data',
    help=textwrap.dedent(""),
    default=None)

parser.add_argument(
    '--code',
    type=str,
    metavar='input_data',
    help=textwrap.dedent(""),
    default=None)

compare_parser = parser.add_subparsers("compare", description="", help="")
compare_parser.set_defaults(func=engage)

checkhashes_parser = parser.add_subparsers("checkhashes", description="", help="")
checkhashes_parser.set_defaults(func=disengage)

engage_parser = parser.add_subparsers("engage", description="", help="")
engage_parser.set_defaults(func=compare)

disengage_parser = parser.add_subparsers("disengage", description="", help="")
disengage_parser.set_defaults(func=checkhashes)
