# Завдання 1. Перевірка валідності email
# Напишіть функцію, яка перевіряє, чи є email-адреса валідною.
# Email вважається валідним, якщо він має формат example@domain.com, де:
# example — послідовність з букв, цифр або точок
# (але точка не може бути на початку або в кінці).
# domain — послідовність з букв або цифр.
# .com, .net, тощо — домен верхнього рівня (TLD) довжиною від 2 до 6 символів.
import re


def is_valid_email(email: str) -> bool:
    """
    Перевіряє, чи є email-адреса валідною.

    :param email: Email-адреса для перевірки.
    :return: bool: True, якщо email валідний, False — інакше.
    """

    # pattern = r'^[a-zA-Z0-9](\.?[a-zA-Z0-9]+)*@[a-zA-Z0-9]+\.[a-zA-Z]{2,6}$'

    local = r'[a-zA-Z0-9]+(\.?[a-zA-Z0-9]+)*'
    domain = r'[a-zA-Z0-9]+\.[a-zA-Z]{2,6}'
    pattern = fr'^{local}@{domain}$'

    return bool(re.match(pattern, email))


# _____________________________________

# Валідні
print(f"test@domain.com: {is_valid_email('test@domain.com')}")
print(f"a1.b2@c3.net: {is_valid_email('a1.b2@c3.net')}")
print(f"user123@d.co: {is_valid_email('user123@d.co')}")
print(f"long.user.name@short.com: "
      f"{is_valid_email('long.user.name@short.com')}")

# Невалідні
print(f".user@domain.com: {is_valid_email('.user@domain.com')}")
print(f"user.@domain.com: {is_valid_email('user.@domain.com')}")
print(f"user@.domain.com: {is_valid_email('user@.domain.com')}")
print(f"user@domain.toolongtld: {is_valid_email('user@domain.toolongtld')}")
print(f"user@domain.c: {is_valid_email('user@domain.c')}")

#
# [...] — Клас символів:
#
# Означає: будь-який один символ із вказаних усередині.
#
# [a-z]      # одна літера від a до z
# [0-9]      # одна цифра
# [a-zA-Z0-9]# літера або цифра
# [.]        # саме крапка
#
# Важливо:
#
# [.] — це саме символ крапка, буквально.
#
# Але . без [] — означає будь-який символ.
#
# re.match(r'[abc]', 'a')  # є співпадіння
# re.match(r'[abc]', 'b')  #
# re.match(r'[abc]', 'd')  # немає співпадіння
#
# (...) — Група / capturing group:
#
# Групує частини виразу для:
#
# повторення ((...)*, (...)+)
#
# збереження значення (match.group(1))
#
# альтернатив ((abc|def))
#
# (ab)+      # група "ab", повторюється один або більше разів
# (\d{3})-   # три цифри, потім дефіс — група з 3 цифр
