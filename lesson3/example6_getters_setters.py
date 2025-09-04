class Person:
    def __init__(self, name, age, balance):
        self._name = name
        self._age = age
        self.__balance = balance  # Note the double underscore for name mangling

    def __str__(self):
        return f"{self._name} is {self._age} years old. Balance is {self.__balance}"

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

p1 = Person(name="John", age=36, balance=1000)
print(p1)
print(p1.get_balance())

p1.set_balance(1500)
print(p1.get_balance())