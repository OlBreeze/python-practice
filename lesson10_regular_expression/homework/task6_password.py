# Завдання 6. Перевірка валідності пароля
# Напишіть функцію, яка перевіряє, чи є пароль надійним. Пароль надійним:
#
# містить як мінімум 8 символів,
# містить принаймні одну цифру,
# має хоча б одну велику літеру та одну малу,
# містить хоча б один спеціальний символ (@, #, $, %, &, тощо).


# import string  # string.punctuation
import re


def is_strong_password(password: str) -> bool:
    """
    Перевіряє, чи є пароль надійним.

    Args:
        password (str): Пароль для перевірки.

    Returns:
        bool: True, якщо пароль відповідає вимогам, False інакше.

    Приклади:
        >>> is_strong_password("Weak123")
        False
        >>> is_strong_password("StrongPass1!")
        True
    """

    # special_chars = "@#$%&!?*-_"
    special_chars = "!@#$%^&*(),.?:{}|<>"

    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    # 1v
    if not re.search(fr'[{special_chars}]', password):
        return False

    # 2v
    # if not any(char in string.punctuation for char in password):
    #     return False

    # 3v
    # if not any(char in special_chars for char in password):
    #     return False

    return True


print(is_strong_password("Pass123"))  # False замало символів
print(is_strong_password("password123"))  # False немає спецсимволу
print(is_strong_password("Password123"))  # False немає спецсимволу
print(is_strong_password("Password@123"))  # True
print(is_strong_password("12345678!"))  # False немає літер
