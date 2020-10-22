import unittest

import say


class TestSay(unittest.TestCase):
    def test_say(self):
        say.say("Hello in English")
        say.say("こんにちは", 'ja-JP')

    def test_is_speaking(self):
        say.say("I'm speaking")
        if say.speech_available:
            assert say.is_speaking()
        else:
            assert not say.is_speaking()

    def test_finish_speaking(self):
        say.finish_speaking()
        assert not say.is_speaking()

    def test_say_jap_wait(self):
        say.say_jap_wait("1", 0.5)
        say.say_jap_wait("2", 0)

    def test_say_eng_wait(self):
        say.say_eng_wait("1", 0.5)
        say.say_eng_wait("2", 0)


if __name__ == '__main__':
    unittest.main()
