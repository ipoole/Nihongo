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


def times_quiz(num_questions=10, repeats=2, delay=4):
    for i in range(1, num_questions + 1):
        hrs = random.randint(0, 12)
        mins = random.choice(['05', 15, 15, 30, 30, 30, 45, 45, 55, 40, 20, 10])
        am_or_pm = random.choice(['am', 'pm'])
        say_jap_wait(f'{str(i)} ばん', 1)
        time_eng = f"{hrs}:{mins} {am_or_pm}"
        for _ in range(repeats):
            say_jap_wait(time_eng, delay)   # Japanese speech cleverly interprets English times!
        print(i, ':', time_eng)
        say_eng_wait(f'That was {time_eng}', 1)
        say_jap_wait(time_eng, 2)
    say_jap_wait('おわりました')


if __name__ == "__main__":
    numbers_quiz(num_questions=5, repeats=2, delay=4)
    say_jap_wait('なんじですか', 2)
    times_quiz(num_questions=5, repeats=2, delay=5)
