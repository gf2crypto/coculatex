"""The module containing the function to action of the `apply` command."""
import logging
from os import (path,
                getcwd,
                listdir)
from shutil import (copy2,
                    copytree)
from yaml import safe_load
from yaml.scanner import ScannerError
from jinja2 import (FileSystemLoader,
                    Environment,
                    exceptions)
from coculatex.config import (LTCONFIG,
                              J2CONFIG,
                              SECTION_NAMES_CONFIG,
                              PARAMETERS_NAMES_CONFIG,
                              THEME_PARAMETERS_CONFIG)
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
    params = __load_params(config_file, embed)
    if not params:
        return 1
    theme = load_theme(str(params[PARAMETERS_NAMES_CONFIG['theme']]))
    LOG.debug('Loaded theme %s, config: %s',
              params.pop(PARAMETERS_NAMES_CONFIG['theme']),
              theme)
    working_dir = path.dirname(config_file)
    out_file = '{project_name}.{ext}'.format(
        project_name=params.pop(PARAMETERS_NAMES_CONFIG['project_name']),
        ext=LTCONFIG['tex_ext'])
    tex_options = theme[SECTION_NAMES_CONFIG['tex']]
    tex_options.update(params.pop(PARAMETERS_NAMES_CONFIG['tex_options']))
    __write_tex_options(path.join(working_dir, out_file), tex_options)
    tex_sources = params.pop(PARAMETERS_NAMES_CONFIG['tex_sources'], [])
    if isinstance(tex_sources, str):
        tex_sources = [tex_sources]
    if embed:
        tex_sources += [path.basename(config_file)]
    if not tex_sources:
        LOG.error('Cannot apply theme, because no one source file '
                  'is not specified, check the directive `%s` '
                  'in your configuration: %s',
                  PARAMETERS_NAMES_CONFIG['tex_sources'],
                  params)
        return 1
    LOG.debug('List of the `TeX` sources files: %s', tex_sources)
    result = __write_template(root_path=path.join(
        path.dirname(theme['path']),
        path.normpath(theme[SECTION_NAMES_CONFIG['root_file']])),
                              out_path=path.join(working_dir, out_file),
                              values=params,
                              tex_sources=tex_sources,
                              jinja2config=theme[
                                  SECTION_NAMES_CONFIG['jinja2_config']])
    if result:
        return result
    __write_latex_magic(out_file,
                        working_dir,
                        tex_sources)
    LOG.debug('Copy additional theme files %s',
              theme.get(SECTION_NAMES_CONFIG['include_files'], []))
    __copy_included_files(path.dirname(theme['path']),
                          working_dir,
                          theme.get(SECTION_NAMES_CONFIG['include_files'], []))
    return 0


def __load_params(config_file, embed):
    """Load parameters from configuration file.

    :param: `str` config_file - the path to the config file
    :param: `bool` embed - if it is setted to the True the configuration
                           file is a tex file with the embeded config.
    """
    params = dict(THEME_PARAMETERS_CONFIG)
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            if embed:
                LOG.debug('Configurations is embed')
                user_params, _ = extract_variables(file)
            else:
                LOG.debug('Configurations is not embed')
                user_params = safe_load(file)
    except (FileNotFoundError, IOError, OSError) as error:
        LOG.error('Cannot read the path %s: %s', config_file, error)
        return None
    except ScannerError as error:
        LOG.error('The problem happens while parse config file '
                  '%s: %s', config_file, error)
        return None
    if user_params:
        for name, value in params.items():
            if name in user_params and not isinstance(user_params[name],
                                                      type(value)):
                LOG.debug('Expected `%s` is `%s`, but got `%s`',
                          name, type(value), type(user_params[name]))
                user_params.pop(name)
        params.update(user_params)

    # LOG.debug('The output directory: %s', working_dir)
    if not params.get(PARAMETERS_NAMES_CONFIG['theme']):
        LOG.error('Cannot apply theme because the name of '
                  'it is not specified in configuration, '
                  'check the directive `%s` in your configuration: %s',
                  PARAMETERS_NAMES_CONFIG['theme'],
                  params)
        return None
    if not params.get(PARAMETERS_NAMES_CONFIG['project_name']):
        LOG.error('Cannot apply theme, because the project name '
                  'is not specified, check the directive `%s` '
                  'in your configuration: %s',
                  PARAMETERS_NAMES_CONFIG['project_name'],
                  params)
        return None
    return params


def __write_tex_options(out_path,
                        tex_options):
    """Write the tex options to the file."""
    with open(out_path, 'a', encoding='utf-8') as file:
        for name, value in tex_options.items():
            if isinstance(value, list):
                try:
                    file.write(
                        '%!TEX {}={}\n'.format(
                            name,
                            ' '.join(value)
                            ))
                except (TypeError, ValueError, AttributeError) as error:
                    LOG.debug('Magic comment `%s` is not list, pass it: %s',
                              name,
                              error)
            else:
                file.write('%!TEX {}={}\n'.format(name, value))


def __write_template(root_path,
                     out_path,
                     values=None,
                     tex_sources=None,
                     jinja2config=None):
    """
    Make jinja2 template and interpolate it by using variables.

    Return `str` data from jinja2 template rendered by variables.
    """
    if jinja2config:
        LOG.debug('User jinja2 configuration: %s', jinja2config)
        J2CONFIG.update({item: jinja2config.get(item, value)}
                        for item, value in J2CONFIG.items())
    LOG.debug('Use the follow jinja2 configuration: %s', J2CONFIG)
    if not values:
        values = {}
    if not tex_sources:
        tex_sources = []
    LOG.debug('List of the `TeX` sources files: %s', tex_sources)
    tex_main_format = '\\include{{{source}}}\n'
    tex_main_str = ''
    try:
        for source in tex_sources:
            if not source.endswith('.tex'):
                source += '.tex'
            tex_main_str += tex_main_format.format(
                source=path.normpath(source))
    except TypeError:
        LOG.debug('tex_sources has wrong format, it is not list, but `%s`',
                  type(tex_sources))
    LOG.debug('`tex_main` string: %s', tex_main_str)
    values['tex_main'] = tex_main_str
    try:
        data = Environment(
            loader=FileSystemLoader(path.dirname(root_path),
                                    followlinks=True),
            **J2CONFIG).get_template(
                path.basename(root_path)).render(**values)
    except exceptions.TemplateSyntaxError as error:
        LOG.error('Error while template interpolation: %s', error)
        return 1
    except (exceptions.TemplateNotFound) as error:
        LOG.error('Error while reading the file %s: %s',
                  root_path,
                  error)
        return 1
    LOG.debug('Result of the interpolation:\n%s', data)
    with open(out_path, 'a', encoding='utf-8') as file:
        file.write(data)
    return 0


def __write_latex_magic(filename, working_dir, tex_sources):
    """Write the `LaTeX` magic comments."""
    if filename.endswith('.tex'):
        latex_root_magic = '%!TEX root={}\n'.format(filename)
    else:
        latex_root_magic = '%!TEX root={}.tex\n'.format(filename)
    if not tex_sources:
        LOG.debug('The list of the sources file is empty: %s', tex_sources)
        return
    for source in tex_sources:
        if not source.endswith('.tex'):
            source += '.tex'
        source = path.join(working_dir, path.normpath(source))
        try:
            with open(source, 'r', encoding='utf8') as file:
                lines = file.readlines()
        except FileNotFoundError:
            try:
                with open(source, 'w', encoding='utf8') as file:
                    file.write(latex_root_magic)
            except (OSError, PermissionError) as error:
                LOG.debug('Cannot add latex magic root to the file %s: %s',
                          source, error)
        except (OSError, PermissionError) as error:
            LOG.debug('Cannot add latex magic root to the file %s: %s',
                      source, error)
        else:
            try:
                with open(source, 'w', encoding='utf8') as file:
                    file.write(latex_root_magic)
                    file.writelines([line for line in lines
                                     if not line.startswith('%!TEX root=')])
            except (OSError, PermissionError) as error:
                LOG.debug('Cannot add latex magic root to the file %s: %s',
                          source, error)


def __copy_included_files(theme_path,
                          working_dir,
                          include_files):
    """Copy the included files to a project."""
    try:
        for dst, src in include_files.items():
            try:
                try:
                    copytree(
                        path.join(theme_path, src),
                        path.join(working_dir, dst))
                except NotADirectoryError:
                    copy2(
                        path.join(theme_path, src),
                        path.join(working_dir, dst))
            except (FileNotFoundError, IOError, PermissionError) as error:
                LOG.debug('Cannot copy path `%s` to `%s` because: %s',
                          path.join(theme_path, src),
                          path.join(working_dir, dst),
                          error)
    except AttributeError:
        LOG.debug('Directive the `%s` has wrong format: %s. '
                  'Therefore additional files was not copied.',
                  SECTION_NAMES_CONFIG['include_files'],
                  include_files)
