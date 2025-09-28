import re

# Припускаємо, що string був визначений раніше, наприклад:
string = "test1 test2 test3 test4 test5"
# print(result) # Рядок 12 залежить від попереднього, невидимого коду

# Шаблон не збігається, оскільки string не дорівнює "test1 test2 test3 test4 test5" (без лапок)
result = re.fullmatch(pattern=r"test1 test2 test3 test4 test5", string=string)
# None
print(result)

# Шаблон шукає 1-5 символів слова, за якими слідує 1 пробіл.
# Не збігається з усім рядком.
result = re.fullmatch(pattern=r"\w+\s{1,5}", string=string)
print(result)

# Шаблон, ймовірно, має відповідати структурі "слово + пробіл" 5 разів.
# r"\w+\s\w+\s\w+\s\w+\s\w+"
result = re.fullmatch(pattern=r"\w+\s\w+\s\w+\s\w+\s\w+", string=string)
print(result)

# Перевірка формату "img" + цифри
print(re.fullmatch(pattern=r'[a-z]+\d+', string='img 20221208')) # None, через пробіл
print(re.fullmatch(pattern=r'[a-z]+-+\d+', string='img-20230111'))