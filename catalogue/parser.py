import argparse
import textwrap

from .engage import engage, disengage
from .compare import compare


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

    compare
    -------
    The `compare` mode is used to check if two hashes are identical, or if the corrent
    state of the input, code, and output match the state from a previous run. The
    `compare` mode accepts either 1 or 2 unnamed input arguments which are strings holding the
    path of existing json files output from the code. If 2 inputs are given, `compare` checks the
    two inputs, while if 1 input is given that input is compared to the current state.
    If 1 input is given, the usual flags for input, code, and output paths apply.

    Note that if `compare` mode is used with 1 input, any use of flags to set data or code
    paths must come before the hash file due to how arguments are parsed.
    """
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    # declare shared arguments here
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        '--input_data',
        type=str,
        metavar='input_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the input data. Default value is data."),
        default='data')

    common_parser.add_argument(
        '--code',
        type=str,
        metavar='code',
        help=textwrap.dedent("This argument should be the path (full or relative) to the code directory." +
                             " The code directory must be a git repository, or must have a parent directory" +
                             " that is a git repository. Default is the current working directory."),
        default='.')

    output_parser = argparse.ArgumentParser(add_help=False)
    output_parser.add_argument(
        '--output_data',
        type=str,
        metavar='output_data',
        help=textwrap.dedent("This argument should be the path (full or relative) to the directory" +
                             " containing the analysis output data. Default value is results."),
        default="results")

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

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
