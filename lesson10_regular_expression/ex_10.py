# Припускаємо, що result був визначений раніше, наприклад:
# import re
# result = re.findall(pattern=r'\w', string='Qwerty Admin')
# print(result) # виведе ['Q', 'w', 'e', 'r', 't', 'y', 'A', 'd', 'm', 'i', 'n']
import re

# print(result) # Цей рядок залежить від попереднього, невидимого коду

result = re.findall(pattern=r'\w', string='Qwerty Admin')
print(result)

result = re.findall(pattern=r'\w+', string='Qwerty Admin')
print(result)

# Вилучення першого слова
result = re.findall(pattern=r'^\w+', string='Qwerty Admin')
print(result)

# Вилучення останнього слова
result = re.findall(pattern=r'\w+$', string='Qwerty Admin')
print(result)