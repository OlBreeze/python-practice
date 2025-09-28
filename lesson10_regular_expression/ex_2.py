import re

string = "Test1 Test2 Test3 Test4 Test5" # Додано для повноти

# re.match(pattern, string) - призначений для пошуку за заданим шаблоном на початку рядка
result = re.match(pattern=r"Test", string=string)

# метод span() поверне кортеж, який містить початкову та кінцеву позиції шуканого фрагмента
print(result.span())

# Позиція початку шаблону в рядку
print(result.start())

# Позиція кінця шаблону в рядку
print(result.end())

print(result, result.span(), result.string, result.group(), sep='\n')