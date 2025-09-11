# Завдання 4: Створення класу динамічно
# Напишіть функцію create_class(class_name, methods), яка створює клас з заданим іменем та методами.
# Методи передаються у вигляді словника, де ключі — це назви методів, а значення — функції.
from typing import Dict, Callable, Type


def create_class(class_name: str, methods: Dict[str, Callable]) -> Type:
    """
    Створює динамічний клас з заданим ім'ям та методами.

    :param class_name: Ім'я нового класу
    :param methods: Словник, де ключі — це назви методів, а значення — функції
    :return: Новий клас, створений динамічно
    """
    return type(class_name, (object,), methods)


def say_hello(self):
    return "Hello!"


def say_goodbye(self):
    return "Goodbye!"


# Словник методів для нового класу
methods: Dict[str, Callable] = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye
}

MyDynamicClass = create_class("MyDynamicClass", methods)

obj = MyDynamicClass()
print(obj.say_hello())  # Hello!
print(obj.say_goodbye())  # Goodbye!
