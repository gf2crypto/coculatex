"""
The main script.

Usage:
Show version info
    >latextm --version
Verbose output
    >latextm --verbose <command> <options> <parameters>
Make LaTeX preambules from root file using template
    >latextm <path_to_root_file>
    specify theme
    >latextm --theme <theme_name> <path_to_root_file>
    >latextm -t <theme_name> <path_to_root_file>
    specify path to themes directory
    >latextm --theme-path <path_to_theme_directory> <path_to_root_file>
    >latextm -p <path_to_theme_directory> <path_to_root_file>
    specify variables
    >latextm --variables <path_to_variables_file> <path_to_root_file>
    >latextm -v <path_to_variables_file> <path_to_root_file>
"""
import os
import shutil
import logging
import argparse
import yaml
import jinja2
# import colorama
from latextm import (
    templates,
    config,
    exceptions)
from latextm import __version__ as VERSION


LOG = logging.getLogger(__name__)


def handler_list(args):
    """Handle the action `list`."""
    theme = args.theme if args.theme else ''
    if args.theme:
        __list_subthemes(args.themes_path, theme, args.detail)
    else:
        __list_themes(args.themes_path, args.detail)
    exit(0)


def __list_themes(themes_path, detail=False):
    """
    Show all the themes for the `theme_path`.

    If `detail` is True It prints the short descriptions.
    """
    LOG.debug('Need to show the list of the themes for path: %s', themes_path)
    for name in os.listdir(themes_path):
        LOG.debug('The proccessing of the theme `%s`', name)
        config_file = os.path.join(themes_path, name, 'config.yaml')
        LOG.debug('The path to the config file of the theme `%s`: %s',
                  name, config_file)
        try:
            with open(config_file, 'r', encoding='utf8') as file:
                theme_config = yaml.load(file, Loader=yaml.FullLoader)
        except (IOError, PermissionError) as error:
            LOG.debug('I cannot read the file %s: %s', config_file, error)
            continue
        except (yaml.YAMLError) as error:
            LOG.debug('The format of the config file `%s` is wrong: %s',
                      config_file, error)
            continue
        LOG.debug('The config of the theme `%s` is successfully loaded: %s',
                  name, theme_config)
        if detail:
            LOG.debug('You need the detail list')
            __print_theme_info(theme_name=name,
                               version=theme_config.get('version', 'unknown'),
                               description=theme_config.get(
                                   'description',
                                   'description is not provided'))
        else:
            LOG.debug('You need only the list of the themes')
            __print_theme_info(name)


def __list_subthemes(themes_path, theme_name, detail=False):
    """
    Show all the subthemes of the theme which is connect to the `theme_path`.

    If `detail` is True It prints the short descriptions.
    """
    theme_config, theme_path = __load_theme(theme_name, themes_path)
    for name, config_file in theme_config.get(config.THEME_SUBTHEMES,
                                              []).items():
        LOG.debug('The proccessing of the subtheme `%s`', name)
        try:
            if not config_file.endswith('.yaml'):
                config_file += '.yaml'
        except TypeError:
            LOG.debug('The path to the configuration file of the theme %s '
                      'is not string, it has type %s', name, type(config_file))
            continue
        config_path = os.path.join(theme_path, config_file)
        LOG.debug('The path to the config file of the theme `%s`: %s',
                  name, config_path)

        try:
            subtheme_config = theme_config.copy()
            with open(config_path, 'r', encoding='utf8') as file:
                subtheme_config.update(yaml.load(file, Loader=yaml.FullLoader))
        except (IOError, PermissionError) as error:
            LOG.debug('I cannot read the file %s: %s', config_path, error)
            continue
        except (yaml.scanner.ScannerError) as error:
            LOG.debug('The format of the config file `%s` is wrong: %s',
                      config_path, error)
            continue
        LOG.debug("The configuration of the subtheme %s: %s",
                  name, subtheme_config)
        if detail:
            __print_theme_info(theme_name=name,
                               version=subtheme_config.get('version',
                                                           'unknown'),
                               description=subtheme_config.get(
                                   'description',
                                   'description is not provided'))
        else:
            __print_theme_info(name)


def __print_theme_info(theme_name,
                       version=None,
                       description=None):
    """Print the information about the theme."""
    LOG.debug('Printing the theme %s(version=%s, description=%s)',
              theme_name, version, description)
    # colorama.init()
    if version and description:
        LOG.debug('The version and the description is passed, using it')
        description = '\n'.join(['    ' + line
                                 for line in description.split('\n')])
        out_string = (
            '{theme_name}\n'
            '    version {version}.\n'
            '{description}'
            ''.format(
                theme_name=theme_name,
                version=version,
                description=description)
            )
    else:
        LOG.debug('Print only the name')
        out_string = (
            '{theme_name}'
            ''.format(
                theme_name=theme_name)
        )
    LOG.debug('output string: %s', out_string)
    print(out_string)
    # print(colorama.Style.RESET_ALL)


def command_init(args):
    """Handle the `init` action."""
    project_name = args.project_name
    if not args.project_name:
        project_name = args.theme
    LOG.debug('The project name is %s', project_name)
    try:
        output_path = os.path.realpath(os.path.expanduser(args.output_path))
    except TypeError:
        LOG.debug('It is expected that the output path is a string, '
                  'but got %s', type(output_path))
        output_path = os.getcwd()
        LOG.debug('The output path is not setted, It is used the current path')
    LOG.debug('The output path is %s', output_path)
    theme_config, theme_path = __load_theme(args.theme, args.themes_path)
    LOG.debug('The theme `%s` from the path `%s` is loaded successfully.',
              args.theme, theme_path)
    LOG.debug('The config of the theme: %s', theme_config)
    theme_parameters = {'theme': args.theme, 'project-name': project_name}
    theme_parameters.update(theme_config.get('parameters', {}))
    theme_parameters['tex_preambule'] = ''
    theme_parameters['tex_options'] = []
    config_dump = yaml.dump(theme_parameters,
                            sort_keys=False,
                            allow_unicode=True)
    if args.embed:
        output_file = os.path.join(output_path, project_name + '.source.tex')
        content = ''
        for line in config_dump.split('\n'):
            if line:
                content += '{} {}\n'.format(
                    config.YAML_LINE_PREFIX,
                    line)
            else:
                content += '\n'
    else:
        output_file = os.path.join(output_path, project_name + '.yaml')
        content = config_dump
    LOG.debug('The output file: %s', output_file)
    LOG.debug('The content of the theme configuration:\n%s', content)
    if not os.path.exists(output_path):
        LOG.debug('The path `%s` is not exist. Make them.', output_path)
        try:
            os.makedirs(output_path)
        except (IOError, PermissionError) as error:
            LOG.error('Cannot make the path %s: %s', output_path, error)
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
    except (IOError, PermissionError) as error:
        LOG.error('Sorry! I cannot write the output file %s. '
                  'Please, check the correctness and the '
                  'existence of the path and '
                  'the permissions it.\n'
                  'The error: %s', output_path, error)
    return output_file, theme_path, theme_config.get('example', None)


def command_apply(args):
    """Handle the `apply` action."""
    LOG.debug('Apply input file %s '
              'while using config file %s',
              args.input, args.config_file)
    if args.input:
        input_file_path = os.path.realpath(os.path.expanduser(args.input))
        values = __load_config_from_input_file(input_file_path)
        working_dir = os.path.dirname(input_file_path)
        source_file = os.path.basename(input_file_path)
    else:
        values = {}
        working_dir = ''
        source_file = ''
    if args.config_file:
        config_file_path = os.path.realpath(
            os.path.expanduser(args.config_file))
        values.update(__load_config_from_config_file(config_file_path))
        if not working_dir:
            working_dir = os.path.dirname(config_file_path)
    if not working_dir:
        working_dir = os.getcwd()
    LOG.debug('The output directory: %s', working_dir)
    theme_name = values.get('theme')
    if not theme_name:
        LOG.error('Cannot apply theme because the name of '
                  'it is not specified in configuration, '
                  'check the directive `theme` in your configuration: %s',
                  values)
        exit(1)
    project_name = values.get('project-name')
    if not project_name:
        LOG.error('Cannot apply theme, because the project name '
                  'is not specified, check the directive `project-name` '
                  'in your configuration: %s', values)
        exit(1)
    if not source_file:
        source_file = project_name + '.source.tex'
    LOG.debug('The source file name: %s', source_file)
    source_file_path = os.path.join(working_dir, source_file)
    LOG.debug('The source file path: %s', source_file_path)
    theme_values, theme_path = __load_theme(theme_name, args.themes_path)
    LOG.debug('The theme `%s` from the path `%s` is loaded, values:\n%s',
              theme_name, theme_path, theme_values)
    theme_values.update({'theme_path': theme_path})
    output_path = os.path.join(working_dir, project_name + '.tex')
    if os.path.isfile(output_path) and not args.config_file:
        LOG.error('Cannot write the output file because '
                  'the path `%s` exists. It seems that you need '
                  'change the project name: %s.',
                  output_path, project_name)
        exit(1)
    __write_output_files(output_path,
                         project_name,
                         source_file_path,
                         theme_values,
                         values)
    include_files = theme_values.pop('include_files', {})
    LOG.debug('Copy additional theme files %s', include_files)
    __copy_included_files(theme_path, working_dir, include_files)
    return source_file_path


def command_example(args):
    """Handle the `example` action."""
    if not args.project_name:
        args.project_name = '{}.example'.format(args.theme)
    LOG.debug('Use the follow project name: %s', args.project_name)
    config_path, theme_path, example_path = command_init(args)
    working_dir = os.path.dirname(config_path)
    config_file_name = os.path.basename(config_path)
    LOG.debug('Inited new project `%s` for the path %s, '
              'the main configuration file is %s',
              args.project_name, working_dir, config_file_name)
    LOG.debug('The path for the theme is: %s', theme_path)
    LOG.debug('The raw path for the example provided by theme: %s',
              example_path)
    if args.embed:
        source_file = command_apply(
            argparse.Namespace(config_file=None, input=config_path,
                               themes_path=args.themes_path))
    else:
        source_file = command_apply(
            argparse.Namespace(config_file=config_path, input=None,
                               themes_path=args.themes_path))
    LOG.debug('The theme is applied successfully, source_file: %s',
              source_file)
    try:
        example_path_directory = os.path.join(
            theme_path,
            os.path.normpath(example_path))
    except TypeError:
        LOG.debug('The theme %s does not provide any example',
                  args.theme)
        return
    LOG.debug('The normalize path to the example of theme: %s',
              example_path_directory)
    example_source = os.path.join(example_path_directory, 'source.tex')
    LOG.debug('Write the example source file from %s to %s ',
              example_source, source_file)
    try:
        with open(example_source, 'r', encoding='utf-8') as src:
            with open(source_file, 'a', encoding='utf-8') as dst:
                dst.write(src.read())
    except (FileNotFoundError, PermissionError, IOError) as error:
        LOG.error('Cannot write the example source file: %s', error)
    LOG.debug('Copy the add ons files from %s', example_path_directory)
    try:
        for src, dst in [(os.path.join(example_path_directory, file),
                          os.path.join(working_dir, file))
                         for file in os.listdir(example_path_directory)
                         if file != 'source.tex']:
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    except (FileNotFoundError, IOError) as error:
        LOG.debug('Cannot copy add ons files: %s', error)
    LOG.debug('The example has done successfully')
    return


def __copy_included_files(theme_path, working_dir, include_files):
    """Copy the included files to a project."""
    try:
        for dst, src in include_files.items():
            try:
                try:
                    shutil.copytree(
                        os.path.join(theme_path, src),
                        os.path.join(working_dir, dst))
                except NotADirectoryError:
                    shutil.copy2(
                        os.path.join(theme_path, src),
                        os.path.join(working_dir, dst))
            except (FileNotFoundError, IOError, PermissionError) as error:
                LOG.debug('Cannot copy path `%s` to `%s` because: %s',
                          os.path.join(theme_path, src),
                          os.path.join(working_dir, dst),
                          error)
    except AttributeError:
        LOG.debug('Directive the `include_files` has wrong format: %s. '
                  'Therefore additional files was not copied.',
                  include_files)


def __write_output_files(output_path,
                         project_name,
                         source_file_path,
                         theme_values,
                         input_values):
    """Write output files."""
    LOG.debug('The output path for the root tex file: %s', output_path)
    tex_options_string = __make_tex_options(
        theme_values.get('tex', {}),
        input_values.pop('tex_options', []))
    LOG.debug('The magic TeX options string: %s', tex_options_string)
    parameters = theme_values.pop('parameters', {})
    parameters.update(input_values)
    tex_main_string = '\\input{{{}}}'.format(
        os.path.basename(source_file_path))
    parameters.update({'tex_main': tex_main_string})
    LOG.debug('The parameters for interpolation: %s', parameters)
    latex_string = __make_latex(
        os.path.join(
            theme_values.pop('theme_path', ''),
            theme_values.pop('root_file', '')),
        parameters)
    LOG.debug('The result of interpolation: %s', latex_string)
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(tex_options_string)
            file.write(latex_string)
    except (OSError, FileNotFoundError, PermissionError) as error:
        LOG.error('Cannot write file %s: %s', output_path, error)
    latex_root_magic = '%!TEX root={}.tex'.format(project_name)
    try:
        with open(source_file_path, 'r', encoding='utf8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        try:
            with open(source_file_path, 'w', encoding='utf8') as file:
                file.write(latex_root_magic + '\n')
        except (OSError, PermissionError) as error:
            LOG.debug('Cannot add latex magic root to the file %s: %s',
                      source_file_path, error)
    except (OSError, PermissionError) as error:
        LOG.debug('Cannot add latex magic root to the file %s: %s',
                  source_file_path, error)
    else:
        try:
            with open(source_file_path, 'w', encoding='utf8') as file:
                file.write(latex_root_magic + '\n')
                file.writelines([line for line in lines
                                 if not line.startswith('%!TEX')])
        except (OSError, PermissionError) as error:
            LOG.debug('Cannot add latex magic root to the file %s: %s',
                      source_file_path, error)


def __load_config_from_input_file(input_file):
    """Load configutration values from `input_file`."""
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            input_values, _ = templates.extract_variables(file)
    except (FileNotFoundError, OSError) as error:
        LOG.debug('Cannot open the file %s, error: %s',
                  input_file, error)
        return {}
    except TypeError as error:
        LOG.debug('The input file path has wrong type: %s', error)
        return {}
    except yaml.scanner.ScannerError as error:
        LOG.debug('error parse variables from file `%s`: %s',
                  input_file, error)
        return {}
    LOG.debug('Loaded values from the input file:\n%s', input_values)
    return input_values


def __load_config_from_config_file(config_file):
    """Load configuration values from yaml file."""
    LOG.debug('Load the values from the config file: %s',
              config_file)
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            config_values = yaml.safe_load(file)
    except (FileNotFoundError, OSError) as error:
        LOG.debug('Cannot open the file %s, error: %s',
                  config_file, error)
        return {}
    except yaml.scanner.ScannerError as error:
        LOG.debug('error parse variables from file `%s`: %s',
                  config_file, error)
        return {}
    return config_values


def __make_tex_options(theme_options, input_options):
    """Make the magic comments from TeX options."""
    tex_options_string = ''
    for name, value in theme_options.items():
        if name == 'options':
            try:
                tex_options_string += (
                    '%!TEX {}={}\n'.format(
                        name,
                        ' '.join(value + input_options)
                        ))
            except (TypeError, ValueError, AttributeError) as error:
                LOG.debug('Cannot add magic comment for \'options\': %s',
                          error)
        else:
            tex_options_string += (
                '%!TEX {}={}\n'.format(name, value))
    return tex_options_string + '\n\n'


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
        return config.VERSION_STRING_TEMPLATE.format(version=VERSION)
    return('No work. I am relaxing.\n'
           'If you wish to do something run `latextm -h` for information')


def create_argparser():
    """Create parser of command line arguments."""
    arg_parser = argparse.ArgumentParser(description=(
        'tools for make LaTeX preambules from template'))
    arg_parser.add_argument('--version', action='store_true',
                            help='show current vesion')
    arg_parser.add_argument('--verbose', '-v', action='count',
                            default=0, help='increase output verbosity')
    arg_parser.add_argument('--themes-path', '-t',
                            action='store',
                            default=config.THEMES_DIRECTORY,
                            help=(
                                'path to the directory for the themes'
                                '(default is `{}`)'
                                ''.format(config.THEMES_DIRECTORY)))
    arg_parser.set_defaults(func=show_version)
    subparsers = arg_parser.add_subparsers()
    parser_list = subparsers.add_parser(
        'list',
        description=('show list of themes'))
    parser_list.add_argument('--detail', '-d', action='store_true',
                             default=False,
                             help=('show description of the theme'))
    parser_list.add_argument('theme', action='store', type=str,
                             nargs='?', default=None,
                             help=('the name of theme; '
                                   'allow you to list of the subthemes'))
    parser_list.set_defaults(func=handler_list)
    parser_init = subparsers.add_parser(
        'init',
        description=('Create the config file from the theme. '
                     'You can it customise for your project.'))
    parser_init.add_argument('--project-name', '--name', '-n',
                             type=str, action='store',
                             help=('it defines the name of your project'))
    parser_init.add_argument('--output-path', '--output-directory',
                             '--out-path', '--out-dir', '-o',
                             default=os.getcwd(),
                             type=str, action='store',
                             help=('the path to the output directory'))
    parser_init.add_argument('--embed', '-e', action='store_true',
                             default=False,
                             help=('place the values to the tex-files, '
                                   'don\'t use the separate yaml-config file'
                                   ))
    parser_init.add_argument('theme', action='store',
                             type=str, help=('the name of the theme'))
    parser_init.set_defaults(func=command_init)
    parser_apply = subparsers.add_parser(
        'apply',
        description=('Apply the theme to the input'))
    parser_apply.add_argument('--config-file', '--config', '-c',
                              type=str, action='store',
                              help=('yaml configuration file '
                                    'for your project'))
    parser_apply.add_argument('input', action='store',
                              nargs='?', default=None,
                              type=str, help=('the path to the input file'))
    parser_apply.set_defaults(func=command_apply)
    parser_example = subparsers.add_parser(
        'example',
        description=(
            'Made the example for the theme. '
            'It is almost equivalent to the sequantial executions '
            'of the commands `init` and `apply`'))
    parser_example.add_argument('--project-name', '--name', '-n',
                                type=str, action='store',
                                help=('it defines the name of your project'))
    parser_example.add_argument('--output-path', '--output-directory',
                                '--out-path', '--out-dir', '-o',
                                type=str, action='store', default=os.getcwd(),
                                help=('the path to the output directory'))
    parser_example.add_argument('--embed', '-e', action='store_true',
                                default=False,
                                help=('place the values to the tex-files, '
                                      'don\'t use the separate yaml-config '
                                      ' file'))
    parser_example.add_argument('theme', action='store',
                                type=str, help=('the name of the theme'))
    parser_example.set_defaults(func=command_example)
    return arg_parser


def __make_latex(root_path, variables):
    """
    Make jinja2 template and interpolate it by using variables.

    Return `str` data from jinja2 template rendered by variables.
    """
    try:
        with open(root_path, 'r', encoding='utf-8') as file:
            jinja2_variables_str, content = templates.extract_variables(file)
    except FileNotFoundError:
        raise exceptions.LaTeXTMError('file `{}` not found'.format(root_path))
    LOG.debug('yaml description of variables for making jinja2 template: %s',
              jinja2_variables_str)
    LOG.debug('content of theme\'s template: %s', content)
    jinja2_variables = dict(config.config_iter(config.JINJA2_DEFAULT_CONFIG))
    LOG.debug('default jinja2 configuration: %s', jinja2_variables)
    # delete unknown keys and update values of default configuration
    if jinja2_variables_str:
        jinja2_variables_from_template = yaml.safe_load(jinja2_variables_str)
        if not jinja2_variables_from_template:
            jinja2_variables_from_template = {}
        LOG.debug('loaded variables from `%s`: %s',
                  root_path,
                  jinja2_variables_from_template)
        jinja2_variables.update(
            {key: value
             for key, value in jinja2_variables_from_template.items()
             if key in jinja2_variables})
        LOG.debug('jinj2 configuration updated by loaded variables: %s',
                  jinja2_variables)
    LOG.debug('using variables for render template: %s', variables)
    try:
        data = jinja2.Environment(
            loader=templates.TemplateLoader(os.path.dirname(root_path)),
            **jinja2_variables).from_string(content).render(**variables)
    except (jinja2.exceptions.TemplateError,
            jinja2.exceptions.TemplateRuntimeError,
            jinja2.exceptions.TemplateSyntaxError) as error:
        raise exceptions.LaTeXTMError(
            'jinja2 theme template error: {}'.format(error))
    return data


def __load_theme(theme_name,
                 themes_path):
    """
    Load LaTeX theme.

    `str` theme_name - name of theme
    `str` themes_path - path to theme's directory
    """
    themes_path = themes_path if themes_path else config.THEMES_DIRECTORY
    LOG.debug('Load theme `%s` from path: `%s`', theme_name, themes_path)
    themes_list = theme_name.split('.')
    theme_directory = os.path.join(themes_path, themes_list[0])
    theme_variables = {themes_list[0]: config.THEME_CONFIG_FILE_NAME}
    for theme in themes_list:
        subtheme_values = __load_theme_config(
            theme_variables.get(config.THEME_SUBTHEMES,
                                theme_variables).get(theme, None),
            theme_directory)
        LOG.debug('The values of the subtheme %s: %s', theme, subtheme_values)
        try:
            parameters = subtheme_values.pop('parameters', {})
            theme_variables['parameters'].update(parameters)
        except AttributeError as error:
            LOG.debug('Cannot update the parameters of the parent theme: %s',
                      error)
        except KeyError:
            theme_variables['parameters'] = parameters
        try:
            include_files = subtheme_values.pop('include_files', {})
            theme_variables['include_files'].update(include_files)
        except AttributeError as error:
            LOG.debug('Cannot update the parameters of the parent theme: %s',
                      error)
        except KeyError:
            theme_variables['include_files'] = include_files
        theme_variables.update(subtheme_values)
        LOG.debug('Value of Theme Variables after loading theme `%s`: `%s`',
                  theme, theme_variables)
        LOG.debug('Theme `%s` is loaded successfully', theme)
    return theme_variables, theme_directory


def __load_theme_config(config_file,
                        theme_directory):
    """Update the theme's configuration by new_config."""
    LOG.debug('Load config file `%s` from the directory: %s',
              config_file, theme_directory)
    if not config_file:
        LOG.info('Config file is `None`. Break loading of it.')
        return None
    try:
        if not config_file.endswith('.yaml'):
            config_file += '.yaml'
    except TypeError:
        LOG.info('The path to the configuration file'
                 'is not string, it has type %s',
                 type(config_file))
        return None

    path_config_file = os.path.join(theme_directory,
                                    config_file)
    LOG.debug('Absolete path to config file `%s`',
              path_config_file)
    try:
        with open(path_config_file, 'r', encoding='utf-8') as file:
            subtheme_values = yaml.safe_load(file)
    except (IOError, FileNotFoundError, PermissionError) as error:
        LOG.debug(
            'Cannot load the config file `%s`, error: %s',
            path_config_file, error)
        return None
    except yaml.scanner.ScannerError as error:
        LOG.debug('error parse variables from file `%s`: %s',
                  path_config_file, error)
        return None
    return subtheme_values


def main():
    """Process the input command."""
    parser = create_argparser()
    arguments = parser.parse_args()
    init_logging(arguments.verbose * 10)
    themes_path = os.path.realpath(
        os.path.expanduser(arguments.themes_path))
    if not os.path.exists(themes_path):
        LOG.error('The path `%s` does not exist', themes_path)
        themes_path = config.THEMES_DIRECTORY
        LOG.debug('Use the default path: %s', themes_path)
    else:
        LOG.debug('OK! The path `%s` exists.', themes_path)
    if not os.path.isdir(themes_path):
        LOG.error('The path `%s` is not folder', themes_path)
        themes_path = config.THEMES_DIRECTORY
        LOG.debug('Use the default path: %s', themes_path)
    else:
        LOG.debug('OK! The path `%s` is folder', themes_path)
    arguments.themes_path = themes_path
    arguments.func(arguments)


if __name__ == "__main__":
    main()
