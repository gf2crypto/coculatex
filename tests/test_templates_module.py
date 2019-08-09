"""Testing parser of arguments."""
from io import StringIO
import unittest
from latextm.templates import extract_variables


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

        self.jinja2_template = (
            r"%%= jinja2:""\n"
            r"%%=    block_start_string: '\BLOCK{'""\n"
            r"%%=    block_end_string: '}'""\n"
            '%%- if pagenumbering is defined\n'
            "%%-     if 'on' in pagenumbering\n"
            "%%-         set pagenum_on = pagenumbering['on']\n"
            r"%%=    variable_start_string: '\VAR{'""\n"
            r"%%=    variable_end_string: '}'""\n"
            r"%%=    comment_start_string: '\#{'""\n"
            r"%%=    comment_end_string: '}'""\n"
            "%%-     endif\n"
            "%%-     if 'position' in pagenumbering\n"
            "%%-         set pagenum_position = pagenumbering['position']\n"
            "%%-     endif\n"
            "%%-     if 'align' in pagenumbering\n"
            r"%%=    line_statement_prefix: '%%'""\n"
            r"%%=    line_comment_prefix: '%#'""\n"
            "%%-         set pagenum_align = pagenumbering['align']\n"
            "%%-     endif\n"
            "%%-     if 'firstpage' in pagenumbering\n"
            "%%-         set pagenum_firstpage = pagenumbering['firstpage']\n"
            "%%-     endif\n"
            "%%- endif\n"
            '\n'
            "%!TEX encoding=utf8\n"
            r"%!TEX options=-output-directory=\VAR{j_outdir}""\n"
            "%!TEX options=-shell-escape\n"
            "%!TEX program=xelatex\n"
            r"%!TEX jobname=\VAR{jobname}""\n"
            '\n'
            r"\documentclass[""\n"
            "    a4paper,\n"
            r"%%=    trim_blocks: true""\n"
            "    oneside,\n"
            "    onecolumn,\n"
            "    article,\n"
            r"    \VAR{font_size}""\n"
            "]{memoir}\n"
            r"%%=    autoescape: false""\n"
            )

        self.jinja2_variables = {
            'jinja2': {
                'block_start_string': '\\BLOCK{',
                'block_end_string': '}',
                'variable_start_string': '\\VAR{',
                'variable_end_string': '}',
                'comment_start_string': '\\#{',
                'comment_end_string': '}',
                'line_statement_prefix': r'%%',
                'line_comment_prefix': r'%#',
                'trim_blocks': True,
                'autoescape': False
            }
        }

        self.jinja2_cleared = (
            '%%- if pagenumbering is defined\n'
            "%%-     if 'on' in pagenumbering\n"
            "%%-         set pagenum_on = pagenumbering['on']\n"
            "%%-     endif\n"
            "%%-     if 'position' in pagenumbering\n"
            "%%-         set pagenum_position = pagenumbering['position']\n"
            "%%-     endif\n"
            "%%-     if 'align' in pagenumbering\n"
            "%%-         set pagenum_align = pagenumbering['align']\n"
            "%%-     endif\n"
            "%%-     if 'firstpage' in pagenumbering\n"
            "%%-         set pagenum_firstpage = pagenumbering['firstpage']\n"
            "%%-     endif\n"
            "%%- endif\n"
            '\n'
            "%!TEX encoding=utf8\n"
            r"%!TEX options=-output-directory=\VAR{j_outdir}""\n"
            "%!TEX options=-shell-escape\n"
            "%!TEX program=xelatex\n"
            r"%!TEX jobname=\VAR{jobname}""\n"
            '\n'
            r"\documentclass[""\n"
            "    a4paper,\n"
            "    oneside,\n"
            "    onecolumn,\n"
            "    article,\n"
            r"    \VAR{font_size}""\n"
            "]{memoir}\n"
            )

    def test_extract_variables_from_latex_template(self):
        """Test the extracting variables from latex template."""
        # print(self.latex_template)
        variables, cleared = extract_variables(StringIO(self.latex_template))
        self.assertEqual(variables.items(),
                         self.latex_variables.items())
        self.assertEqual(cleared, self.latex_cleared)

    def test_extract_variables_from_jinja2_template(self):
        """Test extracting variables from jinja2 template."""
        variables, cleared = extract_variables(StringIO(self.jinja2_template))
        self.assertEqual(variables.items(),
                         self.jinja2_variables.items())
        self.assertEqual(cleared, self.jinja2_cleared)


if __name__ == '__main__':
    unittest.main(verbosity=0)
