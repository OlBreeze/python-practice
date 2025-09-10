# Завдання 1: Перевірка типів і атрибутів об'єктів
# Напишіть функцію analyze_object(obj), яка приймає будь-який об'єкт та виводить:
# Тип об'єкта.
# Список всіх методів та атрибутів об'єкта.
# Тип кожного атрибута.
import inspect
from typing import Any


def analyze_object(obj: Any) -> None:
    print(f"Тип: {obj}")
    print(f"Ім'я класу: {obj.__class__.__name__}")

    all_members = dir(obj)
    methods = []
    attributes = []

    for name in all_members:
        if name.startswith('__') and name.endswith('__'):
            continue

        try:
            value = getattr(obj, name)
            if callable(value):
                methods.append(f"{name}: {type(value)}")
            else:
                attributes.append(f"{name}: {type(value)}")
            # print(f"- {name}: {type(value)}")
        except AttributeError:
            print(f"- {name}: <не вдалося отримати значення>")

    print("Методи:")
    for method in methods:
        print("-", method)
    print("Атрибуты:")
    for attribute in attributes:
        print("-", attribute)

    #2. callable:
    # methods = [member for member in all_members if callable(getattr(obj, member)) and not member.startswith("__")]
    # attributes = [member for member in all_members if
    #               not callable(getattr(obj, member)) and not member.startswith("__")]
    #3. inspect:
    # methods = [name for name, val in inspect.getmembers(obj, predicate=inspect.ismethod)]
    # attributes = [name for name, val in inspect.getmembers(obj) if not callable(val) and not name.startswith('__')]


# ---------------------------------------------------------
class MyClass:
    def __init__(self, value):
        self.value = value

    def say_hello(self):
        return f"Hello, {self.value}"


obj = MyClass("World")
analyze_object(obj)
