import timeit


def show_letters1(some_str):
    yield from ''.join([letter for letter in some_str if letter.isdigit()])


def show_letters2(some_str):
    return ''.join([letter for letter in some_str if letter.isdigit()])


print(type(show_letters1('qwerty')))
print(type(show_letters2('qwerty')))


'''
Вимірювання часу виконання шматка коду за допомогою модуля «timeit».
Модуль timeit дозволяє виміряти час виконання будь-якого шматка коду.
Великі шматки коду не дуже зручно, але дрібні досить добре. Закидаємо рядок всередину timeit і вуаля.
'''

print("Звичайний вираз", timeit.timeit("''.join(str(n) for n in range(10000))", number=10000))
print("Вираз-генератор", timeit.timeit("''.join((str(n) for n in range(10000)))", number=10000))
print("List expressions", timeit.timeit("''.join([str(n) for n in range(10000)])", number=10000))
print("MAP:", timeit.timeit("''.join(map(str, range(10000)))", number=10000))

# Что здесь происходит:
#
# show_letters1 возвращает генератор (yield from).
# show_letters2 возвращает строку (return).
# timeit используется для сравнения скорости:
# обычное выражение-генератор,
# явный генератор,
# list comprehension,
# map().

# <class 'generator'>
# <class 'str'>
# Звичайний вираз 9.482698500156403
# Вираз-генератор 9.422415100038052
# List expressions 7.584000100381672
# MAP: 7.010919900145382