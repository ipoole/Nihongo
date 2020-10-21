# coding: utf-8

from time import sleep
import random
from japanese import Vt, sdict

try:
	# noinspection PyUnresolvedReferences
	from speech import is_speaking, say
except ModuleNotFoundError:
	print("Speech not available")


	def is_speaking():
		return False

	# noinspection PyUnusedLocal
	def say(text, lang='en-GB', speed=0.5):
		# print("Say:", text[:7], "...")
		pass

	def sleep(_):
		pass


# Here is a comment I added


def finish_speaking():
	# Block until speech synthesis has finished
	while is_speaking():
		sleep(0.1)


def say_jap_wait(jap, t=0):
	say(jap, 'ja-JP', 0.4)
	while is_speaking():
		sleep(0.2)
	sleep(t)


def say_eng_wait(eng, t=0):
	say(eng, 'en-GB')
	while is_speaking():
		sleep(0.15)
	sleep(t)


def print_and_say(jap_eng):
	jap, eng = jap_eng
	print(jap)
	print(eng)
	say(jap, 'ja-JP')
	finish_speaking()
	sleep(1)
	print()


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
	print_and_say(basic_sen('she', 'phone', 'use', None, Vt.PAST))
	print_and_say(basic_sen('I', 'sushi', 'eat', None, Vt.PAST, Vt.PLAIN))
	print_and_say(basic_sen('I', 'beer', 'drink', 'Tanaka-san', Vt.PAST, Vt.POLITE))
	print_and_say(basic_sen('he', 'dog', 'lend', None))
	print_and_say(basic_sen('she', 'class', 'finish', None, Vt.PAST))
	print_and_say(basic_sen('I', 'bread', 'forget', None, Vt.PAST, Vt.NEG))


def polite_request_sen(verb, noun=None):
	jap = ''
	if noun: jap += sdict.noun(noun).jap + ' を '
	jap += sdict.verb(verb).conjugate(Vt.TE) + ' '
	jap += 'ください'

	eng = 'Please ' + sdict.verb(verb).eng
	if noun: eng += ' the ' + sdict.noun(noun).eng

	return jap, eng


def polite_request_sen_examples():
	print_and_say(polite_request_sen('eat'))
	print_and_say(polite_request_sen('watch', 'film'))
	print_and_say(polite_request_sen('turn off', 'light'))
	print_and_say(polite_request_sen('turn on', 'TV'))
	print_and_say(polite_request_sen('wait'))


def say_numbers():
	for i in range(1, 11):
		logn = random.uniform(1.8, 4.5)
		n = int(10 ** logn)
		say_jap_wait(f'{str(i)} ばん', 2)
		for _ in range(2):
			say_jap_wait(str(n), 5)

		say_eng_wait(f'That was {str(n)}.', 1)
		print(i, ':', n)
		say_jap_wait(str(n), 3)
	say_jap_wait('おわりました')


if __name__ == '__main__':
	import doctest

	doctest.testmod()

	# basic_sen_examples()
	print()
	# polite_request_sen_examples()

	say_numbers()
