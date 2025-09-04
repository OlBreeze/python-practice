# 3. to-Compare
# 1. Реалізуйте клас Person із параметрами name та age.
#   Додайте методи для порівняння за віком (__lt__, __eq__, __gt__).
# 2. Напишіть програму для сортування списку об'єктів класу Person за віком.
from typing import Any


class Person:
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

print("До сортування:")
print(people)

people.sort()

print("\nПісля сортування:")
print(people)
