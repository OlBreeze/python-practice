"""
Модуль string_utils.
Містить функції для роботи з рядками: обрізання пробілів та приведення до верхнього регістру.
"""


def upper_case_string(string: str) -> str:
    """
    Перетворює рядок у верхній регістр.
    """
    return string.upper()


def trip_whitespace(string: str) -> str:
    """
    Видаляє зайві пробіли на початку і в кінці рядка.
    """
    return string.strip()
