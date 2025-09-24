from typing import Union, Optional


def parse_input(value: Union[int, str]) -> Optional[int]:
    """
    Приймає значення типу int або str та повертає його у вигляді цілого числа.
    Якщо значення вже є цілим числом — повертає його без змін.
    Якщо конвертація неможлива (наприклад, рядок не є числом) — повертає None.

    Args:
        value (Union[int, str]): Вхідне значення, яке може бути або int, або str.

    Returns:
        Optional[int]: Ціле число або None, якщо конвертація не вдалася.
    """
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except ValueError:
        return None

# Check in homework.py
# print(parse_input(42))
# print(parse_input("100"))
# print(parse_input("hello"))
