"""Configuration variables for ALL modules."""

from os import path

# The default path to the user configuration folder
USER_CONFIG_PATH = path.realpath(path.expanduser('~/.coculatex'))

# The working directory
WORKING_DIRECTORY = ''  # the default is the current folder

# The path to the directory containing themes
THEMES_PATH = path.join(USER_CONFIG_PATH, 'themes')

# The separator of the name parts
THEME_NAME_SEP = '.'

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
    'config_prefix': r'%%=',  # prefix for the line
                              # contained the template variables
    'source_ext': 'source.tex',  # extension of the source tex file
    'tex_ext': 'tex',
    'root_file': 'root.tex',  # the name of the root TeX-file
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
    'root_file': 'root-file',  # the name of the block contained
                               # the root file name
    'tex_options': 'tex-options',       # the block containing
                                        # the tex additional options
    'tex_program': 'tex-program',       # the block containing
                                        # the tex additional options
    'include_files': 'include-files',  # the name of the block containing
                                       # the dictionary of the additional files
                                       # which would be copied to
                                       # the working directory
                                       # format:
                                       # destination_file: source_file
    'readme': 'readme',  # the name of the block containing the name of
                         # the readme file
    'example': 'example',  # the name of the block containing the relaitive
                           # theme directory path to the example file
    'jinja2_config': 'jinja2-config'  # the name of the block containing
                                      # the configuration of jinja2 template
}

# Additiona theme variables which is specified in user configuration
PARAMETERS_NAMES_CONFIG = {
    'theme': 'theme',  # the theme's name block
    'project_name': 'project-name',  # the project name's block
    'tex_preambule': 'tex-preambule',  # the block containing the tex preambule
    'tex_sources': 'tex-sources',  # the list of sources file block
    'tex_options': SECTION_NAMES_CONFIG['tex_options']
}

# This parameters will add in the begin of the configuration
PARAMETERS_BEGIN = [
    PARAMETERS_NAMES_CONFIG['theme'],
    PARAMETERS_NAMES_CONFIG['project_name']
]

# This parameters will add in the end of the configuration
PARAMETERS_END = [
    PARAMETERS_NAMES_CONFIG['tex_options'],
    PARAMETERS_NAMES_CONFIG['tex_preambule'],
    PARAMETERS_NAMES_CONFIG['tex_sources'],
]

# The theme's configuration

THEME_CONFIG = {
    'path': str,  # the path to the theme
    SECTION_NAMES_CONFIG['subthemes']: dict,  # the subthemes
    SECTION_NAMES_CONFIG['parameters']: dict,  # the template's parameters
    SECTION_NAMES_CONFIG['description']: str,  # the description of the theme
    SECTION_NAMES_CONFIG['root_file']: str,  # the root file name
    # the compiling TeX options
    SECTION_NAMES_CONFIG['tex_options']: (list, str),
    SECTION_NAMES_CONFIG['tex_program']: str,  # the compiling TeX options
    SECTION_NAMES_CONFIG['include_files']: dict,  # the theme's addition files
    SECTION_NAMES_CONFIG['readme']: str,  # the readme file name
    SECTION_NAMES_CONFIG['example']: dict,  # the relative path to the example
    SECTION_NAMES_CONFIG['jinja2_config']: dict  # the jinja2's configuration
}

# The theme's parameters section configuration
THEME_PARAMETERS_CONFIG = {
    PARAMETERS_NAMES_CONFIG['theme']: str,
    PARAMETERS_NAMES_CONFIG['project_name']: str,
    PARAMETERS_NAMES_CONFIG['tex_preambule']: str,
    PARAMETERS_NAMES_CONFIG['tex_options']: (
        THEME_CONFIG[SECTION_NAMES_CONFIG['tex_options']]),
    PARAMETERS_NAMES_CONFIG['tex_sources']: (list, str)
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


def make_empty_theme():
    """Make empty theme."""
    theme = {
        key: value()
        for key, value in THEME_CONFIG.items()
        if not isinstance(value, tuple)
    }
    theme.update({
        key: list(value)[0]()
        for key, value in THEME_CONFIG.items()
        if isinstance(value, tuple)
        })
    return theme


def make_default_params():
    """Make default theme's parameters."""
    params = {
        key: value()
        for key, value in THEME_PARAMETERS_CONFIG.items()
        if not isinstance(value, tuple)
    }
    params.update({
        key: list(value)[0]()
        for key, value in THEME_PARAMETERS_CONFIG.items()
        if isinstance(value, tuple)
        })
    return params
