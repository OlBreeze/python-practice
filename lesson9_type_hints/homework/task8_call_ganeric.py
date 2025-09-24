# Завдання 8: Callable та Generics
#
# Створіть узагальнений клас Processor[T], який:
#
# Приймає список data: List[T]
# Має метод apply(func: Callable[[T], T]) -> List[T], який застосовує передану функцію до всіх елементів списку.
# Реалізуйте приклад із застосуванням функцій double(x: int) -> int та to_upper(s: str) -> str.

from typing import TypeVar, Generic, List, Callable, Optional, Union, Any

# Визначаємо типову змінну
T = TypeVar('T')


class Processor(Generic[T]):
    """
    Узагальнений клас для обробки списків даних

    Type Parameters:
        T: Тип елементів у списку
    """

    def __init__(self, data: List[T]) -> None:
        """
        Ініціалізація процесора з даними

        Args:
            data: Список елементів типу T
        """
        self._data: List[T] = data.copy()  # Створюємо копію для безпеки

    def apply(self, func: Callable[[T], T]) -> List[T]: # Тип Callable[[T], T] означает, что func — это функция, которая принимает аргумент типа T и возвращает тоже T.
        """
        Застосовує функцію до всіх елементів списку

        Args:
            func: Функція, яка приймає T і повертає T

        Returns:
            Новий список з результатами застосування функції
        """
        return [func(item) for item in self._data]

    def get_data(self) -> List[T]:
        """Повертає копію даних"""
        return self._data.copy()


# ========== ФУНКЦІЇ ДЛЯ ДЕМОНСТРАЦІЇ ==========

def double(x: int) -> int:
    """Подвоює число"""
    return x * 2


def to_upper(s: str) -> str:
    """Перетворює рядок у верхній регістр"""
    return s.upper()


def square(x: int) -> int:
    """Возводить число у квадрат"""
    return x * x


def main():
    """Головна функція демонстрації"""

    # Приклад 1: Обробка чисел
    print("1. Обробка чисел:")
    p1 = Processor([1, 2, 3])
    print(f"Початкові дані: {p1.get_data()}")
    print(f"Подвоєння: {p1.apply(lambda x: x * 2)}")
    print(f"З функцією double: {p1.apply(double)}")
    print(f"Квадрати: {p1.apply(square)}")
    # Приклад з float
    float_processor: Processor[float] = Processor([1.5, 2.7, 3.1])
    rounded = float_processor.apply(lambda x: float(int(x)))  # float -> float ✅
    print(f"Округлені float: {rounded}")
    print()

    # Приклад 2: Обробка рядків
    print("2. Обробка рядків:")
    p2 = Processor(["hello", "world"])
    print(f"Початкові дані: {p2.get_data()}")
    print(f"Верхній регістр: {p2.apply(to_upper)}")
    print()


if __name__ == "__main__":
    main()
