# Написати функцію my_sum, яка перекриває вбудовану функцію sum.
# Функція повинна просто виводити повідомлення: "This is my custom sum function!".
import builtins
from typing import Any


def my_sum(*args: Any) -> str:
    """
    Функція my_sum, що перекриває вбудовану функцію sum
    та просто виводити повідомлення: "This is my custom sum function!
    """
    return "This is my custom sum function!"


original_sum = sum  # якщо я хочу зберегти початкову ф-ю
sum = my_sum

task1 = range(1, 10)
print(sum(task1))
print(my_sum(task1))
# print(builtins.sum(task1))
# повертаю original_sum
sum = original_sum
print(sum(task1))
print(my_sum(task1))

# Що відбувається, коли локальна функція має те саме ім’я, що й вбудована?
# Вона перекриває вбудовану у поточній області видимості. Виклик по імені виконає локальну функцію.

# Як отримати доступ до вбудованої функції, навіть якщо вона перекрита?
# - зберегти оригнальну функцію, та потім її повернути
# - Використати builtins.<назва_функції> або __builtins__.<назва_функції>.
