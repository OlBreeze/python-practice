# Завдання 2: Динамічний виклик функцій
# Реалізуйте функцію
# call_function(obj, method_name, *args),
# яка приймає об'єкт, назву методу в вигляді рядка та довільні аргументи для цього методу.
# Функція повинна викликати відповідний метод об'єкта і повернути результат.

from typing import Any


class Calculator:
    """
    Calculator.
    """

    def add(self, a: float, b: float) -> float:
        """
        Додає два числа.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """
        Віднімає друге число від першого.
        """
        return a - b


def call_function(obj: Any, method_name: str, *args: Any) -> Any:
    """
    Динамічно викликає метод об'єкта за назвою методу.

    :param obj: Об'єкт, у якого потрібно викликати метод
    :param method_name: Назва методу у вигляді рядка
    :param args: Аргументи, які передаються до методу
    :return: Результат виклику методу або None, якщо сталася помилка
    """
    # print(f"Test: {obj.__class__.__name__}.{method_name}")

    try:
        method = getattr(obj, method_name)  # отримуємо метод по імені
        return method(*args)  # викликаємо метод з аргументами
    except AttributeError:
        print("Error: Об’єкт не має такого методу.")
    except Exception:
        print("Error.")


calc = Calculator()
print(call_function(calc, "add", 10, 5))  # 15
print(call_function(calc, "subtract", 10, 5))  # 5
