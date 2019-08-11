"""Testing parser of arguments."""
from io import StringIO
import unittest
from coculatex.templates import extract_variables


class ExtractVariablesTestCase(unittest.TestCase):
    """Test Case for function `extract_variables`."""

    def setUp(self):
        """Prepartion for the test case."""
        self.latex_template = (
            '%%= theme: letter\n'
            '%%= outdir: _builds  # output directory\n'
            '%%= jobname: advisors  # name of produced pdf file\n'
            '%%= font:\n'
            '%%=    size: 14pt\n'
            '%%=    main: Times New Roman\n'
            '%%=    sans: Arial\n'
            '%%=    mono: Courier New\n'
            '\n'
            r'\caption{''\n'
            'Выписка \textnumero 190918-1 из '
            'протокола заседания'
            'кафедры информационной\n'
            '%%= margins:\n'
            '%%=     top: 2cm\n'
            '%%=     bottom: 2cm\n'
            '%%=     left: 3cm\n'
            '%%=     right: 1.5cm\n'
            'безопасности ВМК МГУ '
            'имени М.В.~Ломоносова\n'
            '}\n'
            '\n'
            '%%= pagenumbering:\n'
            '%%=     "on": true\n'
            '%%=     position: bottom\n'
            r'\date{19 сентября 2018 года}''\n'
            '%%=     align: right\n'
            '%%=     firstpage: false\n'
            )
        self.latex_variables = {
            'theme': 'letter',
            'outdir': '_builds',
            'jobname': 'advisors',
            'font': {
                'size': '14pt',
                'main': 'Times New Roman',
                'sans': 'Arial',
                'mono': 'Courier New'
            },
            'margins': {
                'top': '2cm',
                'bottom': '2cm',
                'left': '3cm',
                'right': '1.5cm'
            },
            'pagenumbering': {
                'on': True,
                'position': 'bottom',
                'align': 'right',
                'firstpage': False
            }
        }

        self.latex_cleared = (
            '\n'
            r'\caption{''\n'
            'Выписка \textnumero 190918-1 из '
            'протокола заседания'
            'кафедры информационной\n'
            'безопасности ВМК МГУ имени '
            'М.В.~Ломоносова\n'
            '}\n'
            '\n'
            r'\date{19 сентября 2018 года}''\n'
            )

    def test_extract_variables_from_latex_template(self):
        """Test the extracting variables from latex template."""
        variables, cleared = extract_variables(StringIO(self.latex_template))
        self.assertEqual(variables.items(),
                         self.latex_variables.items())
        self.assertEqual(cleared, self.latex_cleared)


if __name__ == '__main__':
    unittest.main(verbosity=0)
