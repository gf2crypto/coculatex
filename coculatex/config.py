"""Configuration variables for ALL modules."""

from os import path

# The default path to the user configuration folder
USER_CONFIG_PATH = path.realpath(path.expanduser('~/.coculatex'))

# The working directory
WORKING_DIRECTORY = ''  # the default is the current folder

# The path to the directory containing themes
THEMES_PATH = path.join(USER_CONFIG_PATH, 'themes')

# The separator of the name parts
THEME_NAME_SEP = ':'

# The name of the theme configuration file
THEME_CONFIG_FILENAME = 'config.yaml'

# ------------Jinja2 template config-------------------------------------------

J2CONFIG = {
    'block_start_string': r'\BLOCK{',
    'block_end_string': '}',
    'variable_start_string': r'\VAR{',
    'variable_end_string': '}',
    'comment_start_string': r'\#{',
    'comment_end_string': '}',
    'line_statement_prefix': r'%%',
    'line_comment_prefix': r'%#',
    'trim_blocks': True,
    'autoescape': False
}

# The LaTeX template config
LTCONFIG = {
    'config_prefix': r'%%='  # prefix for the line
                             # contained the template variables
}

# The names of the configuration file's sections
SECTION_NAMES_CONFIG = {
    'subthemes': 'subthemes',  # the name of the subthemes block in the config
                               # the subthemes block format:
                               # subtheme_name: name_of_root_file
    'parameters': 'parameters',  # the name of the block containing the values
                                 #  of the template variables
    'description': 'description',  # the name of the block
                                   # containing the theme's description
    'root_file': 'root_file',  # the name of the block contained
                               # the root file name
    'tex': 'tex',  # the name of block containing the TeX compiling options
    'include_files': 'include_files',  # the name of the block containing
                                       # the dictionary of the additional files
                                       # which would be copied to
                                       # the working directory
                                       # format:
                                       # destination_file: source_file
    'readme': 'readme',  # the name of the block containing the name of
                         # the readme file
    'example': 'example',  # the name of the block containing the relaitive
                           # theme directory path to the example file
    'jinja2_config': 'jinja2_config'  # the name of the block containing
                                      # the configuration of jinja2 template
}

# The theme's configuration

THEME_CONFIG = {
    'path': '',  # the path to the theme
    'name': '',  # the theme's name
    SECTION_NAMES_CONFIG['subthemes']: {},  # the subthemes
    SECTION_NAMES_CONFIG['parameters']: {},  # the template's parameters
    SECTION_NAMES_CONFIG['description']: '',  # the description of the theme
    SECTION_NAMES_CONFIG['root_file']: '',  # the root file name
    SECTION_NAMES_CONFIG['tex']: {},  # the compiling TeX options
    SECTION_NAMES_CONFIG['include_files']: {},  # the theme's addition files
    SECTION_NAMES_CONFIG['readme']: '',  # the readme file name
    SECTION_NAMES_CONFIG['example']: '',  # the relative path to the example
    SECTION_NAMES_CONFIG['jinja2_config']: {}  # the jinja2's configuration
}

# The list of the registered themes
REGISTERED_THEMES = {}

# The files to dump configuration

DUMP_FILES = {
    'registered_themes': path.join(USER_CONFIG_PATH,
                                   '.registered_themes.yaml'),
    'themes_directories': path.join(USER_CONFIG_PATH,
                                    '.themes_directories.yaml')
}
