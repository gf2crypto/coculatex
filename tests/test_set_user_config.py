"""Testing for the setting of Jinja2 user config."""
import unittest
from latextm import config


class SetUsetConfigTestCase(unittest.TestCase):
    """Test Case for function `set_user_config`."""

    def setUp(self):
        """Prepare the test."""
        self.user_jinja2_config = {
            'block_start_string': 10,
            'block_end_string': True,
            'variable_start_string': r'\VARIABLE{',
            'variable_end_string': '}',
            'comment_start_string': r'\###{',
            'comment_end_string': '}',
            'line_statement_prefix': r'%%',
            'line_comment_prefix': r'%#',
            'trim_blocks': False,
            'autoescape': 10
        }
        self.new_config = config.Jinja2Config(**{
            'BLOCK_START_STRING': r'\BLOCK{',
            'BLOCK_END_STRING': '}',
            'VARIABLE_START_STRING': r'\VARIABLE{',
            'VARIABLE_END_STRING': '}',
            'COMMENT_START_STRING': r'\###{',
            'COMMENT_END_STRING': '}',
            'LINE_STATEMENT_PREFIX': r'%%',
            'LINE_COMMENT_PREFIX': r'%#',
            'TRIM_BLOCKS': False,
            'AUTOESCAPE': False
        })

    def test_set_user_config(self):
        """Test set user configuration."""
        new_config = config.set_user_config(
            config.JINJA2_DEFAULT_CONFIG,
            {'jinja2': self.user_jinja2_config})
        self.assertEqual(new_config, self.new_config)


if __name__ == '__main__':
    unittest.main(verbosity=0)
