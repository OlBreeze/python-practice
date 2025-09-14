# Завдання 6: Інтерсепція методів класу (Proxy)
# Напишіть клас Proxy, який приймає на вхід об'єкт і переадресовує виклики методів цього об'єкта,
# додатково логуючи виклики (наприклад, виводячи назву методу та аргументи).
from typing import Any


class Proxy:
    """
    Клас-проксі, який приймає об'єкт і переадресовує всі виклики методів до нього,
    логуючи назви методів і передані аргументи.
    """

    def __init__(self, target: Any) -> None:
        """
        Ініціалізація проксі з цільовим об'єктом.

        :param target: Об'єкт, до якого будуть переадресовані виклики.
        """
        self._target = target

    def __getattr__(self, name: str) -> Any:
        """
        Перехоплює доступ до атрибутів/методів, делегує їх цільовому об'єкту.
        Якщо це метод — обгортає логуванням.

        :param name: Назва атрибута або методу.
        :return: Значення атрибута або обгорнутий метод.
        """
        attr = getattr(self._target, name)

        if callable(attr):
            def wrapped(*args: Any, **kwargs: Any) -> Any:
                print("Calling method:")
                print(f"{name} with args: {args}")
                return attr(*args, **kwargs)

            return wrapped
        else:
            return attr


# -----------------------------------------------
class MyClass:
    def greet(self, name):
        return f"Hello, {name}!"


# ------------------------test-----------------------
obj = MyClass()
proxy = Proxy(obj)
print(proxy.greet("Alice"))
