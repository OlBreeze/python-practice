# 1.	Реалізуйте клас Fraction (дробові числа), який має методи для додавання, віднімання,
#   множення та ділення двох об'єктів цього класу.
#   Використайте спеціальні методи __add__, __sub__, __mul__, __truediv__.

from math import gcd


class Fraction:
    """
      Клас, що представляє звичайний дріб з чисельником і знаменником.
      Підтримує арифметичні операції: додавання, віднімання, множення та ділення.
      """

    def __init__(self, numerator: int, denominator: int) -> None:
        """
        Ініціалізує новий дріб.
        Args:
            numerator (int): чисельник дробу.
            denominator (int): знаменник дробу (не може дорівнювати нулю).
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        self.numerator = numerator
        self.denominator = denominator
        self._reduce()

    def _reduce(self) -> None:
        """Скорочує дріб, ділячи чисельник і знаменник на їхній найбільший спільний дільник."""
        common = gcd(self.numerator, self.denominator)
        self.numerator //= common
        self.denominator //= common

    def __add__(self, other: "Fraction") -> "Fraction":
        """Додає два дроби."""
        if isinstance(other, Fraction):
            num = self.numerator * other.denominator + other.numerator * self.denominator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        return NotImplemented

    def __sub__(self, other: "Fraction") -> "Fraction":
        """ Віднімає інший дріб від поточного."""
        if isinstance(other, Fraction):
            num = self.numerator * other.denominator - other.numerator * self.denominator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        return NotImplemented

    def __mul__(self, other: "Fraction") -> "Fraction":
        """Множить два дроби."""
        if isinstance(other, Fraction):
            num = self.numerator * other.numerator
            den = self.denominator * other.denominator
            return Fraction(num, den)
        return NotImplemented

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """Ділить поточний дріб на інший."""
        if isinstance(other, Fraction):
            if other.numerator == 0:
                raise ZeroDivisionError("Division by zero fraction")
            num = self.numerator * other.denominator
            den = self.denominator * other.numerator
            return Fraction(num, den)

        return NotImplemented

    def __repr__(self):
        """Повертає рядкове представлення дробу у форматі "numerator/denominator"."""
        return f"{self.numerator}/{self.denominator}"


a = Fraction(1, 2)  # 1/2
b = Fraction(3, 4)  # 3/4

print(a + b)  # 5/4
print(a - b)  # -1/4
print(a * b)  # 3/8
print(a / b)  # 2/3
