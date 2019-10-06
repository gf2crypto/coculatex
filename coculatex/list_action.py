"""The module containing the function to action of the `list` command."""
import logging
from coculatex.config import SECTION_NAMES_CONFIG
from coculatex.themeloader import themes_iter

LOG = logging.getLogger(__name__)

COMMAND_NAME = 'list'
DESCRIPTION = 'list of registered LaTeX themes'
SHIFT_SIZE = 4


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


def handler(args):
    """Handle of the action."""
    print(get_themes_list(theme=args.theme, detail=args.detail))


def get_themes_list(theme=None, detail=False):
    """Make the list of registered themes.

    :param: `str` theme - the name of the theme
    :param: `bool` detail - switch the long and short description
    :return: the `str`which is contained the description of themes
    """
    out_str = ''
    for name, theme_config in themes_iter(theme):
        if detail:
            desc = theme_config.get(SECTION_NAMES_CONFIG['description'],
                                    'no description')
            if not desc:
                desc = 'no description'
            desc = '\n'.join([SHIFT_SIZE * ' ' + line
                              for line in desc.split('\n') if line])
            subthemes = ' '.join(
                theme_config.get(SECTION_NAMES_CONFIG['subthemes'], {}).keys())
            if not subthemes:
                subthemes = 'not provided'
            theme_str = (
                '{name}\n'
                '{desc}\n\n'
                '{shift}Subthemes: {subthemes}\n'
                ''.format(name=name, desc=desc,
                          shift=SHIFT_SIZE * ' ', subthemes=subthemes)
                )
        else:
            theme_str = '{name} '.format(name=name)
        out_str += theme_str
    return out_str
