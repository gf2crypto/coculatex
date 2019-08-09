"""Testing parser of arguments."""

import unittest
from latextm.latextm import create_argparser
from latextm.config import THEMES_DIRECTORY


class ArgumentParserTestCase(unittest.TestCase):
    """Test Case for function which parsed the command line arguments."""

    def setUp(self):
        """Prepare the tests."""
        self.parser = create_argparser()

    def test_parse_version(self):
        """Test parse version argument."""
        parser_list = ['--version']
        arguments = self.parser.parse_args(parser_list)
        self.assertTrue(arguments.version)
        parser_list = ['list']
        arguments = self.parser.parse_args(parser_list)
        self.assertFalse(arguments.version)

    def test_parse_verbosity(self):
        """Test parse verbosity argument."""
        parser_list = ['--verbose']
        arguments = self.parser.parse_args(parser_list)
        self.assertEqual(arguments.verbose, 1)
        parser_list = ['-vvv']
        arguments = self.parser.parse_args(parser_list)
        self.assertEqual(arguments.verbose, 3)

    def test_parse_theme_path(self):
        """Test parse theme-path argument."""
        parser_str = '--themes-path ~/my_themes list'
        arguments = self.parser.parse_args(parser_str.split())
        self.assertEqual(arguments.themes_path, '~/my_themes')
        parser_str = '-t ~/my_themes list'
        arguments = self.parser.parse_args(parser_str.split())
        self.assertEqual(arguments.themes_path, '~/my_themes')
        parser_str = 'list'
        arguments = self.parser.parse_args(parser_str.split())
        self.assertEqual(arguments.themes_path, THEMES_DIRECTORY)


if __name__ == '__main__':
    unittest.main(verbosity=0)
