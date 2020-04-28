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

    disengage
    ---------
    When running in `disengage` mode, three options can be set: `--input_data`, `--code`
    and `output_data`. The meaning and defaults for `--input_data` and `code` are the
    same as when in `engage` mode (see above). The `output_data` argument should also
    be a string, specifying the directory with the analysis results. The default for
    the `output_data` argument is `"results"` (relative to the current working directory).
    """
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers(dest="command")

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

    checkhashes_parser.add_argument("--hashes", type=str, metavar="hashes", help="")

    checkhashes_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent(""),
        default="data")

    checkhashes_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent(""),
        default=".")

    checkhashes_parser.add_argument(
        '--output_data',
        type=str,
        metavar='output_data',
        help=textwrap.dedent(""),
        default="results")

    compare_parser = subparsers.add_parser("compare", description="", help="")
    compare_parser.set_defaults(func=compare)

    compare_parser.add_argument("hashes", type=str, nargs=2, help="")

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
