
from unicodedata import east_asian_width
from japanese import Vt
from dictionary import sdict


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
        >>> words_ = ['eat', 'たべる', 'たべない']
        >>> UFormat.format_uwords(words_, 10)
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


def print_verb_conjugation_table(max_n=9999):
    width = 15
    headings = (
        'Meaning', 'Masu', 'Te', 'Pres. Pos', 'Pres. Neg.', 'Past Pos.', 'Past Neg.')
    underlines = ('-' * len(h) for h in headings)

    print(UFormat.format_uwords(headings, width))
    print(UFormat.format_uwords(underlines, width))

    for i, v in enumerate(sdict.eng_verb_dict.values()):
        if i >= max_n:
            break
        conjugations = [
            v.conjugate(t, pn)
            for t in (Vt.PRESENT, Vt.PAST)
            for pn in (Vt.AFFIRM, Vt.NEG)]
        print(UFormat.format_uwords((v.meaning, v.masu, v.te, *conjugations), width))


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=False)

    print_verb_conjugation_table()
