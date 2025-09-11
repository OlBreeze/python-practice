# Завдання 5: Модифікація атрибутів під час виконання
# Напишіть клас MutableClass, який має методи для динамічного додавання та видалення атрибутів об'єкта.
# Реалізуйте методи add_attribute(name, value) та remove_attribute(name).
from typing import Any


class MutableClass:
    """
    Клас, що дозволяє динамічно додавати та видаляти атрибути під час виконання програми.
    """

    def add_attribute(self, name: str, value: Any) -> None:
        """
        Додає новий атрибут до об'єкта.

        :param name: Назва атрибута
        :param value: Значення атрибута
        """
        setattr(self, name, value)

    def remove_attribute(self, name: str) -> None:
        """
        Видаляє атрибут з об'єкта, якщо він існує.

        :param name: Назва атрибута
        """
        if hasattr(self, name):
            delattr(self, name)
        else:
            print(f"Атрибут '{name}' не знайдено.")


# -----------
if __name__ == "__main__":
    obj = MutableClass()

    # Додавання атрибутів
    obj.add_attribute("name", "Python")
    obj.add_attribute("version", 1.0)

    print(obj.name)  # Python
    print(obj.version)  # 1.0

    # Видалення атрибута
    obj.remove_attribute("version")
    print(f"hasattr version: {hasattr(obj, "version")}")  # False

    # Спроба видалити неіснуючий атрибут
    obj.remove_attribute("nonexistent")
    obj.remove_attribute("name")
    print(f"hasattr name: {hasattr(obj, "name")}")  # False
    # print(obj.name)  # Виникне помилка, атрибут видалений
