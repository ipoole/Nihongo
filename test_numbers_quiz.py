import unittest
import numbers_quiz


class TestNumbersQuiz(unittest.TestCase):
    def test_numbers_quiz(self):
        numbers_quiz.numbers_quiz(num_questions=2, repeats=1, delay=1)


if __name__ == '__main__':
    unittest.main()
