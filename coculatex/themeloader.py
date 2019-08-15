"""The module containing the function for loading themes."""
import logging
from os import (path,
                listdir)
from yaml import safe_load
from yaml.scanner import ScannerError
from coculatex import config

LOG = logging.getLogger(__name__)


def load_theme_from_iterable(iterable):
    """Load a theme from the iterable source.

    :param: `iterable` - any iterable type
    :return: the theme configuration dictionary (see `config.THEME_CONFIG`)

    Note! That function does not set the `path` and the `name`
          of the theme configuration
    """
    theme_config = config.make_empty_theme()
    try:
        theme_config.update({
            key: value for key, value in safe_load(iterable).items()
            if key in config.THEME_CONFIG and
            isinstance(value, config.THEME_CONFIG[key])})
    except ScannerError as error:
        LOG.debug('cannot load theme, error parse configuration `%s`: %s',
                  dict(iterable), error)
        return {}
    except AttributeError:
        LOG.debug('Iterable does not contain any information.')
        return {}
    normalizer = {}
    for section, value in theme_config.items():
        if (config.THEME_CONFIG[section] == (list, str) and
                isinstance(value, str)):
            normalizer[section] = value.split(' ')
    theme_config.update(normalizer)
    return theme_config


def load_theme_from_path(filepath):
    """Load the theme from the path.

    :param: `filepath` - the path to the theme config file
    :return: the theme configuration dictionary (see `config.THEME_CONFIG`)
    Note! That function does not set the `name` of the theme configuration
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            theme_config = load_theme_from_iterable(file)
    except (FileNotFoundError, IOError, PermissionError) as error:
        LOG.debug('Cannot read the path `%s`: %s', path, error)
        return {}
    theme_config['path'] = filepath
    return theme_config


def load_theme(name):
    """Load the theme with name.

    :param: `name` - the theme's name
    :return: the theme configuration dictionary (see `config.THEME_CONFIG`)
    """
    LOG.debug('Load theme `%s` from path: `%s`', name, config.THEMES_PATH)
    splited_names = name.split(config.THEME_NAME_SEP)
    theme_path = path.join(config.THEMES_PATH, splited_names[0])
    LOG.debug('The theme\'s path: %s', theme_path)
    subthemes = splited_names[1:]
    theme_config = load_theme_from_path(path.join(
        theme_path,
        path.normpath(config.THEME_CONFIG_FILENAME)))
    LOG.debug('The config of the theme `%s`: `%s`',
              splited_names[0], theme_config)
    for theme in subthemes:
        LOG.debug('Load subtheme `%s`', theme)
        config_filename = theme_config.get(
            config.SECTION_NAMES_CONFIG['subthemes'], {}).get(theme, '')
        LOG.debug('The config file of the subtheme `%s`: %s',
                  theme, config_filename)
        subtheme_config = load_theme_from_path(
            path.join(path.dirname(theme_config['path']),
                      path.normpath(config_filename)))
        LOG.debug('The config of the subtheme %s: %s', theme, subtheme_config)
        __update_dict(theme_config, subtheme_config,
                      ['parameters', 'include_files', 'jinja2_config'])
        LOG.debug('The value of the theme variables after '
                  'loading subtheme `%s`: `%s`',
                  theme, theme_config)
        theme_config.update(subtheme_config)
    return theme_config


def themes_iter(name=None):
    """Iterate over theme's.

    :param: `str` name - name of the theme
    :return: python iterator object over all registered themes,
             or over all subthemes if the theme's name is specified.
    """
    if name:
        LOG.debug('Init iterator over subtheme of the theme: %s', name)
        theme_config = load_theme(name)
        LOG.debug('Load the configuration of the theme %s: %s',
                  name, theme_config)
        if not theme_config:
            return
        try:
            theme_list = [
                '{root}{sep}{theme}'.format(root=name,
                                            sep=config.THEME_NAME_SEP,
                                            theme=theme)
                for theme in theme_config.get(
                    config.SECTION_NAMES_CONFIG['subthemes'], {}).keys()
                ]
        except (TypeError, AttributeError):
            LOG.warning('Configuration theme `%s` error. '
                        'Block `%s` has incorrect type: expected'
                        ' `dict`, but got `%s`',
                        name,
                        config.SECTION_NAMES_CONFIG['subthemes'],
                        type(theme_config.get(
                            config.SECTION_NAMES_CONFIG['subthemes'])))
            return
    else:
        LOG.debug('Init iterator over all registered themes')
        theme_list = listdir(config.THEMES_PATH)

    for theme in theme_list:
        subtheme_config = load_theme(theme)
        if not subtheme_config:
            continue
        yield theme, subtheme_config


def __update_dict(old, new, sections):
    """Update the `old` dictionary with the values of the new.

    :param: old - `dict`, old dictionary
    :param: new - `dict`, new dictionary
    :param: sections - `iist` of the section names of the dictionary
                        which is will be updated
    """
    for sect in sections:
        try:
            old[config.SECTION_NAMES_CONFIG[sect]].update(
                new.pop(config.SECTION_NAMES_CONFIG[sect], {})
                )
        except TypeError:
            LOG.debug('Cannot update the %s of the parent theme. '
                      'Wrong type of the subsection: '
                      'expected `dict`',
                      sect)
