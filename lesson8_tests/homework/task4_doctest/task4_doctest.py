# Завдання 4. Тестування з використанням doctest
#
# Додайте документацію з прикладами використання та напишіть тести з використанням doctest.
# Напишіть функції для роботи з числами:
#
# is_even(n: int) -> bool: перевіряє, чи є число парним.
# factorial(n: int) -> int: повертає факторіал числа.
# Додайте doctest-приклади для кожної функції
# python -m doctest
# python -m doctest task4_doctest.py -v

def is_even(n: int) -> bool:
    """
    Перевіряє, чи є число парним.

    Args:
        n (int): Число для перевірки

    Returns:
        bool: True, якщо число парне, False - якщо непарне

    Examples:
        >>> is_even(2)
        True
        >>> is_even(3)
        False
        >>> is_even(0)
        True
        >>> is_even(-4)
        True
        >>> is_even(-3)
        False
        >>> is_even(100)
        True
        >>> is_even(101)
        False
    """
    return n % 2 == 0


def factorial(n: int) -> int:
    """
    Обчислює факторіал числа.

    Args:
        n (int): Невід'ємне ціле число

    Returns:
        int: Факторіал числа n

    Raises:
        ValueError: Якщо n < 0

    Examples:
        >>> factorial(0)
        1
        >>> factorial(1)
        1
        >>> factorial(3)
        6
        >>> factorial(4)
        24
        >>> factorial(5)
        120
        >>> factorial(6)
        720
        >>> factorial(-1)
        Traceback (most recent call last):
            ...
        ValueError: Факторіал не визначений для від'ємних чисел
    """
    if n < 0:
        raise ValueError("Факторіал не визначений для від'ємних чисел")

    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result
