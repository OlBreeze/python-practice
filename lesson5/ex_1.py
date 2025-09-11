class MyType1:
    x = 1.5
    c = 3

# Те саме визначення типу, але під час виконання за допомогою type()
MyType2 = type('MyType2', (object,), {'x': 1.5, 'c': 3})

print(MyType1)
print(type(MyType1))
print(MyType2)
print(type(MyType2))


# Два способа создания класса:
class A:
    x = 5

# Эквивалентно:
A2 = type('A2', (), {'x': 5})

# ----- FULL CREATE CLASS -----
from typing import Callable, Dict, Any, Type, Optional


def create_class(
    class_name: str,
    methods: Dict[str, Callable],
    attributes: Optional[Dict[str, Any]] = None
) -> Type:
    """
    Створює динамічний клас з методами та (опційно) атрибутами.

    :param class_name: Ім'я нового класу
    :param methods: Словник методів (назва: функція)
    :param attributes: (Необов'язково) словник атрибутів класу
    :return: Новий клас, створений динамічно
    """
    class_dict = {}

    # Додаємо методи
    for name, func in methods.items():
        class_dict[name] = func

    # Додаємо атрибути, якщо є
    if attributes:
        for attr_name, value in attributes.items():
            class_dict[attr_name] = value

    return type(class_name, (object,), class_dict)
# Test
def say_hello(self) -> str:
    return f"Hello, my name is {self.name}!"


def say_goodbye(self) -> str:
    return "Goodbye!"


@staticmethod
def static_info() -> str:
    return "Я — статичний метод."


# @classmethod
def class_info(cls) -> str:
    return f"Я — клас {cls.__name__}"


# Метод з параметрами
def repeat_phrase(self, phrase: str, times: int = 2) -> str:
    return " ".join([phrase] * times)


methods: Dict[str, Callable] = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye,
    "repeat_phrase": repeat_phrase,
    "static_info": staticmethod(static_info),
    "class_info": classmethod(class_info),
}

attributes: Dict[str, Any] = {
    "name": "DynamicPerson",
    "version": 1.0
}

MyDynamicClass = create_class("MyDynamicClass", methods, attributes)

# Тестування
if __name__ == "__main__":
    obj = MyDynamicClass()
    print(obj.say_hello())                 # Hello, my name is DynamicPerson!
    print(obj.say_goodbye())              # Goodbye!
    print(obj.repeat_phrase("Hi", 3))     # Hi Hi Hi
    print(obj.static_info())              # Я — статичний метод.
    print(obj.name)                       # DynamicPerson
    print(obj.version)                    # 1.0
    # print(obj.class_info())               # Я — клас MyDynamicClass
    print(MyDynamicClass.class_info())  # ✅ ПРАВИЛЬНО
