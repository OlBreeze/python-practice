# Завдання 10: Метаклас для контролю створення класів
# Реалізуйте метаклас SingletonMeta,
# який гарантує, що клас може мати лише один екземпляр (патерн Singleton).
# Якщо екземпляр класу вже створений, наступні виклики повинні повертати той самий об'єкт.
from typing import Any, Dict


class SingletonMeta(type):
    """
    Метаклас SingletonMeta гарантує, що клас має лише один екземпляр.
    Використовується для реалізації патерну Singleton.
    """

    # Словник для зберігання екземплярів класів
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs) -> Any:
        """
        Перевизначення виклику класу. Якщо екземпляр вже існує — повертає його.
        Інакше створює новий і зберігає.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# --------------------------
class Singleton(metaclass=SingletonMeta):
    def __init__(self):
        print("Creating instance")


obj1 = Singleton()  # Creating instance
obj2 = Singleton()
print(obj1 is obj2)  # True
