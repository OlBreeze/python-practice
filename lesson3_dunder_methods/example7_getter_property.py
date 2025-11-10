class Person:
    def __init__(self, name, age, balance):
        self._name = name
        self._age = age
        self.__balance = balance  # Note the double underscore for name mangling

    def __str__(self):
        return f"{self._name} is {self._age} years old. Balance is {self.__balance}"

    # Методы для balance
    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

    # Методы для name
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    def __test_method(self):# СКРЫТЫЙ МЕТОД ВЫТАЩИМ И ВЫПОЛНИМ ИЗ СЛОВАРЯ!!!
        return "Test"


p1 = Person(name="John", age=36, balance=1000)
print(p1)

print(p1.get_balance())

p1.set_balance(1500)
print(p1.get_balance())

print(p1.get_name())

p1.set_name("Max")
print(p1.get_name())

print(p1.age)

p1.age = 37
print(p1.age)

print(p1.__dict__)
print(Person.__dict__)
print(p1._Person__test_method())
