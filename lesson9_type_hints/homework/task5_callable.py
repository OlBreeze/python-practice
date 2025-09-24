# Завдання 5: Використання Callable

# Реалізуйте функцію apply_operation, яка приймає:
# число x: int
# функцію operation: Callable[[int], int]
# повертає результат застосування функції до x.
# Створіть дві функції square (повертає квадрат числа) та double (подвоює число). Перевірте їх роботу з apply_operation.
from typing import Callable


def apply_operation(x: int, operation: Callable[[int], int]) -> int:
    """
    Застосовує передану функцію до числа x.

    Args:
        x (int): Число, до якого потрібно застосувати операцію.
        operation (Callable[[int], int]): Функція, яка приймає int і повертає int.

    Returns:
        int: Результат застосування функції до числа x.
    """
    return operation(x)


def square(n: int) -> int:
    """
    Повертає квадрат числа.

    Args:
        n (int): Вхідне число.

    Returns:
        int: Квадрат числа n.
    """
    return n * n


def double(n: int) -> int:
    """
    Повертає подвоєне число.

    Args:
        n (int): Вхідне число.

    Returns:
        int: Подвоєне значення числа n.
    """
    return n * 2

# Check in homework.py
# print(apply_operation(5, square))
# print(apply_operation(5, double))
