import re

# Пошук послідовностей з двох символів \w
result = re.findall(pattern=r'\w{2}', string='Qwerty Admin')
print(result)

# Вилучення 2х послідовних символів
# Шукає межу слова (\b), за якою слідує один символ слова (\w),
# за яким слідує будь-який символ (.).
result = re.findall(pattern=r'\b\w.', string='qwerty a.dmin')
print(result)