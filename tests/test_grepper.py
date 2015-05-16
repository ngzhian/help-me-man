import unittest
from textwrap import dedent

from grepper import (
    capture_paragraph_from_lines,
    get_para_of_option,
    split_into_lines,
    current_argument,
)

class TestGrepper(unittest.TestCase):
    def test_split_into_lines(self):
        lines = split_into_lines(dedent('''
            lineone
            linetwo
        '''))
        self.assertEqual(['', 'lineone', 'linetwo', ''], lines)

    def test_capture_paragraph_from_lines(self):
        lines = ['', '', '--stuff', 'description', 'more', '']
        self.assertEqual(
            ['--stuff', 'description', 'more'],
            list(capture_paragraph_from_lines(lines)))

    def test_get_para_of_option(self):
        cat_man_output = '''
        NAME
               cat - concatenate files and print on the standard output

        SYNOPSIS
               cat [OPTION]... [FILE]...

        DESCRIPTION
               Concatenate FILE(s), or standard input, to standard output.

               -A, --show-all
                      equivalent to -vET

               -b, --number-nonblank
                      number nonempty output lines, overrides -n

               -e     equivalent to -vE
        '''
        para = get_para_of_option('-A', dedent(cat_man_output))
        stripped_para = map(lambda l: l.strip(), para)
        self.assertEqual(
            ['-A, --show-all', 'equivalent to -vET'],
            stripped_para)

    def test_current_argument(self):
        cases = [('man ', ''),
                ('man -c', '-c'),
                ('man -c adsf', '-c'),
                ('man --ch', '--ch'),
                ('man --ch -', '--ch'),]
        for case in cases:
            self.assertEqual(current_argument(case[0]), case[1])


if __name__ == '__main__':
    unittest.main()
