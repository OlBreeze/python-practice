# 3. to-Compare
# 1. Реалізуйте клас Person із параметрами name та age.
#   Додайте методи для порівняння за віком (__lt__, __eq__, __gt__).
# 2. Напишіть програму для сортування списку об'єктів класу Person за віком.
from typing import Any


class Person:
    species = "Homo sapiens"

    def __init__(self, name: str, age: int) -> None:
        """Ініціалізує об'єкт класу Person з ім'ям та віком."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Повертає рядкове представлення об'єкта."""
        return f"{self.name} {self.age}"

    def __eq__(self, other: Any) -> bool:
        """Перевіряє рівність за віком."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age == other.age

    def __lt__(self, other: Any) -> bool:
        """Порівнює, чи менший вік поточного об'єкта."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age < other.age

    def __gt__(self, other: Any) -> bool:
        """Порівнює, чи більший вік поточного об'єкта."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.age > other.age


# ==================================
people: list[Person] = [
    Person("Андрій", 25),
    Person("Олена", 19),
    Person("Богдан", 32),
    Person("Марія", 25)
]

# print("До сортування:")
# print(people)
#
# people.sort()
#
# print("\nПісля сортування:")
# print(people)

#-------------------------L5
person = Person("Іван", 25)
print(f"isinstance(person, Person): {isinstance(person, Person)}")
print(f"type(person) is Person: {type(person) is Person}")
print(f"Тип об'єкта: {type(person)}")
print(f"Ім'я класу: {type(person).__name__}")

print(f"hasattr(person, 'name'): {hasattr(person, 'name')}")
print(f"hasattr(person, 'salary'): {hasattr(person, 'salary')}")

print(f"getattr(person, 'name'): {getattr(person, 'name')}")
print(f"getattr(person, 'salary'): {getattr(person, 'salary', 'Не знайдено')}")

setattr(person, 'city', 'Київ')
print(f"setattr(person, 'city'): {person.city}")

print(person.__dict__)

delattr(person, 'city')
print(person.__dict__)

print(Person.__dict__)
delattr(Person, 'species')
print(Person.__dict__)