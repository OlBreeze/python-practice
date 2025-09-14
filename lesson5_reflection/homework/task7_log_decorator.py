# Завдання 7: Декоратор для логування викликів методів
# Реалізуйте декоратор log_methods, який додається до класу і логуватиме виклики всіх його методів
# (назва методу та аргументи).

from typing import Any, Type
import types
import functools


def log_methods(cls: Type) -> Type:
    """
    Декоратор класу, який обгортає всі методи класу
    для логування їх викликів (назва методу + аргументи).

    :param cls: Клас, до якого застосовується декоратор.
    :return: Клас з обгорнутими методами.
    """

    for attr_name, attr_value in cls.__dict__.items():
        if isinstance(attr_value, (types.FunctionType, types.MethodType)):
            # Обгортаємо тільки методи екземпляра
            original_method = attr_value

            @functools.wraps(original_method)
            def wrapper(self, *args: Any, __method=original_method, __name=attr_name, **kwargs: Any) -> Any:
                print(f"Logging: {__name} called with {args}")
                return __method(self, *args, **kwargs)

            setattr(cls, attr_name,
                    wrapper)  # У класі cls, заміни (або встанови) метод з іменем attr_name на нову функцію wrapper

    return cls


@log_methods
class MyClass:
    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b


# ---------------------- Тестування:
obj = MyClass()
obj.add(5, 3)  # Logging: add called with (5, 3)
obj.subtract(5, 3)  # Logging: subtract called with (5, 3)
