"""The module containing the function to action of the `init` command."""
import logging
from os import (getcwd,
                path,
                makedirs,
                listdir,)
from shutil import (copytree,
                    copy2)
from yaml import dump
from coculatex.config import (LTCONFIG,
                              PARAMETERS_BEGIN,
                              PARAMETERS_END,
                              PARAMETERS_NAMES_CONFIG,
                              SECTION_NAMES_CONFIG,
                              THEME_CONFIG_FILENAME,
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


def __make_theme_parameters(theme_config,
                            theme,
                            project_name):
    """Make the parameters of the theme."""
    empty_theme = make_default_params()
    if PARAMETERS_BEGIN:
        theme_parameters = {item: empty_theme[item]
                            for item in PARAMETERS_BEGIN}
    else:
        theme_parameters = {}
    theme_parameters.update(theme_config.get('parameters', {}))
    theme_parameters.update({
        PARAMETERS_NAMES_CONFIG['theme']: theme,
        PARAMETERS_NAMES_CONFIG['project_name']: project_name})
    if PARAMETERS_END:
        theme_parameters.update({item: empty_theme[item]
                                 for item in PARAMETERS_END})
    return theme_parameters


def __copy_example_files(output_directory,
                         example_path):
    """Copy the example files of a theme."""
    try:
        for src, dst in [(path.join(example_path, file),
                          path.join(output_directory, file))
                         for file in listdir(example_path)
                         if file != LTCONFIG['root_file']]:
            if path.isdir(src):
                copytree(src, dst)
            else:
                copy2(src, dst)
    except (FileNotFoundError, IOError) as error:
        LOG.debug('Cannot copy addons files of the example: %s', error)


def __write_init_file(theme_parameters,
                      output_directory,
                      output_file,
                      example_root,
                      embed):
    """Write the root init file of a theme."""
    config_dump = dump(theme_parameters,
                       sort_keys=False,
                       allow_unicode=True)
    if example_root:
        try:
            with open(example_root, 'r', encoding='utf-8') as file:
                example_content = file.read()
        except (FileNotFoundError, IOError, PermissionError) as error:
            LOG.debug('Cannot read the file %s, error: %s',
                      example_root,
                      error)
            example_content = ''
    if embed:
        content = ''
        for line in config_dump.split('\n'):
            if line:
                content += '{} {}\n'.format(
                    LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
        content += example_content
        config_file = output_file
    else:
        config_file = path.join(output_directory,
                                THEME_CONFIG_FILENAME)
        content = config_dump
    LOG.debug('The output file: %s', output_file)
    LOG.debug('The content of the theme configuration:\n%s', content)
    makedirs(output_directory, exist_ok=True)
    try:
        with open(config_file, 'w', encoding='utf-8') as file:
            file.write(content)
    except (IOError, PermissionError) as error:
        LOG.error('Sorry! I cannot write the configuration file %s. '
                  'Please, check the correctness and the '
                  'existence of the path and '
                  'the permissions it.\n'
                  'The error: %s', config_file, error)
    if example_root and not embed:
        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(example_content)
        except (IOError, PermissionError) as error:
            LOG.error('Sorry! I cannot write the output file %s. '
                      'Please, check the correctness and the '
                      'existence of the path and '
                      'the permissions it.\n'
                      'The error: %s', output_file, error)


def handler(theme,
            project_name=None,
            output_directory=None,
            embed=False,
            make_example=False):
    """Init the theme `theme` in the output directory.

    In the result of the function evaluation,
    the sample config file will be created.

    :param: `str` theme - the name of the theme
    :param: `str` project_name - the name of the project
    :param: `str` output_directory - the path to output directory
    :param: `bool` embed - if it is true the function places config
                           straight to the tex-file
    :param: `bool` make_example - if it is true the source example is created;
                                   Note: a theme must provide the example.
    :return: no return value
    """
    if not project_name:
        project_name = theme
    LOG.debug('The project name is %s', project_name)
    LOG.debug('The output directory is %s', output_directory)
    theme_config = load_theme(theme)
    theme_path = path.dirname(theme_config['path'])
    LOG.debug('The theme `%s` is loaded: %s',
              theme, theme_config)
    theme_parameters = __make_theme_parameters(theme_config,
                                               theme,
                                               project_name)

    output_file = path.join(output_directory,
                            '{}.{}'.format(project_name,
                                           LTCONFIG['source_ext']))
    if make_example:
        example = theme_config.get(SECTION_NAMES_CONFIG['example'], {})
        example_path = example.get('path', '')
        example_sources = example.get('sources', [])
        example_root = path.join(theme_path,
                                 example_path,
                                 LTCONFIG['root_file'])
        if not embed:
            example_sources.append(path.basename(output_file))
            theme_parameters.update({
                PARAMETERS_NAMES_CONFIG['tex_sources']: example_sources})

    __write_init_file(theme_parameters,
                      output_directory,
                      output_file,
                      example_root,
                      embed)

    if make_example:
        __copy_example_files(output_directory,
                             path.join(theme_path, example_path))
