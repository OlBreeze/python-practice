import re

string = "Test1 Test2 Test3 Test4 Test5"

# re.compile(pattern[, repl], string) - можливість зібрати регулярне вираження в об'єкт, який у свою чергу можна
# використовувати для пошуку. Призначений для пошуку за заданим шаблоном і дозволяє уникнути переписування
# одного і того ж коду (виразу)
pattern = re.compile("T")
result1 = pattern.findall(string)
print(result1)

# Якщо шукане не знайшли, результат - порожній список
result2 = pattern.findall(string.lower())
print(result2)

phone_pattern = re.compile(r"\((\d{3})\) (\d{3})-(\d{4})")

text = """
Контактні дані співробітників:
- Іван Іванович: (123) 456-7890
- Ольга Петрівна: (987) 654-3210
- Олексій Сергійович: не вказано
- Олена Олександрівна: (555) 123-4567
"""

phone_numbers = phone_pattern.findall(text)

for number in phone_numbers:
    print("Знайдено номер телефону:", number)