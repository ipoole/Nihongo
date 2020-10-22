from japanese import Verb, Noun, Vt


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
        """ Find a pronoun given either its japanese or english meaning """
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
