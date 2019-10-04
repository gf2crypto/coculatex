"""The main script."""
import os
import logging
import argparse
from coculatex import config
from coculatex import __version__ as VERSION
from coculatex import __name__ as PROGNAME
from coculatex import __author__ as AUTHOR
from coculatex import __email__ as EMAIL
from coculatex import (
    list_action,
    init_action,
    apply_action,
    )


LOG = logging.getLogger(__name__)


def init_logging(level=logging.ERROR):
    """Init logging facilities."""
    # create logger with __name__ of program
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    # create console handler with a higher log level
    handler = logging.StreamHandler()
    handler.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)


def show_version(args):
    """Show version of program."""
    print(make_version_string(args.version))


def make_version_string(version):
    """Make the string for show version."""
    if version:
        return '{name} v.{version} by {author} (email {email})'.format(
            name=PROGNAME, version=VERSION, author=AUTHOR, email=EMAIL)
    return('No work. I am relaxing.\n'
           'If you wish to do something run `{} -h` for information'
           ''.format(PROGNAME))


def create_argparser():
    """Create parser of command line arguments."""
    arg_parser = argparse.ArgumentParser(description=(
        'tools for make LaTeX preambules from template'))
    arg_parser.add_argument('--version', action='store_true',
                            help='show current vesion')
    arg_parser.add_argument('--verbose', '-v', action='count',
                            default=0, help='increase output verbosity')
    arg_parser.set_defaults(func=show_version)
    subparsers = arg_parser.add_subparsers()
    list_action.register(subparsers)
    init_action.register(subparsers)
    apply_action.register(subparsers)
    return arg_parser


def main():
    """Process the input command."""
    parser = create_argparser()
    arguments = parser.parse_args()
    init_logging(arguments.verbose * 10)
    arguments.func(arguments)


if __name__ == "__main__":
    main()
