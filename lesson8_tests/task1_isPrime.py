# Isprime в Python — это название функции или метода из библиотеки, такой как sympy,
# предназначенная для проверки того, является ли заданное целое число простым.
# В математике простое число — это натуральное число больше 1, которое делится без остатка только на 1 и на себя самого.
#
# Функция isprime возвращает True, если число простое, и False в противном случае.
# Как работает isprime:
# 1. Проверка входных данных: Функция сначала проверяет, является ли входное значение целым числом.
# 2. Определение простоты:
# Отрицательные числа не являются простыми, поэтому isprime вернет False.
# Числа меньше или равные 1 также не считаются простыми.
# Для положительных целых чисел функция применяет алгоритм (например, тест Миллера-Рабина),
# чтобы определить, есть ли у числа другие делители, кроме 1 и самого себя.
from mpmath.libmp import isprime

assert isprime(0) == False
assert isprime(1) == False
assert isprime(2) == True
assert isprime(3) == True

assert isprime(5) == True
assert isprime(7) == True
assert isprime(13) == True
assert isprime(97) == True

assert isprime(4) == False
assert isprime(9) == False
assert isprime(100) == False

assert isprime(7919) == True
assert isprime(8000) == False
