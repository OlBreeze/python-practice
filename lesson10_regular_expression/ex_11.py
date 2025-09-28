import re # Додано імпорт для коректної роботи

# print(result) # Рядок 7 залежить від попереднього, невидимого коду.

result = re.findall(pattern=r'\w*', string='Qwerty Admin')
print(result)

result = re.findall(pattern=r'\w+', string='Qwerty Admin')
print(result)

# Вилучення першого слова
result = re.findall(pattern=r'^\w+', string='Qwerty Admin')
print(result)

# Вилучення останнього слова
result = re.findall(pattern=r'\w+$', string='Qwerty Admin')
print(result)