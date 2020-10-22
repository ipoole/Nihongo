# coding: utf-8

from enum import Enum


hiragana = \
    [
        u"あいうえお",
        u"かきくけこ",
        u"さしすせそ",
        u"たちつてと",
        u"なにぬねの",
        u"はへふへほ",
        u"まみむめも",
        u"や ゆ よ",
        u"らりるれろ",

        u"がぎぐげご",
        u"ざじずぜぞ",
        u"だぢづでど",
        u"ばびぶべぼ",
        u"ぱぴぷぺぽ"]


def find_kana_line(c):
    for line in hiragana:
        if c in line:
            return line
    assert False, "Character " + c + " not found"


def left_kana(c):
    """
    >>> left_kana(u'す')
    'し'
    """
    line = find_kana_line(c)
    ix = line.find(c)
    assert ix >= 1
    return line[ix - 1]


def left_most_kana(c):
    """
    >>> left_most_kana(u'く')
    'か'
    """
    line = find_kana_line(c)
    return u'わ' if line[0] == u'あ' else line[0]


def right_most_kana(c):
    """
    >>> right_most_kana(u'に')
    'の'
    """
    line = find_kana_line(c)
    return line[-1]


# noinspection SpellCheckingInspection
class Vt(Enum):
    REGULAR = 1,  # JFBP Regular 2, e.g. あべる
    VARIABLE = 2,  # JFBP Regular 1, e.g. のむ、いく
    IREGULAR = 3,  # くる、する、もって

    PRESENT = 4,
    PAST = 5,

    AFFIRM = 6,
    NEG = 7,

    POLITE = 8,
    PLAIN = 9,

    VOLITIONAL = 10,
    TE = 11,

    ENG = 12


class Verb(object):
    """ Models a single verb word, providing functionality to congigate
    and translate """

    def __init__(self, plain, meaning, vtype=None):
        """"Construct a verb conjugation object given plain form and
        english meaning.  The tyle flag is to override verb type for
        variable verbs ending in る, otherwise type is inferred """
        assert len(plain) >= 1
        self.plain = plain
        self.meaning = meaning

        if vtype is None:
            self.type = Vt.REGULAR if plain[-1] == u'る' else Vt.VARIABLE
            if plain in (u'くる', u'する', u'もってくる'):
                self.type = Vt.IREGULAR
        else:
            self.type = vtype

        if self.type is Vt.REGULAR:
            # Regular 2 verbs masu form just removes る then ads ます
            self.masu = plain[:-1] + u'ます'

            # te form just replaces u'る' with u'て' (not right!)
            self.te = plain[:-1] + u'て'

            self.nai = plain[:-1] + u'ない'

            self.ou = plain[:-1] + u'よう'

        elif self.type is Vt.VARIABLE:
            # variable verbs (Regular 1)
            # masu form moves the final char to left on the kana line then adds 'masu'
            self.masu = plain[:-1] + left_kana(plain[-1]) + u"ます"

            # te form is based on masu form, depnds on the char (c) preceding ます
            te_map = {
                u'き': u'いて', u'ぎ': u'いで', u'し': u'して',
                u'い': u'って', u'ち': u'って', u'り': u'って',
                u'に': u'んで', u'み': u'んで', u'び': u'んで'}
            c = self.masu[-3]
            if c not in te_map.keys():
                print('Te construction not known for character ' + c)
                assert False
            self.te = self.masu[:-3] + te_map[c] if plain != u'いく' else u'いって'
            # exception for いく (to go)

            self.nai = self.masu[:-3] + left_most_kana(self.masu[-3]) + u'ない'
            self.ou = self.plain[:-1] + right_most_kana(plain[-1]) + u'う'

        elif self.type is Vt.IREGULAR:
            self.masu = {u'くる': u'きます', u'する': u'します', u'もってくる': u'もってきます'}[plain]
            self.te = {u'くる': u'きて', u'する': u'して', u'もってくる': u'もってきて'}[plain]
            self.nai = {u'くる': u'こない', u'する': u'しない', u'もってくる': u'もってこない'}[plain]
            self.ou = {u'くる': u'こよう', u'する': u'しよう', u'もってくるよう': u'もってくよう'}[plain]

        # polite present negative replaces 'masu' with 'masen'
        self.masen = self.masu[:-2] + 'ません'

        # the past polite is the mashita
        self.mashita = self.masu[:-2] + 'ました'

        # past plain is the 'ta' form, obtained from the te form
        c = self.te[-1]
        assert c in u'てで'
        self.ta = self.te[:-1] + (u'た' if c == u'て' else u'だ')

        # polite negative past tense uses 'masen' + 'deshita'
        self.masen_deshita = self.masen + u' ' + u'でした'

        # plain negative past is based on the 'nai' form, replacing
        # the 'i' with 'katta'
        self.nakata = self.nai[:-1] + u'かった'

        # polite volitional
        self.mashyo = self.masu[:-2] + u'ましょう'

    @property
    def eng(self):
        return self.meaning

    def conjugate(self, *args):
        """Pass a number of Vt constants to define the conjugation.
        Defaut is plain, present, affirmative

        >>> v = Verb(u'わかる', 'to understand', Vt.VARIABLE)
        >>> v.conjugate(Vt.PAST, Vt.NEG)
        'わからなかった'
        >>> v.conjugate(Vt.POLITE, Vt.PAST, Vt.AFFIRM)
        'わかりました'
        """
        if Vt.ENG in args:
            if Vt.PAST in args:
                return self.meaning + 'ed'
            else:
                return self.meaning

        if Vt.TE in args:
            assert len(args) == 1
            return self.te

        if Vt.VOLITIONAL in args:
            if Vt.POLITE in args:
                return self.mashyo
            else:
                return self.ou

        result_table = \
            [
                [[self.plain, self.nai], [self.ta, self.nakata]],
                [[self.masu, self.masen], [self.mashita, self.masen_deshita]]
            ]
        result = result_table[Vt.POLITE in args][Vt.PAST in args][Vt.NEG in args]
        return result

    def print_one_verb_congugations(self):
        for p in (Vt.PLAIN, Vt.POLITE):
            for t in (Vt.PRESENT, Vt.PAST):
                for pn in (Vt.AFFIRM, Vt.NEG):
                    print(p, t, pn, self.conjugate(p, t, pn))
        print(Vt.TE, self.conjugate(Vt.TE))
        print(Vt.VOLITIONAL, Vt.PLAIN, self.conjugate(Vt.VOLITIONAL, Vt.PLAIN))
        print(Vt.VOLITIONAL, Vt.POLITE, self.conjugate(Vt.VOLITIONAL, Vt.POLITE))
        print()


class Noun(object):
    """ Japanese nouns, with english meaning.  """

    def __init__(self, jap, meaning):
        self.jap = jap
        self.meaning = meaning

    @property
    def eng(self):
        return self.meaning


if __name__ == '__main__':
    # v = Verb(u'かく', 'to write')
    # v.print_one_verb_congugations()
    import doctest
    doctest.testmod(verbose=False)
