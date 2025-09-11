# Завдання 9: Динамічне додавання властивостей
# Напишіть клас DynamicProperties, в якому можна динамічно додавати властивості через методи.
# Використовуйте вбудовані функції property() для створення геттера та сеттера під час виконання програми.

from typing import Any, Dict


class DynamicProperties:
    """
    Клас DynamicProperties дозволяє динамічно додавати властивості з геттерами та сеттерами під час виконання програми.
    """

    def __init__(self) -> None:
        """
        Ініціалізація об'єкта з приватним словником для зберігання значень властивостей.
        """
        self._values: Dict[str, Any] = {}

    def add_property(self, name: str, default_value: Any = None) -> None:
        """
        Додає нову властивість до класу динамічно з використанням property().

        :param name: Назва властивості
        :param default_value: Значення за замовчуванням
        """
        self._values[name] = default_value

        def getter(self) -> Any:
            """
            Геттер для властивості.
            """
            return self._values.get(name)

        def setter(self, value: Any) -> None:
            """
            Сеттер для властивості.
            """
            self._values[name] = value

        # Додаємо property до класу динамічно
        setattr(
            self.__class__,
            name,
            property(fget=getter, fset=setter, doc=f"Динамічна властивість '{name}'")
        )


# --- Приклад використання ---
if __name__ == "__main__":
    obj = DynamicProperties()
    obj.add_property('name', 'default_name')
    print(obj.name)  # default_name
    obj.name = "Python"
    print(obj.name)  # Python
