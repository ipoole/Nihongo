import unittest

from dictionary import sdict


class TestDictionary(unittest.TestCase):
    def test_verb(self):
        v1 = sdict.verb('eat')
        v2 = sdict.verb('たべる')
        v3 = sdict.verb('drink')
        assert v1 is v2
        assert v2 is not v3

    def test_noun(self):
        n1 = sdict.noun('book')
        n2 = sdict.noun('ほん')
        n3 = sdict.noun('dog')
        assert n1 is n2
        assert n2 is not n3

    def test_pronoun(self):
        p1 = sdict.pronoun('I')
        p2 = sdict.pronoun('わたし')
        p3 = sdict.pronoun('she')
        assert p1 is p2
        assert p2 is not p3


if __name__ == '__main__':
    unittest.main()
