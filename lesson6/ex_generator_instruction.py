"""
Інструкція дозволяє створювати генератори.

На відміну від оголошення return у функції, де повертається один об’єкт, yield при кожному виклику функції генерує
новий об’єкт. Фактично це дозволяє використовувати генератори в циклах. Найважливіша причина застосування такої
інструкції – економія пам’яті, коли не потрібно зберігати всю послідовність, а можна отримувати її елементи
одному.

Студент написав генератор show_letters(some_str), що виводить усі символи рядка на друк, але тільки в тому випадку,
якщо вони є літерами (інші ігноруються). Необхідно скоротити код функції.
"""

def show_letters(some_str):
    clean_str = ''.join([letter for letter in some_str if letter.isalpha()])
    for symbol in clean_str:
        yield symbol


"""
Конструкція yield from дозволяє повністю забрати цикл з функції. Вона "вкладає" один генератор всередину іншого,
що дає можливість керування кількома генераторами.
"""

def show_letters2(some_str):
    yield from ''.join([letter for letter in some_str if letter.isalpha()])


# --- Тестирование генераторов ---
random_str = show_letters('B?wah 75 - sw')
print(next(random_str))
print(next(random_str))
print(next(random_str))
print(next(random_str))
print(next(random_str))
print(next(random_str))
# print(next(random_str))  # здесь будет StopIteration

print()

random_str2 = show_letters2('B?wah 75 - s')
print(next(random_str2))
print(next(random_str2))
print(next(random_str2))
print(next(random_str2))
print(next(random_str2))
# print(next(random_str2))
