"""Testing `show version` command."""

import unittest
from latextm.latextm import (make_version_string,
                             create_argparser,
                             VERSION)
from latextm.config import VERSION_STRING_TEMPLATE


class ShowVersionTestCase(unittest.TestCase):
    """Test Case for `show_version` action."""

    def setUp(self):
        """Prepare the test."""
        arg_parser = create_argparser()
        self.args = arg_parser.parse_args('--version'.split())

    def test_show_version(self):
        """Test show version."""
        self.assertEqual(make_version_string(self.args.version),
                         VERSION_STRING_TEMPLATE.format(version=VERSION))


if __name__ == '__main__':
    unittest.main(verbosity=0)
