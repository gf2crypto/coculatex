"""Module contains functions for working with various templates."""
import logging
import os
import yaml
from jinja2 import BaseLoader, TemplateNotFound
from latextm import config


LOG = logging.getLogger(__name__)


class TemplateLoader(BaseLoader):
    """Redefined BaseLoader to specify path where search the templates."""

    def __init__(self, path):
        """Init the Loader by using path variabel."""
        self.path = path
        LOG.debug('Define the TemplateLoader for the path %s', self.path)

    def get_source(self, environment, template):
        """Get the source file for the template."""
        path = os.path.join(self.path, template)
        if not os.path.exists(path):
            raise TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with open(path, encoding='utf-8') as file:
            source = file.read()
        return source, path, lambda: mtime == os.path.getmtime(path)


def extract_variables(file):
    """
    Extract variables from templates.

    :file: - file object or any similar (iterable) object
    :return:
        `dict` variables, - the dictionary that contains variables
        `str` clear_template - file lines cleared of variables
    """
    LOG.debug("Extract variables from iterables")
    prefix = config.YAML_LINE_PREFIX
    LOG.debug("Prefix of line which is contains varibales: %s", prefix)
    len_prefix = len(prefix)
    var_strings = ''
    cleared_template = ''
    for line in file:
        if len(line) >= len_prefix and line[:len_prefix] == prefix:
            var_strings += line[len_prefix:]
        else:
            cleared_template += line
    try:
        values = yaml.safe_load(var_strings)
    except yaml.scanner.ScannerError as error:
        LOG.debug('The problem happens while load values from '
                  'the string %s: %s', var_strings, error)
        values = {}
    return values, cleared_template
