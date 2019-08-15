"""Test for applying the theme."""
import unittest
from tempfile import TemporaryDirectory
from os import (makedirs,
                path)
from yaml import (safe_load,
                  safe_dump)
import coculatex.config as config
from coculatex.apply_action import handler


class ApplyThemeNotEmbedTestCase(unittest.TestCase):
    """Test Case for applying the yaml separate configuration."""

    def setUp(self):
        """Prepartion for the test case."""
        self.theme_dir = TemporaryDirectory()
        self.out_dir = TemporaryDirectory()
        config.THEMES_PATH = self.theme_dir.name

        self.themes_config = {
            'sayhello': (
                'path: {path}\n'
                '{parameters}:\n'
                '    name: Noname\n'
                '    lang: english\n'
                '{description}: just say hello to someone\n'
                '{root_file}: sources/sayhello.tex\n'
                '{tex}:\n'
                '    options: [ \'-shell-escape\' ]\n'
                '    program: pdflatex\n'
                '    encoding: utf8\n'
                '{include_files}:\n'
                '    sayhello.sty: sources/sty/sayhello.sty\n'
                '{readme}: readme.txt\n'
                '{example}: example\n'
                ''.format(**config.SECTION_NAMES_CONFIG,
                          path=path.join(self.theme_dir.name, 'alpha',
                                         'config.yaml'))
            )
        }
        self.theme_files = {
            'sayhello/sources/base/basehello.tex': (
                r'\documentclass[twoside]{article}''\n'
                r'\usepackage[\BLOCK{block lang}'
                r'\BLOCK{endblock lang}]{babel}''\n'
                r'\usepackage[utf8]{inputenc}''\n'
                r'\usepackage{sayhello}''\n\n'
                r'%===========USER DEFINED PREAMBULES=============''\n'
                r'\VAR{tex_preambule}''\n\n'
                r'\begin{document}''\n'
                r'\sayhello{\VAR{name}}{\VAR{lang}}''\n'
                r'\VAR{tex_main}''\n'
                r'\end{document}''\n'
            ),
            'sayhello/sources/sayhello.tex': (
                r'%% extends "base/basehello.tex"''\n'
                r'\BLOCK{block lang}\VAR{lang}\BLOCK{endblock lang}''\n'
                ),
            'sayhello/sources/sty/sayhello.sty': (
                r'\newcommand{\sayhello}[2]{''\n'
                r'    \textbf{Hello, #1!}''\n\n'
                r'    \textit{How are you?! I hope You are fine!}''\n\n'
                r'    Do you speak #2''\n'
                r'}'
                )
        }
        self.user_parameters = safe_load(
            '{theme}: sayhello\n'
            '{project_name}: saymyname\n'
            'name: Ivan Chizhov\n'
            'lang: english\n'
            '{tex_options}:\n'
            '    program: xelatex\n'
            '    myoption: myvalue\n'
            '{tex_preambule}: |''\n'
            '  \\usepackage{{amsthm}}''\n'
            '{tex_sources}:\n'
            '    - hello.source.tex\n'
            ''.format(**config.PARAMETERS_NAMES_CONFIG)
            )
        self.make_diretory_tree()
        self.maxDiff = None

    def make_diretory_tree(self):
        """Make the directories tree."""
        for name, value in self.themes_config.items():
            makedirs(path.join(self.theme_dir.name, name), exist_ok=True)
            with open(path.join(self.theme_dir.name,
                                name, 'config.yaml'), 'w') as file:
                file.write(value)

        for name, value in self.theme_files.items():
            makedirs(path.dirname(path.join(self.theme_dir.name,
                                            path.normpath(name))),
                     exist_ok=True)
            with open(path.join(self.theme_dir.name,
                                path.normpath(name)), 'w') as file:
                file.write(value)

    def tearDown(self):
        """Clean the system after tests."""
        self.theme_dir.cleanup()
        self.out_dir.cleanup()

    def test_full_yaml_config(self):
        """Test apply with full yaml configuration."""
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'saymyname.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'hello.source.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'sayhello.sty')))

        saymyname_tex = (
            '%!TEX options=-shell-escape\n'
            '%!TEX program=xelatex\n'
            '%!TEX encoding=utf8\n'
            '%!TEX myoption=myvalue\n'
            '\\documentclass[twoside]{article}\n'
            '\\usepackage[english]{babel}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{sayhello}\n'
            '\n'
            '%===========USER DEFINED PREAMBULES=============\n'
            '\\usepackage{amsthm}\n\n\n'
            '\\begin{document}\n'
            '\\sayhello{Ivan Chizhov}{english}\n'
            '\\include{hello.source.tex}\n'
            '\n'
            '\\end{document}'
            )
        with open(path.join(self.out_dir.name, 'saymyname.tex'), 'r') as file:
            self.assertEqual(saymyname_tex, file.read())
        with open(path.join(self.out_dir.name,
                            'hello.source.tex'), 'r') as file:
            self.assertEqual(file.read(), '%!TEX root=saymyname.tex\n')
        with open(path.join(self.out_dir.name, 'sayhello.sty'), 'r') as file:
            self.assertEqual(file.read(),
                             self.theme_files[
                                 'sayhello/sources/sty/sayhello.sty'])

    def test_theme_is_not_specified(self):
        """Test apply theme if theme's name is not specified."""
        self.user_parameters.pop('theme')
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'saymyname.tex')))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'hello.source.tex')))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'sayhello.sty')))

    def test_project_name_is_not_specified(self):
        """Test apply theme if the project name is not specified."""
        self.user_parameters.pop('project-name')
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'saymyname.tex')))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'hello.source.tex')))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'sayhello.sty')))

    def test_tex_options_is_not_specified(self):
        """Test applying theme if tex options is not specified."""
        self.user_parameters.pop('tex-options')
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'saymyname.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'hello.source.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'sayhello.sty')))

        saymyname_tex = (
            '%!TEX options=-shell-escape\n'
            '%!TEX program=pdflatex\n'
            '%!TEX encoding=utf8\n'
            '\\documentclass[twoside]{article}\n'
            '\\usepackage[english]{babel}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{sayhello}\n'
            '\n'
            '%===========USER DEFINED PREAMBULES=============\n'
            '\\usepackage{amsthm}\n\n'
            '\n'
            '\\begin{document}\n'
            '\\sayhello{Ivan Chizhov}{english}\n'
            '\\include{hello.source.tex}\n'
            '\n'
            '\\end{document}'
            )
        with open(path.join(self.out_dir.name, 'saymyname.tex'), 'r') as file:
            self.assertEqual(saymyname_tex, file.read())
        with open(path.join(self.out_dir.name,
                            'hello.source.tex'), 'r') as file:
            self.assertEqual(file.read(), '%!TEX root=saymyname.tex\n')
        with open(path.join(self.out_dir.name, 'sayhello.sty'), 'r') as file:
            self.assertEqual(file.read(),
                             self.theme_files[
                                 'sayhello/sources/sty/sayhello.sty'])

    def test_tex_preambule_is_not_specified(self):
        """Test applying theme if preambule is not specified."""
        self.user_parameters.pop('tex_preambule')
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'saymyname.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'hello.source.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'sayhello.sty')))

        saymyname_tex = (
            '%!TEX options=-shell-escape\n'
            '%!TEX program=xelatex\n'
            '%!TEX encoding=utf8\n'
            '%!TEX myoption=myvalue\n'
            '\\documentclass[twoside]{article}\n'
            '\\usepackage[english]{babel}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{sayhello}\n'
            '\n'
            '%===========USER DEFINED PREAMBULES=============\n'
            '\n\n'
            '\\begin{document}\n'
            '\\sayhello{Ivan Chizhov}{english}\n'
            '\\include{hello.source.tex}\n'
            '\n'
            '\\end{document}'
            )
        with open(path.join(self.out_dir.name, 'saymyname.tex'), 'r') as file:
            self.assertEqual(saymyname_tex, file.read())
        with open(path.join(self.out_dir.name,
                            'hello.source.tex'), 'r') as file:
            self.assertEqual(file.read(), '%!TEX root=saymyname.tex\n')
        with open(path.join(self.out_dir.name, 'sayhello.sty'), 'r') as file:
            self.assertEqual(file.read(),
                             self.theme_files[
                                 'sayhello/sources/sty/sayhello.sty'])

    def test_tex_sources_is_not_specified(self):
        """Test applying theme if tex options is not specified."""
        self.user_parameters.pop('tex_sources')
        with open(
                path.join(self.out_dir.name,
                          'saymyname.yaml'), 'w') as file:
            file.write(safe_dump(self.user_parameters))
        handler(config_file=path.join(self.out_dir.name, 'saymyname.yaml'))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'saymyname.tex')))
        self.assertFalse(path.exists(path.join(self.out_dir.name,
                                               'hello.source.tex')))
        self.assertTrue(path.exists(path.join(self.out_dir.name,
                                              'sayhello.sty')))
        saymyname_tex = (
            '%!TEX options=-shell-escape\n'
            '%!TEX program=xelatex\n'
            '%!TEX encoding=utf8\n'
            '%!TEX myoption=myvalue\n'
            '\\documentclass[twoside]{article}\n'
            '\\usepackage[english]{babel}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{sayhello}\n'
            '\n'
            '%===========USER DEFINED PREAMBULES=============\n'
            '\\usepackage{amsthm}\n\n'
            '\n'
            '\\begin{document}\n'
            '\\sayhello{Ivan Chizhov}{english}\n'
            '\n'
            '\\end{document}'
            )
        with open(path.join(self.out_dir.name, 'saymyname.tex'), 'r') as file:
            self.assertEqual(saymyname_tex, file.read())
        with open(path.join(self.out_dir.name, 'sayhello.sty'), 'r') as file:
            self.assertEqual(file.read(),
                             self.theme_files[
                                 'sayhello/sources/sty/sayhello.sty'])


if __name__ == '__main__':
    unittest.main(verbosity=0)
