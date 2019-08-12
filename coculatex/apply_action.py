"""The module containing the function to action of the `apply` command."""
import logging
from os import (getcwd,
                path,
                makedirs,
                listdir)
from yaml import safe_dump, safe_load
from yaml.scanner import ScannerError
from coculatex.config import (LTCONFIG,
                              SECTION_NAMES_CONFIG)
from coculatex.templates import extract_variables
from coculatex.themeloader import load_theme

LOG = logging.getLogger(__name__)


def register(arg_parser):
    """Register the parameters of the argument parser."""
    parser = arg_parser.add_parser(
        'apply',
        description=('Apply the theme to the input'))
    parser.add_argument('--config-file', '--config', '-c',
                        type=str, action='store',
                        help=('yaml configuration file '
                              'for your project'))
    parser.add_argument('input', action='store',
                        nargs='?', default=None,
                        type=str, help=('the path to the input file'))
    parser.set_defaults(func=handler)


def __find_config_file():
    """Find configuration file for the current path.

    :return: `str` path to configuration file,
             `bool` embed (is embed config?)
    """
    curr_path = getcwd()
    LOG.debug('Current directory: %s', curr_path)
    yaml_files = [filename
                  for filename in listdir(curr_path)
                  if filename.endswith('.yaml')]
    if len(yaml_files) != []:
        file_path = path.join(curr_path, yaml_files[0])
        LOG.debug('Found yaml file configuration: %s', file_path)
        if len(yaml_files) > 1:
            LOG.warning('Found many configurations files %s, but we used only '
                        'the first. Please specify obviously the '
                        'configuration file with command line argument '
                        '`--config` to use another one.',
                        yaml_files)
        return file_path, False
    embed_config = [filename
                    for filename in listdir(curr_path)
                    if filename.endswith(LTCONFIG['source_ext'])]
    if embed_config != []:
        file_path = path.join(curr_path, embed_config[0])
        LOG.debug('Found tex-file with embed configuration: %s', file_path)
        if len(embed_config) > 1:
            LOG.warning('Found many configurations files %s, but we used only '
                        'the first. Please specify obviously the '
                        'configuration file with command line argument '
                        '`--config` to use another one.',
                        embed_config)
        return file_path, True
    return '', False


def handler(config_file=None, embed=False):
    """Create the theme files, using configuration file.

    In the result of the function evaluation,
    the theme's files will be created.

    :param: `str` config_file - configuration file
    :param: `bool` embed - if it is true the function cosiders
                           the config_file as the tex file,
                           which is contained the configuration
    :return: no return value
    """
    if not config_file:
        config_file, embed = __find_config_file()
    if not config_file:
        LOG.error('Cannot find configurations file! Plese specify it '
                  'obviously with command line argument `--config`')
        return 1

    LOG.debug('Use the follow configuration file: %s', config_file)
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            if embed:
                LOG.debug('Configurations is not embed')
                params = safe_load(file)
            else:
                LOG.debug('Configurations is embed')
                params, _ = extract_variables(file)
    except (FileNotFoundError, IOError, OSError) as error:
        LOG.error('Cannot read the path %s: %s', config_file, error)
        return 1
    except ScannerError as error:
        LOG.error('The problem happens while parse config file '
                  '%s: %s', config_file, error)
        return 1
    if not params:
        LOG.error('Cannot load configurations from the path %s', config_file)

    # LOG.debug('The output directory: %s', working_dir)
    if 'theme' not in params:
        LOG.error('Cannot apply theme because the name of '
                  'it is not specified in configuration, '
                  'check the directive `theme` in your configuration: %s',
                  params)
        return 1
    if 'project-name' not in params:
        LOG.error('Cannot apply theme, because the project name '
                  'is not specified, check the directive `project-name` '
                  'in your configuration: %s', params)
        return 1
    tex_sources = params.get('tex-sources', [])
    if embed:
        LOG.debug('Add the configurations file %s to the tex sources',
                  config_file)
        tex_sources += [config_file]
    if not tex_sources:
        LOG.error('Cannot apply theme, because no one tex source file'
                  'is not specified, check the directive `tex-sources` '
                  'in your configuration: %s', params)
        return 1
    theme = load_theme(str(params['theme']))
    LOG.debug('Loaded theme %s, config: %s', params['theme'], theme)
    # if not source_file:
    #     source_file = project_name + '.source.tex'
    # LOG.debug('The source file name: %s', source_file)
    # source_file_path = os.path.join(working_dir, source_file)
    # LOG.debug('The source file path: %s', source_file_path)
    # theme_values, theme_path = __load_theme(theme_name, args.themes_path)
    # LOG.debug('The theme `%s` from the path `%s` is loaded, values:\n%s',
    #           theme_name, theme_path, theme_values)
    # theme_values.update({'theme_path': theme_path})
    # output_path = os.path.join(working_dir, project_name + '.tex')
    # if os.path.isfile(output_path) and not args.config_file:
    #     LOG.error('Cannot write the output file because '
    #               'the path `%s` exists. It seems that you need '
    #               'change the project name: %s.',
    #               output_path, project_name)
    #     exit(1)
    # __write_output_files(output_path,
    #                      project_name,
    #                      source_file_path,
    #                      theme_values,
    #                      values)
    # include_files = theme_values.pop('include_files', {})
    # LOG.debug('Copy additional theme files %s', include_files)
    # __copy_included_files(theme_path, working_dir, include_files)
    return 0
