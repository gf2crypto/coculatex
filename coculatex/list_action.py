"""The module containing the function to action of the `list` command."""
import logging

LOG = logging.getLogger(__name__)

COMMAND_NAME = 'list'
DESCRIPTION = 'list of registered LaTeX themes'


def register(arg_parser):
    """Register the parameters of the argument parser."""
    parser = arg_parser.add_parser(
        COMMAND_NAME,
        description=DESCRIPTION)
    parser.add_argument('--detail', '-d', action='store_true',
                        default=False,
                        help=('show description of the theme'))
    parser.add_argument('theme', action='store', type=str,
                        nargs='?', default=None,
                        help=('the name of theme; '
                              'allow you to list of the subthemes'))
    parser.set_defaults(func=handler)


def handler(theme=None, detail=False):
    """Handle of the `list` command."""
    return
