# coding: utf-8

from enum import Enum
from unicodedata import east_asian_width

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
                for l in (Vt.AFFIRM, Vt.NEG):
                    print(p, t, l, self.conjugate(p, t, l))
        print(Vt.TE, self.conjugate(Vt.TE))
        print(Vt.VOLITIONAL, Vt.PLAIN, self.conjugate(Vt.VOLITIONAL, Vt.PLAIN))
        print(Vt.VOLITIONAL, Vt.POLITE, self.conjugate(Vt.VOLITIONAL, Vt.POLITE))
        print()


class UFormat(object):
    """ Routines to lay out text in tables, taking account of the different
    width of kana characters; With experimentation I find they occupy 5/3 ascii
    space widths """

    @staticmethod
    def sum_width(ustr):
        """ Japanese characters are 'W' and seem to have a width of 5/3 (1.666)
        that of ascii characters
        >>> UFormat.sum_width('123')
        3.0
        >>> UFormat.sum_width('あいえ')
        5.0
        """

        return sum([5 / 3 if east_asian_width(c) == 'W' else 1.0 for c in ustr])

    @staticmethod
    def format_uwords(words, width):
        """ Format given list of words in 'width' per column, taking care of non-ascii
        character widths.
        >>> words = ['eat', 'たべる', 'たべない']
        >>> UFormat.format_uwords(words, 10)
        'eat       たべる     たべない   '
        """

        actual_width_acc = 0.0
        required_width_acc = 0
        result_str = ''
        for word in words:
            result_str = result_str + word
            actual_width_acc += UFormat.sum_width(word)
            required_width_acc += width
            spaces_needed = round(required_width_acc - actual_width_acc)
            if spaces_needed > 0:
                result_str += ' ' * spaces_needed
                actual_width_acc += spaces_needed

        return result_str


class Noun(object):
    """ Japanese nouns, with english meaning.  """

    def __init__(self, jap, meaning):
        self.jap = jap
        self.meaning = meaning

    @property
    def eng(self):
        return self.meaning


class Dictionary(object):
    def __init__(self):
        verblist = Dictionary._verbs()
        self.jap_verb_dict = {v.plain: v for v in verblist}
        self.eng_verb_dict = {v.meaning: v for v in verblist}

        nounlist = Dictionary._nouns()
        self.jap_noun_dict = {n.jap: n for n in nounlist}
        self.eng_noun_dict = {n.meaning: n for n in nounlist}

        pronounlist = Dictionary._pronouns()
        self.jap_pronoun_dict = {n.jap: n for n in pronounlist}
        self.eng_pronoun_dict = {n.meaning: n for n in pronounlist}

    def verb(self, w):
        """ Find a verb given either its plain form or its english meaning """
        if w in self.jap_verb_dict.keys():
            return self.jap_verb_dict[w]
        elif w in self.eng_verb_dict.keys():
            return self.eng_verb_dict[w]
        else:
            print('Verb', w, 'not found')
            assert False

    def noun(self, w):
        """ Find a noun given either its plain form or its english meaning """
        if w in self.jap_noun_dict.keys():
            return self.jap_noun_dict[w]
        elif w in self.eng_noun_dict.keys():
            return self.eng_noun_dict[w]
        else:
            print('Noun', w, 'not found')
            assert False

    def pronoun(self, w):
        """ Find a pronoun given either its either japanese english meaning """
        if w is None:
            return None
        elif w in self.jap_pronoun_dict.keys():
            return self.jap_pronoun_dict[w]
        elif w in self.eng_pronoun_dict.keys():
            return self.eng_pronoun_dict[w]
        else:
            print('Pronoun', w, 'not found')
            assert False

    @staticmethod
    def _verbs():
        result = [
            # Variable verbs
            Verb('あう', 'meet', Vt.VARIABLE),
            Verb('あずかる', 'look after', Vt.VARIABLE),
            Verb('ある', 'exist', Vt.VARIABLE),
            Verb('あるく', 'walk', Vt.VARIABLE),
            Verb('いう', 'say', Vt.VARIABLE),
            Verb('いく', 'go', Vt.VARIABLE),
            Verb('いただく', 'accept', Vt.VARIABLE),
            Verb('うる', 'sell', Vt.VARIABLE),
            Verb('おく', 'put', Vt.VARIABLE),
            Verb('おくる', 'send', Vt.VARIABLE),
            Verb('おす', 'push', Vt.VARIABLE),
            Verb('おわる', 'finish', Vt.VARIABLE),
            Verb('かう', 'buy', Vt.VARIABLE),
            Verb('かえる', 'return', Vt.VARIABLE),
            Verb('かく', 'write', Vt.VARIABLE),
            Verb('かす', 'lend', Vt.VARIABLE),
            Verb('かつぐ', 'carry', Vt.VARIABLE),
            Verb('がんばる', "do one's best", Vt.VARIABLE),
            Verb('きく', 'listen', Vt.VARIABLE),
            Verb('けす', 'turn off', Vt.VARIABLE),
            Verb('こむ', 'be crowded', Vt.VARIABLE),
            Verb('しる', 'know', Vt.VARIABLE),
            Verb('すう', 'smoke', Vt.VARIABLE),
            Verb('すむ', 'live', Vt.VARIABLE),
            Verb('たつ', 'stand up', Vt.VARIABLE),
            Verb('ちがう', 'be wrong', Vt.VARIABLE),
            Verb('つかう', 'use', Vt.VARIABLE),
            Verb('つく', 'arrive', Vt.VARIABLE),
            Verb('つくる', 'make', Vt.VARIABLE),
            Verb('とる', 'take', Vt.VARIABLE),
            Verb('ならる', 'learn', Vt.VARIABLE),
            Verb('にあう', 'look good on', Vt.VARIABLE),
            Verb('のむ', 'drink', Vt.VARIABLE),
            Verb('のる', 'get on', Vt.VARIABLE),
            Verb('はいる', 'enter', Vt.VARIABLE),
            Verb('まがる', 'turn', Vt.VARIABLE),
            Verb('まつ', 'wait', Vt.VARIABLE),
            Verb('もつ', 'hold', Vt.VARIABLE),
            Verb('もらう', 'receive', Vt.VARIABLE),
            Verb('よぶ', 'call', Vt.VARIABLE),
            Verb('よむ', 'read', Vt.VARIABLE),
            Verb('わかる', 'understand', Vt.VARIABLE),

            # Plain verbs
            Verb('あける', 'open'),
            Verb('あげる', 'give'),
            Verb('いる', 'be'),
            Verb('いれる', 'put in'),
            Verb('おしえる', 'tell'),
            Verb('おりる', 'get off'),
            Verb('わすれる', 'forget'),
            Verb('しめる', 'close'),
            Verb('たべる', 'eat'),
            Verb('つける', 'turn on'),
            Verb('けす', 'turn off'),
            Verb('つける', 'be careful'),
            Verb('つとめる', 'work for'),
            Verb('でる', 'leave'),
            Verb('とどける', 'deliver'),
            Verb('とめる', 'park'),
            Verb('みせる', 'show'),
            Verb('みる', 'see'),
            Verb('みる', 'look'),
            Verb('みる', 'watch'),

            # Irregular verbs
            Verb('する', 'do')
        ]
        return result

    @staticmethod
    def _nouns():
        result = [
            Noun('ほん', 'book'),
            Noun('じてんしゃ', 'bicycle'),
            Noun('すし', 'sushi'),
            Noun('ひこうき', 'airplane'),
            Noun('でうぶつ', 'animal'),
            Noun('いぬ', 'dog'),
            Noun('りんご', 'apple'),
            Noun('せなか', 'back'),
            Noun('かばん', 'bag'),
            Noun('ぎんこう', 'bank'),
            Noun('バー', 'bar'),
            Noun('ベッド', 'bed'),
            Noun('ぎゅうにく', 'beef'),
            Noun('ビール', 'beer'),
            Noun('たんじょうび', 'birthday'),
            Noun('くろ', 'black'),
            Noun('あお', 'blue'),
            Noun('ほんだな', 'bookshelf'),
            Noun('はこ', 'box'),
            Noun('パン', 'bread'),
            Noun('あさごはん', 'breakfast'),
            Noun('はし', 'bridge'),
            Noun('ちゃいろ', 'brown'),
            Noun('たてもの', 'building'),
            Noun('しんかんせん', 'bullet train'),
            Noun('かいぎ', 'meeting'),
            Noun('しょくどう', 'dining room'),
            Noun('ケーキ', 'cake'),
            Noun('ねこ', 'cat'),
            Noun('いす', 'chair'),
            Noun('こども', 'child'),
            Noun('おはし', 'chopsticks'),
            Noun('えいがかん', 'cinema'),
            Noun('じゅぎょう', 'class'),
            Noun('そうじ', 'cleaning'),
            Noun('ふく', 'clothes'),
            Noun('うあぎ', 'coat'),
            Noun('コーヒー', 'coffee'),
            Noun('きっさてん', 'coffee shoo'),
            Noun('まんが', 'comic'),
            Noun('パソコン', 'computer'),
            Noun('でんとう', 'light'),
            Noun('ごはん', 'rice'),
            Noun('うし', 'cow'),
            Noun('えいが', 'film'),
            Noun('でんわ', 'phone'),
            Noun('テレビ', 'TV'),
            Noun('まど', 'window')
        ]
        return result

    @staticmethod
    def _pronouns():
        result = [
            Noun('わたし', 'I'),
            Noun('あなた', 'you'),
            Noun('かれ', 'he'),
            Noun('かのじょ', 'she'),
            Noun('わたしたち', 'we'),
            Noun('たなかさん', 'Tanaka-san')
        ]
        return result


# A statically defined dictionary for everyone to use
sdict = Dictionary()


def print_verb_conjugation_table():
    width = 15
    headings = (
        'Meaning', 'Masu', 'Te', 'Pres. Pos', 'Pres. Neg.', 'Past Pos.', 'Past Neg.')
    underlines = ('-' * len(h) for h in headings)

    print(UFormat.format_uwords(headings, width))
    print(UFormat.format_uwords(underlines, width))

    for v in sdict.eng_verb_dict.values():
        conjugations = [
            v.conjugate(t, l)
            for t in (Vt.PRESENT, Vt.PAST)
            for l in (Vt.AFFIRM, Vt.NEG)]
        print(UFormat.format_uwords((v.meaning, v.masu, v.te, *conjugations), width))


if __name__ == '__main__':
    # v = Verb(u'かく', 'to write')
    # v.print_one_verb_congugations()
    import doctest
    doctest.testmod(verbose=0)

    print_verb_conjugation_table()
