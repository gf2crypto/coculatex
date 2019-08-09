"""
    Configuration variables for ALL modules
"""
import os
import logging
from collections import namedtuple


LOG = logging.getLogger(__name__)

# ------------JINJA2 Config----------------------------------------------------

Jinja2Config = namedtuple(
    'jinja2',
    ('BLOCK_START_STRING BLOCK_END_STRING VARIABLE_START_STRING '
     'VARIABLE_END_STRING COMMENT_START_STRING COMMENT_END_STRING '
     'LINE_STATEMENT_PREFIX LINE_COMMENT_PREFIX TRIM_BLOCKS AUTOESCAPE'))


JINJA2_DEFAULT_CONFIG = Jinja2Config(
    BLOCK_START_STRING=r'\BLOCK{',
    BLOCK_END_STRING='}',
    VARIABLE_START_STRING=r'\VAR{',
    VARIABLE_END_STRING='}',
    COMMENT_START_STRING=r'\#{',
    COMMENT_END_STRING='}',
    LINE_STATEMENT_PREFIX=r'%%',
    LINE_COMMENT_PREFIX=r'%#',
    TRIM_BLOCKS=True,
    AUTOESCAPE=False)


# ------------LaTeX Template Config--------------------------------------------

LatexTemplateConfig = namedtuple(
    'latex_template',
    'LINE_STATEMENT_PREFIX')


LATEX_TEMPLATE_DEFAULT_CONFIG = LatexTemplateConfig(
    LINE_STATEMENT_PREFIX=r'%%=')

YAML_LINE_PREFIX = r'%%='
# -----------------------------------------------------------------------------

THEMES_DIRECTORY = os.path.realpath(os.path.expanduser('~/latextm_themes'))

THEME_CONFIG_FILE_NAME = 'config.yaml'

THEME_SUBTHEMES = 'subthemes'

OUTPUT_DIR = ''

DEFAULT_ROOT_TEX = 'root.tex'

LTM_FILE_EXTENSION = 'ltm'

VERSION_STRING_TEMPLATE = "LaTeXTM {version} by Ivan Chizhov"


def config_iter(config):
    """
        Iteration over configuration values
    """
    for attr_name, attr_value in _namedtuple_iter(config):
        yield attr_name.lower(), attr_value


def _namedtuple_iter(named_tuple):
    """
        Iteration over attributes and values of namedtuple object
    """
    for attr_name in named_tuple._fields:
        yield attr_name, getattr(named_tuple, attr_name)


def set_user_config(config, user_config):
    """
        Function set user configuration
        config - `namedtuple` config instance
        user_config - `dict` with user config
    """
    LOG.debug('Changing configuration: %r', config)
    user_config = user_config.get(config.__class__.__name__, {})
    LOG.debug('Using user configuration: %s', user_config)
    new_config = {}
    for attr_name, attr_value in _namedtuple_iter(config):
        LOG.debug('Processing attribute `%s` (default value = %s)',
                  attr_name, attr_value)
        value = user_config.get(attr_name.lower())
        LOG.debug('User value of attribute `%s`: %s', attr_name, value)
        new_config[attr_name] = (value
                                 if isinstance(value, type(attr_value))
                                 else attr_value)
        LOG.debug('New value of attribute `%s`: %s',
                  attr_name, new_config[attr_name])
    LOG.debug('Final configuration: %s', new_config)
    return config.__class__(**new_config)
