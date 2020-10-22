"""
Wrapper to Pythonista speech package, with no-op fall backs when on Linux
"""
from time import sleep

try:
    # noinspection PyUnresolvedReferences
    from speech import is_speaking, say
    print("Speech IS available")
    speech_available = True
except ModuleNotFoundError:
    speech_available = False
    print("Speech NOT available")

    # noinspection PyUnusedLocal
    def say(text, lang='en-GB', speed=0.5):
        # print("Saying:", text[:7], "...")
        assert lang in ['en-GB', 'ja-JP']    # There are many others but these are only ones we use
        assert 0.05 <= speed <= 1

    def is_speaking():
        return False


def finish_speaking():
    # Block until speech synthesis has finished
    while is_speaking():
        sleep(0.1)


def say_jap_wait(jap, t=0):
    say(jap, 'ja-JP', 0.4)
    while is_speaking():
        sleep(0.1)
    if speech_available:
        sleep(t)


def say_eng_wait(eng, t=0):
    say(eng, 'en-GB')
    while is_speaking():
        sleep(0.1)
    if speech_available:
        sleep(t)



