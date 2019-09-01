"""Test for theme's initialisation."""
from io import StringIO
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import (safe_load,
                  safe_dump)
import coculatex.config as config
from coculatex.init_action import handler


class ThemeLoaderTestCase(unittest.TestCase):
    """Test Case for function `extract_variables`."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        self.out_dir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.themes_config = {
            'alpha': (
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
            ),
            'a': (
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
            ),
            'alpha{sep}a'.format(sep=config.THEME_NAME_SEP): (
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
            ),
            'a1': (
                '{parameters}:\n'
                '    param3: newtest111\n'
                '{root_file}: 1.tex\n'
                '{tex}:\n'
                '    option1: val1111\n'
                '    option4: 11111\n'
                '{jinja2_config}: {{}}\n'
                ''.format(**config.SECTION_NAMES_CONFIG)
            ),
            'alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP): (
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
        }
        self.themes = {
            'alpha': safe_load(StringIO(self.themes_config['alpha'])),
            'alpha{sep}a'.format(sep=config.THEME_NAME_SEP):
                safe_load(StringIO(self.themes_config[
                    'alpha{sep}a'.format(sep=config.THEME_NAME_SEP)])),
            'alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP):
                safe_load(StringIO(self.themes_config[
                    'alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP)]))
        }
        self.make_diretory_tree()

    def make_diretory_tree(self):
        """Make the directories tree."""
        for name, theme in self.themes.items():
            makedirs(path.dirname(theme['path']), exist_ok=True)
            with open(theme['path'], 'w') as file:
                file.write(self.themes_config[name])

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()
        self.out_dir.cleanup()

    def test_init_default_theme(self):
        """Test init the theme, default parameters."""
        handler('alpha', output_directory=self.out_dir.name)
        out_path = path.join(self.out_dir.name,
                             'alpha' + '.yaml')
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'alpha'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), safe_dump(params, sort_keys=False))

    def test_init_embed_theme(self):
        """Test init the theme, embeded configuration."""
        handler('alpha', output_directory=self.out_dir.name, embed=True)
        out_path = path.join(self.out_dir.name,
                             'alpha' + '.{}'.format(
                                 config.LTCONFIG['source_ext']))
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'alpha'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        content = ''
        for line in safe_dump(params, sort_keys=False).split('\n'):
            if line:
                content += '{} {}\n'.format(
                    config.LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)

    def test_init_project_theme(self):
        """Test init the theme, specify project-name, not embed."""
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name)
        out_path = path.join(self.out_dir.name,
                             'my_project' + '.yaml')
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), safe_dump(params, sort_keys=False))

    def test_init_project_embed_theme(self):
        """Test init the theme, specify project-name, embeded configuration."""
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name, embed=True)
        out_path = path.join(self.out_dir.name,
                             'my_project' + '.{}'.format(
                                 config.LTCONFIG['source_ext']))
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        content = ''
        for line in safe_dump(params, sort_keys=False).split('\n'):
            if line:
                content += '{} {}\n'.format(
                    config.LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)

    def test_init_project_subsubtheme(self):
        """Test init the subsubtheme, specify project-name, not embed."""
        handler('alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP),
                project_name='my_project',
                output_directory=self.out_dir.name)
        out_path = path.join(self.out_dir.name,
                             'my_project' + '.yaml')
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha{sep}a{sep}a1'.format(
            sep=config.THEME_NAME_SEP),
                  'project-name': 'my_project'}
        params.update(
            self.themes[
                'alpha{sep}a{sep}a1'.format(
                    sep=config.THEME_NAME_SEP)].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), safe_dump(params, sort_keys=False))

    def test_init_subsubtheme(self):
        """Test init the subsubtheme, not embed."""
        handler('alpha{sep}a{sep}a1'.format(sep=config.THEME_NAME_SEP),
                output_directory=self.out_dir.name)
        out_path = path.join(self.out_dir.name,
                             'alpha{sep}a{sep}a1'.format(
                                 sep=config.THEME_NAME_SEP) + '.yaml')
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha{sep}a{sep}a1'.format(
            sep=config.THEME_NAME_SEP),
                  'project-name': 'alpha{sep}a{sep}a1'.format(
                      sep=config.THEME_NAME_SEP)}
        params.update(
            self.themes[
                'alpha{sep}a{sep}a1'.format(
                    sep=config.THEME_NAME_SEP)].get('parameters', {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), safe_dump(params, sort_keys=False))

    def test_init_project_embed_subtheme(self):
        """Test init the subtheme, specify project, embed config."""
        handler('alpha{sep}a'.format(sep=config.THEME_NAME_SEP),
                project_name='my_project',
                output_directory=self.out_dir.name, embed=True)
        out_path = path.join(self.out_dir.name,
                             'my_project' + '.{}'.format(
                                 config.LTCONFIG['source_ext']))
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha{sep}a'.format(sep=config.THEME_NAME_SEP),
                  'project-name': 'my_project'}
        params.update(self.themes[
            'alpha{sep}a'.format(sep=config.THEME_NAME_SEP)].get('parameters',
                                                                 {}))
        params.update({'tex-preambule': '', 'tex-options': {}})
        content = ''
        for line in safe_dump(params, sort_keys=False).split('\n'):
            if line:
                content += '{} {}\n'.format(
                    config.LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)


if __name__ == '__main__':
    unittest.main(verbosity=0)
