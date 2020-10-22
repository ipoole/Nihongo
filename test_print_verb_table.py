import unittest

from print_verb_table import print_verb_conjugation_table


class TestPrintVerbTable(unittest.TestCase):
    def test_print_verb_conjugation_table(self):
        print_verb_conjugation_table(3)


if __name__ == '__main__':
    unittest.main()
