# 2. Numeric-like
# 1.	Реалізуйте клас Vector, що підтримує операції додавання, віднімання,
#   множення на число та порівняння за довжиною.
#   Використовуйте відповідні dunder-методи (__add__, __sub__, __mul__, __lt__, __eq__).
# 2.	Додайте до класу метод для отримання довжини вектора.

import math
from typing import Union


class Vector:
    def __init__(self, *elements: Union[int, float]) -> None:
        """Ініціалізує вектор з довільною кількістю числових компонент-координати вектора (x, y, z, ...)"""
        self.elements = elements

    def __add__(self, other: 'Vector') -> 'Vector':
        """Додає два вектори поелементно."""
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be of the same dimension")

        result = tuple(a + b for a, b in zip(self.elements, other.elements))
        # Це генераторний вираз, який по черзі:
        # бере пари (a, b) із zip(...)
        # складає їх (a + b)

        return Vector(*result)

    def __sub__(self, other: 'Vector') -> 'Vector':
        """Віднімає один вектор від іншого поелементно."""
        if len(self.elements) != len(other.elements):
            raise ValueError("Vectors must be of the same dimension")
        result = tuple(a - b for a, b in zip(self.elements, other.elements))
        return Vector(*result)

    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        """Множить вектор на число (скаляр)."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("Can only multiply by a scalar")
        result = tuple(a * scalar for a in self.elements)
        return Vector(*result)

    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        """Забезпечує підтримку множення: scalar * vector."""
        return self.__mul__(scalar)

    def __eq__(self, other: object) -> bool:
        """Перевіряє, чи мають вектори однакову довжину.
        math.isclose(...) - говорить: Эти два числа почти одинаковые с точностью до 1e-9"""
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.length(), other.length(), rel_tol=1e-9)

    def __lt__(self, other: 'Vector') -> bool:  # «меньше чем»
        """
        Порівнює вектори за довжиною.
        :param other: інший вектор
        :return: True, якщо поточний коротший
        """
        return self.length() < other.length()

    def length(self) -> float:
        """Обчислює довжину (модуль) вектора """
        return math.sqrt(
            sum(a ** 2 for a in self.elements))  # формула для нахождения длины (модуля) вектора в пространстве

    def __repr__(self) -> str:
        """Повертає строкове представлення вектора."""
        return f"Vector{self.elements}"


v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)  # Vector(4, 6)
print(v1 - v2)  # Vector(2, 2)
print(v1 * 3)  # Vector(9, 12)
print(2 * v2)  # Vector(2, 4)
print(v1.length())  # 5.0
print(v1 > v2)  # True
