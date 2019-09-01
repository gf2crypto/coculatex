"""Test for the list themes functions."""
from io import StringIO
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import safe_load
import coculatex.config as config
from coculatex.list_action import (handler,
                                   SHIFT_SIZE)


class ListThemesTestCase(unittest.TestCase):
    """Test Case for list themes functionality."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        self.themes_config = {
            'a': (
                'path: {path}\n'
                '{description}: this is theme a\n'
                '{subthemes}:\n'
                '    a1: a1.yaml\n'
                '    a2: a2.yaml\n'
                '    a3: a3.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'config.yaml'))
            ),
            'a1': (
                'path: {path}\n'
                '{description}: |\n'
                '    this is theme a1\n'
                '    this is multiline description\n'
                '    this is the last line\n'
                '{subthemes}:\n'
                '    a11: a11.yaml\n'
                '    a12: a12.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'a1.yaml'))
            ),
            'a11': (
                'path: {path}\n'
                '{description}: hello, this is a11\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'a11.yaml'))
            ),
            'a12': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'a', 'a12.yaml'))
            ),
            'a2': (
                'path: {path}\n'
                '{description}: |\n'
                '    this is theme a2\n'
                '    this is multiline description\n'
                '    this is the last line\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'a2.yaml'))
            ),
            'a3': (
                'path: {path}\n'
                '{root_file}: a3.tex\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'a', 'a3.yaml'))
            ),
            'b': (
                'path: {path}\n'
                '{description}: |\n'
                '    this is theme BBBBB\n'
                '    this is multiline description\n'
                '    this is the last line\n'
                '{subthemes}:\n'
                '    b1: b1.yaml\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'b', 'config.yaml'))
            ),
            'b1': (
                'path: {path}\n'
                ''.format(path=path.join(self.tempdir.name,
                                         'b', 'b1.yaml'))
            ),
            'c': (
                'path: {path}\n'
                '{root_file}: c.tex\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name,
                                         'c', 'config.yaml'))
            ),
        }
        self.themes = {}
        config.THEMES_PATH = self.tempdir.name
        self.make_files()

    def tearDown(self):
        """Clean after test."""
        self.tempdir.cleanup()

    def make_files(self):
        """Make directory tree."""
        for (name, conf_str) in self.themes_config.items():
            self.themes[name] = safe_load(StringIO(conf_str))
            makedirs(path.dirname(self.themes[name]['path']), exist_ok=True)
            with open(self.themes[name]['path'], 'w') as file:
                file.write('\n'.join(conf_str.split('\n')[1:]))

    def test_list_root_not_detailed(self):
        """Test list all themes, not detailed."""
        self.assertEqual(sorted('a b c '.split(' ')),
                         sorted(handler().split(' ')))

    def test_list_root_detailed(self):
        """Test list all themes, not detailed."""
        out_str = ''
        for name in [n for n in handler().split(' ') if n]:
            desc = self.themes[name].get(
                config.SECTION_NAMES_CONFIG['description'],
                'no description')
            desc = '\n'.join([SHIFT_SIZE * ' ' + line
                              for line in desc.split('\n') if line])
            subthemes = ' '.join(
                self.themes[name].get(config.SECTION_NAMES_CONFIG['subthemes'],
                                      {}).keys())
            if not subthemes:
                subthemes = 'not provided'
            out_str += (
                '{name}\n'
                '{desc}\n\n'
                '{shift}Subthemes: {subthemes}\n'
                ''.format(name=name, desc=desc,
                          shift=SHIFT_SIZE * ' ', subthemes=subthemes)
                )
        self.assertEqual(out_str, handler(detail=True))

    def test_list_theme_not_detailed(self):
        """Test list all themes, not detailed."""
        self.assertEqual('a{sep}a1 a{sep}a2 a{sep}a3 '.format(
            sep=config.THEME_NAME_SEP), handler('a'))

    def test_list_theme_detailed(self):
        """Test list all themes, not detailed."""
        out_str = ''
        for name in ['a1', 'a2', 'a3']:
            desc = self.themes[name].get(
                config.SECTION_NAMES_CONFIG['description'],
                'no description')
            desc = '\n'.join([SHIFT_SIZE * ' ' + line
                              for line in desc.split('\n') if line])
            subthemes = ' '.join(
                self.themes[name].get(config.SECTION_NAMES_CONFIG['subthemes'],
                                      {}).keys())
            if not subthemes:
                subthemes = 'not provided'
            out_str += (
                'a{sep}{name}\n'
                '{desc}\n\n'
                '{shift}Subthemes: {subthemes}\n'
                ''.format(sep=config.THEME_NAME_SEP, name=name, desc=desc,
                          shift=SHIFT_SIZE * ' ', subthemes=subthemes)
                )
        self.assertEqual(out_str, handler('a', detail=True))


if __name__ == '__main__':
    unittest.main(verbosity=0)
