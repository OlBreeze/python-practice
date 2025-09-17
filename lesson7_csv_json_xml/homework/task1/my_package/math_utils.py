"""
Модуль math_utils.
Містить математичні функції: факторіал та найбільший спільний дільник.
"""

import math


def factorial(n):
    """
      Обчислює факторіал заданого числа.
    """
    if n < 0:
        return "Факторіал не визначений для від'ємних чисел"
    if n == 0:
        return 1
    return n * factorial(n - 1)


# my_gcd =  math.gcd
def my_gcd(a: int, b: int) -> int:
    """
    Знаходить найбільший спільний дільник (НСД) двох чисел.
    """
    return math.gcd(a, b)
