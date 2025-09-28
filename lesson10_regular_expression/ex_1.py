import re

string = "Test1 Test2 Test3 Test4 Test5"

# re.match(pattern, string) - призначений для пошуку за заданим шаблоном на початку рядка
result = re.match(pattern=r"Test", string=string)
print(result)

# метод group() повертає фрагмент рядка, в якому було виявлено збіг
print(result.group(0))

# поле string поверне рядок, який передавали для пошуку
print(result.string)

# Результат - None, т.к. фрагмент знаходиться не спочатку
result1 = re.match(pattern=r"Test2", string=string)
print(result1)