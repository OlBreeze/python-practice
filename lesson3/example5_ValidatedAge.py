class ValidatedAge:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a non-negative integer")
        instance.__dict__[self.name] = value


class Person:
    age = ValidatedAge()  # Дескриптор

    def __init__(self, name, age):
        self.name = name
        self.age = age


p = Person("Alice", 30)
print(p.age)  # Виведе: 30
p.age = 25
# p.age = -1  # Викличе ValueError