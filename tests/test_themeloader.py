"""Test for theme's loader."""
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import safe_dump
import coculatex.config as config
from coculatex.themeloader import load_theme


class LoadParametersTestCase(unittest.TestCase):
    """Test Case for loading various parameters."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.theme_name = 'test_theme'
        self.theme = {
            'path': path.join(config.THEMES_PATH,
                              self.theme_name,
                              'config.yaml')
        }
        makedirs(path.dirname(self.theme['path']), exist_ok=True)
        self.maxDiff = None

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()

    def test_load_subthemes_param(self):
        """Test load `subthemes` block."""
        section = config.SECTION_NAMES_CONFIG['subthemes']
        self.theme[section] = {
            'sub1': 'sub1.yaml',
            'sub2': 'sub2.yaml'
        }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_parameters_param(self):
        """Test load `parameters` block."""
        section = config.SECTION_NAMES_CONFIG['parameters']
        self.theme[section] = {
            'param1': 'sub1.yaml',
            'param2': 'sub2.yaml'
        }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_description_param(self):
        """Test load `description` block."""
        section = config.SECTION_NAMES_CONFIG['description']
        self.theme[section] = 'This is too short description!'
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_root_file_param(self):
        """Test load `root_file` block."""
        section = config.SECTION_NAMES_CONFIG['root_file']
        self.theme[section] = 'file.tex'
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_tex_options_list_param(self):
        """Test load `tex_options` list block."""
        section = config.SECTION_NAMES_CONFIG['tex_options']
        self.theme[section] = [
            '--shell-escape', '--pdf-view', '--some-param', '-f'
            ]
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_tex_options_str_param(self):
        """Test load `tex_options` str block."""
        section = config.SECTION_NAMES_CONFIG['tex_options']
        self.theme[section] = [
            '--shell-escape', '--pdf-view', '--some-param', '-f'
            ]
        self.theme[section] = ' '.join(self.theme[section])
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        self.theme[section] = [
            '--shell-escape', '--pdf-view', '--some-param', '-f'
            ]
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_tex_program_param(self):
        """Test load `tex_program` block."""
        section = config.SECTION_NAMES_CONFIG['tex_program']
        self.theme[section] = 'xelatex'
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_include_files_param(self):
        """Test load `include_files` block."""
        section = config.SECTION_NAMES_CONFIG['include_files']
        self.theme[section] = {
            'file1': 'sub1.yaml',
            'file2': 'sub2.yaml'
        }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_jinja2_config_param(self):
        """Test load `jinja2_config` block."""
        section = config.SECTION_NAMES_CONFIG['jinja2_config']
        self.theme[section] = {
            'j2_c1': 'jj',
            'j2_c2': 'kkkkk'
        }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_readme_param(self):
        """Test load `readme` block."""
        section = config.SECTION_NAMES_CONFIG['readme']
        self.theme[section] = 'readme.txt'
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_example_param(self):
        """Test load `example` block."""
        section = config.SECTION_NAMES_CONFIG['example']
        self.theme[section] = {
            'path': 'example/theme1',
            'sources': [
                'source1', 'source2'
            ]
            }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())


class LoadParametersWrongTypeTestCase(unittest.TestCase):
    """Test Case for loading various parameters with wrong type."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.theme_name = 'test_theme'
        self.theme = {
            'path': path.join(config.THEMES_PATH,
                              self.theme_name,
                              'config.yaml')
        }
        makedirs(path.dirname(self.theme['path']), exist_ok=True)
        self.maxDiff = None

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()

    def test_load_subthemes_param(self):
        """Test load `subthemes` block."""
        section = config.SECTION_NAMES_CONFIG['subthemes']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_parameters_param(self):
        """Test load `parameters` block."""
        section = config.SECTION_NAMES_CONFIG['parameters']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_description_param(self):
        """Test load `description` block."""
        section = config.SECTION_NAMES_CONFIG['description']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_root_file_param(self):
        """Test load `root_file` block."""
        section = config.SECTION_NAMES_CONFIG['root_file']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_tex_options_list_param(self):
        """Test load `tex_options` list block."""
        section = config.SECTION_NAMES_CONFIG['tex_options']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_tex_program_param(self):
        """Test load `tex_program` block."""
        section = config.SECTION_NAMES_CONFIG['tex_program']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_include_files_param(self):
        """Test load `include_files` block."""
        section = config.SECTION_NAMES_CONFIG['include_files']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_jinja2_config_param(self):
        """Test load `jinja2_config` block."""
        section = config.SECTION_NAMES_CONFIG['jinja2_config']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_readme_param(self):
        """Test load `readme` block."""
        section = config.SECTION_NAMES_CONFIG['readme']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_load_example_param(self):
        """Test load `example` block."""
        section = config.SECTION_NAMES_CONFIG['example']
        self.theme[section] = 10
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        theme = load_theme(self.theme_name)
        self.theme.pop(section)
        check_theme = config.make_empty_theme()
        check_theme.update(self.theme)
        self.assertEqual(theme.items(), check_theme.items())


class UpdateParametersTypeTestCase(unittest.TestCase):
    """Test Case for updating parameters with subtheme."""

    def setUp(self):
        """Prepartion for the test case."""
        self.tempdir = TemporaryDirectory()
        config.THEMES_PATH = self.tempdir.name

        self.theme_name = 'test_theme'
        subtheme_sect = config.SECTION_NAMES_CONFIG['subthemes']
        self.theme = {
            'path': path.join(config.THEMES_PATH,
                              self.theme_name,
                              'config.yaml'),
            subtheme_sect: {
                'subtheme1': 'subtheme1.yaml'
            }
        }
        self.subtheme = {
            'path': path.join(config.THEMES_PATH,
                              self.theme_name,
                              self.theme[subtheme_sect]['subtheme1'])
        }
        makedirs(path.dirname(self.theme['path']), exist_ok=True)
        self.maxDiff = None

    def tearDown(self):
        """Clean the system after tests."""
        self.tempdir.cleanup()

    def test_update_str_param(self):
        """Test udating strings."""
        section = config.SECTION_NAMES_CONFIG['root_file']
        self.theme[section] = 'main_root.tex'
        self.subtheme[section] = 'subtheme_root.tex'
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        with open(self.subtheme['path'], 'w') as file:
            file.write(safe_dump(self.subtheme))
        theme = load_theme('{}{}{}'.format(self.theme_name,
                                           config.THEME_NAME_SEP,
                                           'subtheme1'))
        check_theme = config.make_empty_theme()
        check_theme.update(self.subtheme)
        self.assertEqual(theme.items(), check_theme.items())

    def test_update_dict_param(self):
        """Test udating strings."""
        section = config.SECTION_NAMES_CONFIG['parameters']
        self.theme[section] = {
            'param1': 'value1',
            'param3': 'value3'
        }
        self.subtheme[section] = {
            'param1': 'value2',
            'param2': 'value3'
        }
        with open(self.theme['path'], 'w') as file:
            file.write(safe_dump(self.theme))
        with open(self.subtheme['path'], 'w') as file:
            file.write(safe_dump(self.subtheme))
        theme = load_theme('{}{}{}'.format(self.theme_name,
                                           config.THEME_NAME_SEP,
                                           'subtheme1'))
        check_theme = config.make_empty_theme()
        self.theme[section].update(self.subtheme[section])
        check_theme.update(self.subtheme)
        check_theme[section] = self.theme[section]
        self.assertEqual(theme.items(), check_theme.items())


if __name__ == '__main__':
    unittest.main(verbosity=0)
