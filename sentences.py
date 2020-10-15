# coding: utf-8

from japanese import Vt, sdict

# Here is a comment I added

def basic_sen(subject=None, noun=None, verb=None, with_=None, *args):
	"""
	>>> print(basic_sen(None, 'beer', 'drink', None, Vt.PAST, Vt.POLITE))
	('ビール を のみました', 'drinked the beer ')
	>>> print(basic_sen('he', 'sushi', 'eat', 'Tanaka-san', Vt.PLAIN))
	('かれ は たなかさん と すし を たべる', 'he eat the sushi with Tanaka-san')
	"""

	jap = ''
	if subject: jap += sdict.pronoun(subject).jap + ' は '
	if with_: jap += sdict.pronoun(with_).jap + ' と '
	if noun: jap += sdict.noun(noun).jap + ' を '
	if verb: jap += sdict.verb(verb).conjugate(*args)

	eng = ''
	if subject: eng += subject + ' '
	if verb: eng += sdict.verb(verb).conjugate(Vt.ENG, *args) + ' '
	if noun: eng += 'the ' + sdict.noun(noun).eng + ' '
	if with_: eng += 'with ' + sdict.pronoun(with_).eng
	return jap, eng

def basic_sen_examples():
	print(basic_sen('she', 'phone', 'use', None, Vt.PAST))
	print(basic_sen('I', 'sushi', 'eat', None, Vt.PAST, Vt.PLAIN))
	print(basic_sen('I', 'beer', 'drink', 'Tanaka-san', Vt.PAST, Vt.POLITE))
	print(basic_sen('he', 'dog', 'lend', None))
	print(basic_sen('she', 'class', 'finish', None, Vt.PAST))
	print(basic_sen('I', 'bread', 'forget', None, Vt.PAST))

def polite_request_sen(verb, noun=None):
	jap = ''
	if noun: jap += sdict.noun(noun).jap + ' を '
	jap += sdict.verb(verb).conjugate(Vt.TE) + ' '
	jap += 'ください'

	eng = 'Please ' + sdict.verb(verb).eng
	if noun: eng += ' the ' + sdict.noun(noun).eng

	return jap, eng

def polite_request_sen_examples():
	print(polite_request_sen('eat'))
	print(polite_request_sen('watch', 'film'))
	print(polite_request_sen('turn off', 'light'))
	print(polite_request_sen('turn on', 'TV'))
	print(polite_request_sen('wait'))




if __name__ == '__main__':
	import doctest

	doctest.testmod()

	basic_sen_examples()
	print()
	polite_request_sen_examples()


