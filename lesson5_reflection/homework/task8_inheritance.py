# Завдання 8: Перевірка успадкування та методів класу
# Напишіть функцію analyze_inheritance(cls), яка приймає клас, аналізує його спадкування та виводить усі методи,
# які він наслідує від базових класів.
from typing import Type, Dict


def analyze_inheritance(cls: Type) -> None:
    """
    Аналізує спадкування класу та виводить усі методи, які він наслідує від базових класів
    :param cls: Клас для аналізу.
    """
    own_methods = {
        name for name, value in cls.__dict__.items()
        if callable(value)
    }

    inherited_methods: Dict[str, str] = {}

    for base in cls.__mro__[1:]:  # Пропускаємо сам клас
        if base is object:
            continue  # Пропускаємо object

        for name, value in base.__dict__.items():
            if (
                    callable(value)
                    and name not in own_methods
                    and name not in inherited_methods
                    and not (name.startswith('__') and name.endswith('__'))  # Пропускаємо спеціальні методи
            ):
                inherited_methods[name] = base.__name__

    print(f"Клас {cls.__name__} наслідує:")
    if inherited_methods:
        for method, origin in sorted(inherited_methods.items()):
            print(f"- {method} з {origin}")
    else:
        print("- (немає успадкованих методів)")


# --------------------------------
class Parent:
    def parent_method(self):
        pass


class Child(Parent):
    def child_method(self):
        pass


analyze_inheritance(Child)
