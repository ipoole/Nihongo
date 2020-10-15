# coding: utf-8

import unittest
from japanese import Verb, Noun, Vt, hiragana, left_kana, left_most_kana, \
    print_verb_conjugation_table, Dictionary


class TestJapanese(unittest.TestCase):
    def test_hiragana(self):
        for line in hiragana:
            assert len(line) == 5

    def test_left_kana(self):
        assert left_kana(u'く') == u'き'
        assert left_kana(u'ね') == u'ぬ'

    def test_left_most_kana(self):
        assert left_most_kana(u'い') == u'わ'
        assert left_most_kana('す') == u'さ'
        assert left_most_kana('に') == u'な'

    def test_VerbTaberu(self):
        v = Verb(u'たべる', 'to eat')
        assert v.type is Vt.REGULAR
        assert v.plain == 'たべる'
        assert v.meaning == 'to eat'
        assert v.masu == 'たべます'
        assert v.te == 'たべて'
        assert v.nai == 'たべない'
        assert v.mashita == 'たべました'
        assert v.ta == 'たべた'
        assert v.masen == 'たべません'
        assert v.masen_deshita == 'たべません でした'
        assert v.nakata == 'たべなかった'
        assert v.mashyo == 'たべましょう'
        assert v.ou == 'たべよう'

    def test_VerbMiru(self):
        v = Verb(u'みる', 'to see')
        assert v.type is Vt.REGULAR
        assert v.plain == u'みる'
        assert v.meaning == 'to see'
        assert v.masu == u'みます'
        assert v.te == u'みて'
        assert v.nai == u'みない'
        assert v.mashita == u'みました'
        assert v.ta == u'みた'
        assert v.masen == u'みません'
        assert v.masen_deshita == u'みません でした'
        assert v.nakata == u'みなかった'
        assert v.mashyo == u'みましょう'
        assert v.ou == u'みよう'

    def test_VerbAru(self):
        v = Verb(u'あるく', 'to walk')
        assert v.type is Vt.VARIABLE
        assert v.plain == u'あるく'
        assert v.meaning == 'to walk'
        assert v.masu == u'あるきます'
        assert v.te == u'あるいて'
        assert v.mashita == u'あるきました'
        assert v.nai == u'あるかない'
        assert v.ta == u'あるいた'
        assert v.masen == u'あるきません'
        assert v.masen_deshita == u'あるきません でした'
        assert v.nakata == u'あるかなかった'
        assert v.mashyo == u'あるきましょう'
        assert v.ou == u'あるこう'

    def test_VerbTsukau(self):
        v = Verb(u'つかう', 'to use')
        assert v.type is Vt.VARIABLE
        assert v.plain == u'つかう'
        assert v.meaning == 'to use'
        assert v.masu == u'つかいます'
        assert v.te == u'つかって'
        assert v.mashita == u'つかいました'
        assert v.nai == u'つかわない'
        assert v.ta == u'つかった'
        assert v.masen == u'つかいません'
        assert v.masen_deshita == u'つかいません でした'
        assert v.nakata == u'つかわなかった'
        assert v.mashyo == u'つかいましょう'
        assert v.ou == u'つかおう'

    def test_VerbKuru(self):
        v = Verb(u'くる', 'to come')
        assert v.type is Vt.IREGULAR
        assert v.plain == u'くる'
        assert v.meaning == 'to come'
        assert v.masu == u'きます'
        assert v.te == u'きて'
        assert v.nai == u'こない'
        assert v.mashita == u'きました'
        assert v.masen == u'きません'
        assert v.masen_deshita == u'きません でした'
        assert v.nakata == u'こなかった'
        assert v.mashyo == u'きましょう'
        assert v.ou == u'こよう'

    def test_VerbOkuru(self):
        v = Verb(u'おくる', 'to send', vtype=Vt.VARIABLE)
        assert v.type is Vt.VARIABLE
        assert v.masu == u'おくります'
        assert v.te == u'おくって'
        assert v.nai == u'おくらない'
        assert v.mashita == u'おくりました'
        assert v.ta == u'おくった'
        assert v.masen == u'おくりません'
        assert v.masen_deshita == u'おくりません でした'
        assert v.nakata == u'おくらなかった'
        assert v.mashyo == u'おくりましょう'
        assert v.ou == u'おくろう'

    def test_VerbIku(self):
        v = Verb(u'いく', 'to go', vtype=Vt.VARIABLE)
        assert v.type is Vt.VARIABLE
        assert v.masu == u'いきます'
        assert v.te == u'いって'  # exception to the variable verb rule
        assert v.nai == u'いかない'
        assert v.mashita == u'いきました'
        assert v.ta == u'いった'
        assert v.masen == u'いきません'
        assert v.masen_deshita == u'いきません でした'
        assert v.nakata == u'いかなかった'
        assert v.mashyo == u'いきましょう'
        assert v.ou == u'いこう'

    def test_VerbNomu(self):
        v = Verb(u'のむ', 'to drink')
        assert v.type is Vt.VARIABLE
        assert v.masu == u'のみます'
        assert v.te == u'のんで'  # exception to the variable verb rule
        assert v.nai == u'のまない'
        assert v.mashita == u'のみました'
        assert v.ta == u'のんだ'
        assert v.masen == u'のみません'
        assert v.masen_deshita == u'のみません でした'
        assert v.nakata == u'のまなかった'
        assert v.mashyo == u'のみましょう'
        assert v.ou == u'のもう'

    def test_Verb_kasui(self):
        with self.assertRaises(AssertionError):
            Verb('かすい', 'lend')

    def test_conjugate(self):
        v = Verb('ならう', 'to learn')
        assert v.conjugate() == 'ならう'
        assert v.conjugate(Vt.PAST) == 'ならった'
        assert v.conjugate(Vt.POLITE, Vt.PAST, Vt.NEG) == 'ならいません でした'
        assert v.conjugate(Vt.TE) == 'ならって'
        assert v.conjugate(Vt.VOLITIONAL) == 'ならおう'
        assert v.conjugate(Vt.VOLITIONAL, Vt.POLITE) == 'ならいましょう'

    def test_print_verb_conjugation_table(self):
        print_verb_conjugation_table()

    def test_dictionary(self):
        jdict = Dictionary()

        # nouns
        n = jdict.noun('apple')
        assert n.jap == 'りんご'
        assert n.meaning == 'apple'

        n = jdict.noun('ねこ')
        assert n.jap == 'ねこ'
        assert n.meaning == 'cat'

        assert jdict.noun('ねこ') is jdict.noun('cat')
        assert jdict.noun('cat') is not jdict.noun('dog')

        # verbs
        v = jdict.verb('eat')
        assert v.plain == 'たべる'
        assert v.meaning == 'eat'

        v = jdict.verb('のむ')
        assert v.plain == 'のむ'
        assert v.meaning == 'drink'

        assert jdict.verb('do') is jdict.verb('する')
        assert jdict.verb('eat') is not jdict.verb('drink')


if __name__ == '__main__':
    unittest.main()
