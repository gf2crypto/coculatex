"""The module containing the function to action of the `init` command."""
import logging
from os import (getcwd,
                path,
                makedirs)
from yaml import dump
from coculatex.config import (LTCONFIG,
                              PARAMETERS_BEGIN,
                              PARAMETERS_END,
                              THEME_PARAMETERS_CONFIG,
                              make_default_params)
from coculatex.themeloader import load_theme

LOG = logging.getLogger(__name__)


def register(arg_parser):
    """Register the parameters of the argument parser."""
    parser = arg_parser.add_parser(
        'init',
        description=('Create the config file from the theme. '
                     'You can it customise for your project.'))
    parser.add_argument('--project-name', '--name', '-n',
                        type=str, action='store',
                        help=('it defines the name of your project'))
    parser.add_argument('--output-path', '--output-directory',
                        '--out-path', '--out-dir', '-o',
                        default=getcwd(),
                        type=str, action='store',
                        help=('the path to the output directory'))
    parser.add_argument('--embed', '-e', action='store_true',
                        default=False,
                        help=('place the values to the tex-files, '
                              'don\'t use the separate yaml-config file'
                              )
                        )
    parser.add_argument('theme', action='store',
                        type=str, help=('the name of the theme'))
    parser.set_defaults(func=handler)


def handler(theme,
            project_name=None,
            output_directory=None,
            embed=False):
    """Init the theme `theme` in the output directory.

    In the result of the function evaluation,
    the sample config file will be created.

    :param: `str` theme - the name of the theme
    :param: `str` project_name - the name of the project
    :param: `str` output_directory - the path to output directory
    :param: `bool` embed - if it is true the function places config
                           straight to the tex-file
    :return: no return value
    """
    if not project_name:
        project_name = theme
    LOG.debug('The project name is %s', project_name)
    LOG.debug('The output directory is %s', output_directory)
    theme_config = load_theme(theme)
    LOG.debug('The theme `%s` from is loaded: %s',
              theme, theme_config)
    empty_theme = make_default_params()
    if PARAMETERS_BEGIN:
        theme_parameters = {item: empty_theme[item]
                            for item in PARAMETERS_BEGIN}
    else:
        theme_parameters = {}
    theme_parameters.update(theme_config.get('parameters', {}))
    print(theme_parameters)
    if PARAMETERS_END:
        theme_parameters.update({item: empty_theme[item]
                                 for item in PARAMETERS_END})
    config_dump = dump(theme_parameters,
                       sort_keys=False,
                       allow_unicode=True)
    if embed:
        output_file = path.join(
            output_directory,
            project_name + '.{}'.format(LTCONFIG['source_ext']))
        content = ''
        for line in config_dump.split('\n'):
            if line:
                content += '{} {}\n'.format(
                    LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
    else:
        output_file = path.join(output_directory,
                                project_name + '.yaml')
        content = config_dump
    LOG.debug('The output file: %s', output_file)
    LOG.debug('The content of the theme configuration:\n%s', content)
    makedirs(output_directory, exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
    except (IOError, PermissionError) as error:
        LOG.error('Sorry! I cannot write the output file %s. '
                  'Please, check the correctness and the '
                  'existence of the path and '
                  'the permissions it.\n'
                  'The error: %s', output_file, error)
