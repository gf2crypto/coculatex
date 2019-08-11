"""Test for theme's loader."""
from io import StringIO
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import safe_load
import coculatex.config as config
from coculatex.themeloader import load_theme


class ThemeLoaderTestCase(unittest.TestCase):
    """Test Case for function `extract_variables`."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.theme_alpha_config = (
            'path: {path}\n'
            '{subthemes}:\n'
            '    a: a/a.yaml\n'
            '    b: b.yaml\n'
            '{parameters}:\n'
            '    param1: test1\n'
            '    param2: test2\n'
            '{description}: is alpha theme for the test\n'
            '{root_file}: alpha.tex\n'
            '{tex}:\n'
            '    option1: val1\n'
            '    option2: 25\n'
            '    option3: [1, 2, 3]\n'
            '{include_files}:\n'
            '    file1.tex: template_file1.tex\n'
            '    file2.tex: template_file2.tex\n'
            '{readme}: readme.txt\n'
            '{example}: examples/alpha\n'
            '{jinja2_config}:\n'
            '    autoescape: true\n'
            '    line_comment_prefix:' r' "%%##"' '\n'
            ''.format(**config.SECTION_NAMES_CONFIG,
                      path=path.join(self.tempdir.name, 'alpha',
                                     'config.yaml'))
            )

        self.subtheme_a_config = (
            '{subthemes}:\n'
            '    a1: 1.yaml\n'
            '{parameters}:\n'
            '    param1: test1a\n'
            '    param2: test2a\n'
            '    param3: newtestA\n'
            '{description}: is `a` theme of the alpha subtheme\n'
            '{root_file}: a.tex\n'
            '{tex}:\n'
            '    option1: val1a\n'
            '    option2: AA\n'
            '    option3: [4, 5, 6]\n'
            '{include_files}:\n'
            '    file1.tex: template_file1a.tex\n'
            '    file2.tex: template_file2a.tex\n'
            '    file3.tex: template_file3a.tex\n'
            '{readme}: readmeA.txt\n'
            '{example}: examples/a\n'
            ''.format(**config.SECTION_NAMES_CONFIG)
            )

        self.theme_alpha_a_config = (
            'path: {path}\n'
            '{subthemes}:\n'
            '    a1: 1.yaml\n'
            '{parameters}:\n'
            '    param1: test1a\n'
            '    param2: test2a\n'
            '    param3: newtestA\n'
            '{description}: is `a` theme of the alpha subtheme\n'
            '{root_file}: a.tex\n'
            '{tex}:\n'
            '    option1: val1a\n'
            '    option2: AA\n'
            '    option3: [4, 5, 6]\n'
            '{include_files}:\n'
            '    file1.tex: template_file1a.tex\n'
            '    file2.tex: template_file2a.tex\n'
            '    file3.tex: template_file3a.tex\n'
            '{readme}: readmeA.txt\n'
            '{example}: examples/a\n'
            '{jinja2_config}:\n'
            '    autoescape: true\n'
            '    line_comment_prefix:' r' "%%##"' '\n'
            ''.format(**config.SECTION_NAMES_CONFIG,
                      path=path.join(self.tempdir.name, 'alpha',
                                     'a', 'a.yaml'))
            )

        self.subtheme_1_config = (
            '{parameters}:\n'
            '    param3: newtest111\n'
            '{root_file}: 1.tex\n'
            '{tex}:\n'
            '    option1: val1111\n'
            '    option4: 11111\n'
            '{jinja2_config}: {{}}\n'
            ''.format(**config.SECTION_NAMES_CONFIG)
            )

        self.theme_alpha_a_1_config = (
            'path: {path}\n'
            '{subthemes}: {{}}\n'
            '{parameters}:\n'
            '    param1: test1a\n'
            '    param2: test2a\n'
            '    param3: newtest111\n'
            '{description}: ""\n'
            '{root_file}: 1.tex\n'
            '{tex}:\n'
            '    option1: val1111\n'
            '    option2: AA\n'
            '    option3: [4, 5, 6]\n'
            '    option4: 11111\n'
            '{include_files}:\n'
            '    file1.tex: template_file1a.tex\n'
            '    file2.tex: template_file2a.tex\n'
            '    file3.tex: template_file3a.tex\n'
            '{readme}: ""\n'
            '{example}: ""\n'
            '{jinja2_config}:\n'
            '    autoescape: true\n'
            '    line_comment_prefix:' r' "%%##"' '\n'
            ''.format(**config.SECTION_NAMES_CONFIG,
                      path=path.join(self.tempdir.name, 'alpha',
                                     'a', '1.yaml'))
            )
        self.theme_alpha = safe_load(StringIO(self.theme_alpha_config))
        self.theme_alpha_a = safe_load(StringIO(self.theme_alpha_a_config))
        self.theme_alpha_a_1 = safe_load(StringIO(self.theme_alpha_a_1_config))
        self.make_diretory_tree()

    def make_diretory_tree(self):
        """Make the directories tree."""
        makedirs(path.dirname(self.theme_alpha_a['path']))
        with open(self.theme_alpha['path'], 'w') as file:
            file.write(self.theme_alpha_config)
        with open(self.theme_alpha_a['path'], 'w') as file:
            file.write(self.subtheme_a_config)
        with open(self.theme_alpha_a_1['path'], 'w') as file:
            file.write(self.subtheme_1_config)

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()

    def test_load_root_theme(self):
        """Test load the root theme."""
        theme = load_theme('alpha')
        self.assertEqual(theme.items(), self.theme_alpha.items())

    def test_load_subtheme(self):
        """Test load the subtheme."""
        theme = load_theme('alpha{sep}a'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.theme_alpha_a.items())

    def test_load_subsubtheme(self):
        """Test load the subsubtheme."""
        theme = load_theme(
            'alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.theme_alpha_a_1.items())

    def test_theme_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('beta')
        self.assertEqual(theme.items(), {}.items())

    def test_subtheme_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('alpha{sep}beta'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.theme_alpha.items())

    def test_subtheme_config_not_exits(self):
        """Test load the subsubtheme."""
        theme = load_theme('alpha{sep}b'.format(sep=config.THEME_NAME_SEP))
        self.assertEqual(theme.items(), self.theme_alpha.items())


if __name__ == '__main__':
    unittest.main(verbosity=0)
