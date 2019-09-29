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


class ThemeInitTestCase(unittest.TestCase):
    """Test Case for init theme."""

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
                '{tex_program}: pdflatex\n'
                '{tex_options}:\n'
                '    - option1\n'
                '    - option2\n'
                '    - option3\n'
                '{include_files}:\n'
                '    file1.tex: template_file1.tex\n'
                '    file2.tex: template_file2.tex\n'
                '{readme}: readme.txt\n'
                '{example}:\n'
                '    path: examples/alpha\n'
                '    sources:\n'
                '        - section01.tex\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'config.yaml'))
            ),
        }
        self.themes = {
            'alpha': safe_load(StringIO(self.themes_config['alpha'])),
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
                             config.THEME_CONFIG_FILENAME)
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'alpha'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': []})
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
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': []})
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
                             config.THEME_CONFIG_FILENAME)
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        params.update(self.themes['alpha'].get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': []})
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
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': []})
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


class ThemeInitMakeExampleTestCase(unittest.TestCase):
    """Test Case for init theme and make the example sources."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        self.out_dir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.themes_config = {
            'alpha_one_source': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a: a/a.yaml\n'
                '    b: b.yaml\n'
                '{parameters}:\n'
                '    param1: test1\n'
                '    param2: test2\n'
                '{description}: is alpha theme for the test\n'
                '{root_file}: alpha.tex\n'
                '{tex_program}: pdflatex\n'
                '{tex_options}:\n'
                '    - option1\n'
                '    - option2\n'
                '    - option3\n'
                '{include_files}:\n'
                '    file1.tex: template_file1.tex\n'
                '    file2.tex: template_file2.tex\n'
                '{readme}: readme.txt\n'
                '{example}:\n'
                '    path: examples/alpha\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'config.yaml'))
            ),
            'alpha_multiple_sources': (
                'path: {path}\n'
                '{subthemes}:\n'
                '    a: a/a.yaml\n'
                '    b: b.yaml\n'
                '{parameters}:\n'
                '    param1: test1\n'
                '    param2: test2\n'
                '{description}: is alpha theme for the test\n'
                '{root_file}: alpha.tex\n'
                '{tex_program}: pdflatex\n'
                '{tex_options}:\n'
                '    - option1\n'
                '    - option2\n'
                '    - option3\n'
                '{include_files}:\n'
                '    file1.tex: template_file1.tex\n'
                '    file2.tex: template_file2.tex\n'
                '{readme}: readme.txt\n'
                '{example}:\n'
                '    path: examples/alpha\n'
                '    sources:\n'
                '        - section01.tex\n'
                '        - section02.tex\n'
                '{jinja2_config}:\n'
                '    autoescape: true\n'
                '    line_comment_prefix:' r' "%%##"' '\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.tempdir.name, 'alpha',
                                         'config.yaml'))
            ),
        }
        self.examples_one_source = {
            config.LTCONFIG['root_file']: (
                '\\usepackage{{mystyle}}\n'
                '\\begin{{document}}\n'
                '  \\section{{This is the first section}}\n'
                '    Hello, I\'m first section!\n'
                '    This is just text: bla, bla, bla\n'
                '\n\n\n'
                '  \\section{{This is the second section}}\n'
                '    Hello, I\'m second section!\n'
                '    The text of the section number 2.\n'
                '    Third line of the section\'s text\n'
                '\\end{{document}}\n'
                ),
            'pictures/pic.jpg': (
                'This is picture\n.'
                'Sorry, It is text picture.'
                ),
            'mystyle.sty': (
                '\\newcommand{{\\mycommand}}{{1}}{{\\textbf{{#1}}}}\n'
                )
        }
        self.examples_multiple_sources = {
            config.LTCONFIG['root_file']: (
                '\\usepackage{{mystyle}}\n'
                '\\begin{{document}}\n'
                '  \\include{{section01}}\n'
                '  \\include{{section02}}\n'
                '\\end{{document}}\n'
                ),
            'section01.tex': (
                '\\section{{This is the first section}}\n'
                'Hello, I\'m first section!\n'
                'This is just text: bla, bla, bla\n'
                ),
            'section02.tex': (
                '\\section{{This is the second section}}\n'
                'Hello, I\'m second section!\n'
                'The text of the section number 2.\n'
                'Third line of the section\'s text\n'
                ),
            'pictures/pic.jpg': (
                'This is picture\n.'
                'Sorry, It is text picture.'
                ),
            'mystyle.sty': (
                '\\newcommand{{\\mycommand}}{{1}}{{\\textbf{{#1}}}}\n'
                )
        }

    def make_directories_tree(self, one_source=True):
        """Make the directories tree."""
        if one_source:
            name = 'alpha_one_source'
            example = self.examples_one_source
        else:
            name = 'alpha_multiple_sources'
            example = self.examples_multiple_sources
        theme = safe_load(StringIO(self.themes_config[name]))
        path_theme = path.dirname(theme['path'])
        makedirs(path.dirname(path_theme), exist_ok=True)
        with open(theme['path'], 'w') as file:
            file.write(self.themes_config[name])
        dir_example = path.normpath(
            theme[config.SECTION_NAMES_CONFIG['example']])
        path_example = path.join(path_theme, dir_example)
        for file_name, source in example.items():
            path_file = path.join(path_example,
                                  path.normpath(file_name))
            makedirs(path.dirname(path_file), exist_ok=True)
            with open(path_file, 'w') as file:
                file.write(source)

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()
        self.out_dir.cleanup()

    def test_init_example_one_source_embed(self):
        """Test init the theme and make example, embeded configuration.

        Example has one source file.
        """
        self.make_directories_tree()
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name,
                embed=True, make_example=True)
        out_path = path.join(self.out_dir.name,
                             'my_project' + '.{}'.format(
                                 config.LTCONFIG['source_ext']))
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        theme = safe_load(StringIO(self.themes_config['alpha_one_source']))
        params.update(theme.get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': []})
        content = ''
        for line in safe_dump(params, sort_keys=False).split('\n'):
            if line:
                content += '{} {}\n'.format(
                    config.LTCONFIG['config_prefix'],
                    line)
            else:
                content += '\n'
        content += '\n'
        content += self.examples_one_source[config.LTCONFIG['root_file']]
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)
        for file_name, source in self.examples_one_source.items():
            if file_name == config.LTCONFIG['root_file']:
                continue
            file_path = path.join(self.out_dir.name,
                                  path.normpath(file_name))
            self.assertTrue(path.exists(file_path))
            with open(file_path, 'r') as file:
                self.assertEqual(file.read(), source)

    def test_init_example_multiple_source_embed(self):
        """Test init the theme and make example, embeded configuration.

        Example has multiple sources file.
        """
        self.make_directories_tree(one_source=False)
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name,
                embed=True, make_example=True)
        root_tex = 'my_project' + '.{}'.format(config.LTCONFIG['source_ext'])
        out_path = path.join(self.out_dir.name, root_tex)
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        theme = safe_load(StringIO(
            self.themes_config['alpha_multiple_source']))
        params.update(theme.get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': theme.get(
                config.SECTION_NAMES_CONFIG['example'],
                {}).get('sources', [])})
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
        for file_name, source in self.examples_multiple_sources.items():
            if file_name == config.LTCONFIG['root_tex']:
                file_name = root_tex
            file_path = path.join(self.out_dir.name,
                                  path.normpath(file_name))
            self.assertTrue(path.exists(file_path))
            with open(file_path, 'r') as file:
                self.assertEqual(file.read(), source)

    def test_example_not_embeded_one_source(self):
        """Test init the theme and make example, not embeded configuration.

        Example has one source file.
        """
        self.make_directories_tree()
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name,
                embed=True, make_example=True)
        out_path = path.join(self.out_dir.name,
                             config.THEME_CONFIG_FILENAME)
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        theme = safe_load(StringIO(self.themes_config['alpha_one_source']))
        params.update(theme.get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': theme.get(
                config.SECTION_NAMES_CONFIG['example'],
                {}).get('sources', [])})
        content = safe_dump(params, sort_keys=False)
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)
        for file_name, source in self.examples_one_source.items():
            if file_name == config.LTCONFIG['root_file']:
                file_name = 'my_project.{}'.format(
                    config.LTCONFIG['source_ext'])
            file_path = path.join(self.out_dir.name,
                                  path.normpath(file_name))
            self.assertTrue(path.exists(file_path))
            with open(file_path, 'r') as file:
                self.assertEqual(file.read(), source)

    def test_example_not_embeded_multiple_source(self):
        """Test init the theme and make example, not embeded configuration.

        Example has one source file.
        """
        self.make_directories_tree()
        handler('alpha', project_name='my_project',
                output_directory=self.out_dir.name,
                embed=True, make_example=True)
        out_path = path.join(self.out_dir.name,
                             config.THEME_CONFIG_FILENAME)
        self.assertTrue(path.exists(out_path))
        params = {'theme': 'alpha', 'project-name': 'my_project'}
        theme = safe_load(StringIO(self.themes_config['alpha_one_source']))
        params.update(theme.get('parameters', {}))
        params.update({
            'tex-options': [],
            'tex-preambule': '',
            'tex-sources': theme.get(
                config.SECTION_NAMES_CONFIG['example'],
                {}).get('sources', [])})
        content = safe_dump(params, sort_keys=False)
        with open(out_path, 'r', encoding='utf-8') as file:
            self.assertEqual(file.read(), content)
        for file_name, source in self.examples_multiple_sources.items():
            if file_name == config.LTCONFIG['root_file']:
                file_name = 'my_project.{}'.format(
                    config.LTCONFIG['source_ext'])
            file_path = path.join(self.out_dir.name,
                                  path.normpath(file_name))
            self.assertTrue(path.exists(file_path))
            with open(file_path, 'r') as file:
                self.assertEqual(file.read(), source)


if __name__ == '__main__':
    unittest.main(verbosity=0)
