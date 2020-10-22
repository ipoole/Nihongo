import random
from say import say_jap_wait, say_eng_wait


def numbers_quiz(num_questions=10, repeats=2, delay=4):
    for i in range(1, num_questions + 1):
        logn = random.uniform(1.8, 4.5)
        n = int(10 ** logn)
        say_jap_wait(f'{str(i)} ばん', 1)
        for _ in range(repeats):
            say_jap_wait(str(n), delay)

        print(i, ':', n)
        say_eng_wait(f'That was {str(n)}.', 1)
        say_jap_wait(str(n), 1)
    say_jap_wait('おわりました')


if __name__ == "__main__":
    numbers_quiz(num_questions=5, repeats=2, delay=4)
