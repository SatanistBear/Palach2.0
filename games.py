import random


def casino(money):
    res = random.randint(0, 1000) / 10
    if 0 < res < 0.11:
        return money * 20
    elif 0.11 < res < 40:
        return money
    elif 40 < res < 100:
        return -money
