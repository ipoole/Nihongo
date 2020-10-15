import unittest
import sentences


class TestSentences(unittest.TestCase):
    """ Tests for Japanses sentence construction """

    def test_basic_sen(self):
        sentences.basic_sen_examples()

    def test_polite_request_sen(self):
        sentences.polite_request_sen_examples()


if __name__ == '__main__':
    unittest.main()
