import argparse
import textwrap

from .engage import engage, disengage
from .compare import compare, check_hashes


def main():
    """
    Main function

    This is the main function that is called when running the tool. The function parses
    the arguments supplied and calls the appropriate function (`engage`, `disengage`,
    `checkhashes`, or `compare`). The details of each of these functions is described in
    the appropriate docstrings.

    engage
    -------
    When running in `engage` mode, two options can be set: `--input_data` and `--code`.
    These arguments should be strings specifing the directories where the input data
    and code reside, respectively. Defaults are assumed to be `"data"` (relative to the
    current working directory) for the input data argument, and the current directory
    for the code. The code argument must be a git repository, or a directory whose
    parent directory contains a git repository.
    """
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

    engage_parser = subparsers.add_parser("engage", description="", help="")
    engage_parser.set_defaults(func=engage)

    engage_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containint the input data. Default value is data"),
        default='data')

    engage_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent("This argument should be the path (full or relative) to the code directory." +
                             " The code directory must be a git repository, or must have a parent directory" +
                             " that is a git repository. Default is the current working directory."),
        default='.')

    checkhashes_parser = subparsers.add_parser("checkhashes", description="", help="")
    checkhashes_parser.set_defaults(func=check_hashes)

    compare_parser = subparsers.add_parser("compare", description="", help="")
    compare_parser.set_defaults(func=compare)

    disengage_parser = subparsers.add_parser("disengage", description="", help="")
    disengage_parser.set_defaults(func=disengage)

    disengage_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent(""),
        default="data")

    disengage_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent(""),
        default=".")

    disengage_parser.add_argument(
        '--output_data',
        type=str,
        metavar='output_data',
        help=textwrap.dedent(""),
        default="results")

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
