import argparse
import textwrap

from .engage import engage, disengage
from .compare import compare, check_hashes


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="",
        formatter_class=argparse.RawTextHelpFormatter)

    subparsers = parser.add_subparsers()

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

    compare_parser = subparsers.add_parser("engage", description="", help="")
    compare_parser.set_defaults(func=engage)

    checkhashes_parser = subparsers.add_parser("checkhashes", description="", help="")
    checkhashes_parser.set_defaults(func=check_hashes)

    engage_parser = subparsers.add_parser("compare", description="", help="")
    engage_parser.set_defaults(func=compare)

    disengage_parser = subparsers.add_parser("disengage", description="", help="")
    disengage_parser.set_defaults(func=disengage)

    parser.parse_args()


if __name__ == "__main__":
    main()
