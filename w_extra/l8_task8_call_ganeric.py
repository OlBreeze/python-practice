# Завдання 8: Callable та Generics
#
# Створіть узагальнений клас Processor[T], який:
#
# Приймає список data: List[T]
# Має метод apply(func: Callable[[T], T]) -> List[T], який застосовує передану функцію до всіх елементів списку.
# Реалізуйте приклад із застосуванням функцій double(x: int) -> int та to_upper(s: str) -> str.
from typing import TypeVar, Generic, List, Callable, Optional, Union, Any
from functools import reduce
import math

# Визначаємо типову змінну
T = TypeVar('T')
U = TypeVar('U')


# ========== ОСНОВНИЙ КЛАС PROCESSOR ==========

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

    def apply(self, func: Callable[[T], T]) -> List[T]:
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

    def size(self) -> int:
        """Повертає кількість елементів"""
        return len(self._data)

    def __repr__(self) -> str:
        """Строкове представлення процесора"""
        return f"Processor({self._data})"


# ========== РОЗШИРЕНИЙ ПРОЦЕСОР ==========

class AdvancedProcessor(Generic[T]):
    """Розширений процесор з додатковими методами"""

    def __init__(self, data: List[T]) -> None:
        self._data: List[T] = data.copy()

    def apply(self, func: Callable[[T], T]) -> List[T]:
        """Застосовує функцію до всіх елементів"""
        return [func(item) for item in self._data]

    def map_to(self, func: Callable[[T], U]) -> 'AdvancedProcessor[U]':
        """
        Перетворює елементи в інший тип

        Args:
            func: Функція перетворення T -> U

        Returns:
            Новий процесор з типом U
        """
        transformed_data = [func(item) for item in self._data]
        return AdvancedProcessor(transformed_data)

    def filter(self, predicate: Callable[[T], bool]) -> 'AdvancedProcessor[T]':
        """
        Фільтрує елементи за предикатом

        Args:
            predicate: Функція, яка повертає True для елементів, які потрібно залишити

        Returns:
            Новий процесор з відфільтрованими даними
        """
        filtered_data = [item for item in self._data if predicate(item)]
        return AdvancedProcessor(filtered_data)

    def reduce(self, func: Callable[[T, T], T], initial: Optional[T] = None) -> T:
        """
        Згортає список до одного значення

        Args:
            func: Функція згортання
            initial: Початкове значення

        Returns:
            Результат згортання
        """
        if initial is not None:
            return reduce(func, self._data, initial)
        return reduce(func, self._data)

    def chain(self, *funcs: Callable[[T], T]) -> List[T]:
        """
        Застосовує послідовність функцій

        Args:
            funcs: Послідовність функцій для застосування

        Returns:
            Результат послідовного застосування функцій
        """
        result = self._data.copy()
        for func in funcs:
            result = [func(item) for item in result]
        return result

    def apply_conditional(self, condition: Callable[[T], bool],
                          true_func: Callable[[T], T],
                          false_func: Callable[[T], T]) -> List[T]:
        """
        Умовне застосування функцій

        Args:
            condition: Умова для перевірки
            true_func: Функція для застосування, якщо умова True
            false_func: Функція для застосування, якщо умова False

        Returns:
            Список з результатами умовного застосування
        """
        return [
            true_func(item) if condition(item) else false_func(item)
            for item in self._data
        ]

    def get_data(self) -> List[T]:
        """Повертає копію даних"""
        return self._data.copy()

    def __repr__(self) -> str:
        return f"AdvancedProcessor({self._data})"


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


def add_exclamation(s: str) -> str:
    """Додає знак оклику"""
    return s + "!"


def is_even(x: int) -> bool:
    """Перевіряє чи число парне"""
    return x % 2 == 0


def is_long_word(s: str) -> bool:
    """Перевіряє чи слово довге (>4 символи)"""
    return len(s) > 4


# Функції перетворення типів
def int_to_str(x: int) -> str:
    """Перетворює int в str"""
    return str(x)


def str_to_len(s: str) -> int:
    """Повертає довжину рядка"""
    return len(s)


def float_to_int(x: float) -> int:
    """Перетворює float в int"""
    return int(x)


# ========== ДЕМОНСТРАЦІЯ ВИКОРИСТАННЯ ==========

def basic_examples():
    """Базові приклади використання"""
    print("=== БАЗОВІ ПРИКЛАДИ ===\n")

    # Приклад 1: Обробка чисел
    print("1. Обробка чисел:")
    p1 = Processor([1, 2, 3])
    print(f"Початкові дані: {p1.get_data()}")
    print(f"Подвоєння: {p1.apply(lambda x: x * 2)}")
    print(f"З функцією double: {p1.apply(double)}")
    print(f"Квадрати: {p1.apply(square)}")
    print()

    # Приклад 2: Обробка рядків
    print("2. Обробка рядків:")
    p2 = Processor(["hello", "world"])
    print(f"Початкові дані: {p2.get_data()}")
    print(f"Верхній регістр: {p2.apply(str.upper)}")
    print(f"З функцією to_upper: {p2.apply(to_upper)}")
    print(f"З окликами: {p2.apply(add_exclamation)}")
    print()

    # Приклад 3: Обробка float
    print("3. Обробка float:")
    p3 = Processor([1.1, 2.5, 3.8, 4.2])
    print(f"Початкові дані: {p3.get_data()}")
    print(f"Округлення: {p3.apply(round)}")
    print(f"Квадратний корінь: {p3.apply(math.sqrt)}")
    print()


def advanced_examples():
    """Розширені приклади з AdvancedProcessor"""
    print("=== РОЗШИРЕНІ ПРИКЛАДИ ===\n")

    # Приклад 1: Перетворення типів
    print("1. Перетворення типів:")
    p1 = AdvancedProcessor([1, 2, 3, 4, 5])
    print(f"Числа: {p1.get_data()}")

    p1_str = p1.map_to(int_to_str)
    print(f"В рядки: {p1_str.get_data()}")

    p1_back = p1_str.map_to(int)
    print(f"Назад в числа: {p1_back.get_data()}")
    print()

    # Приклад 2: Фільтрація
    print("2. Фільтрація:")
    p2 = AdvancedProcessor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Всі числа: {p2.get_data()}")

    even_processor = p2.filter(is_even)
    print(f"Парні числа: {even_processor.get_data()}")

    doubled_evens = even_processor.apply(double)
    print(f"Подвоєні парні: {doubled_evens}")
    print()

    # Приклад 3: Згортання
    print("3. Згортання:")
    p3 = AdvancedProcessor([1, 2, 3, 4, 5])
    print(f"Числа: {p3.get_data()}")

    sum_result = p3.reduce(lambda a, b: a + b)
    print(f"Сума: {sum_result}")

    product_result = p3.reduce(lambda a, b: a * b, 1)
    print(f"Добуток: {product_result}")
    print()

    # Приклад 4: Ланцюжок функцій
    print("4. Ланцюжок функцій:")
    p4 = AdvancedProcessor([1, 2, 3, 4, 5])
    print(f"Початкові: {p4.get_data()}")

    chained_result = p4.chain(
        lambda x: x * 2,  # Подвоїти
        lambda x: x + 1,  # Додати 1
        lambda x: x ** 2  # В квадрат
    )
    print(f"Ланцюжок (x*2 + 1)²: {chained_result}")
    print()

    # Приклад 5: Умовне застосування
    print("5. Умовне застосування:")
    p5 = AdvancedProcessor([1, 2, 3, 4, 5, 6])
    print(f"Числа: {p5.get_data()}")

    conditional_result = p5.apply_conditional(
        condition=is_even,
        true_func=lambda x: x * 10,  # Парні * 10
        false_func=lambda x: x * -1  # Непарні * -1
    )
    print(f"Умовне застосування: {conditional_result}")
    print()


def complex_example():
    """Складний приклад комбінування операцій"""
    print("=== СКЛАДНИЙ ПРИКЛАД ===\n")

    # Обробка списку рядків
    words = ["python", "java", "go", "rust", "javascript", "c"]
    processor = AdvancedProcessor(words)

    print(f"Початкові слова: {processor.get_data()}")

    # Фільтруємо довгі слова, перетворюємо у верхній регістр, додаємо оклик
    result = (processor
              .filter(is_long_word)  # Тільки довгі слова
              .apply(to_upper)  # У верхній регістр
              .apply(add_exclamation))  # Додаємо оклик

    print(f"Довгі слова у верхньому регістрі з окликами: {result}")

    # Перетворюємо в довжини
    lengths = processor.map_to(str_to_len)
    print(f"Довжини слів: {lengths.get_data()}")

    # Сума довжин довгих слів
    long_words_total_length = (processor
                               .filter(is_long_word)
                               .map_to(str_to_len)
                               .reduce(lambda a, b: a + b, 0))

    print(f"Загальна довжина довгих слів: {long_words_total_length}")


def type_safety_examples():
    """Приклади type safety"""
    print("\n=== TYPE SAFETY ===\n")

    # Це працює - правильні типи
    int_processor: Processor[int] = Processor([1, 2, 3])
    doubled = int_processor.apply(lambda x: x * 2)  # int -> int ✅
    print(f"Подвоєні цілі: {doubled}")

    str_processor: Processor[str] = Processor(["hello", "world"])
    upper = str_processor.apply(str.upper)  # str -> str ✅
    print(f"У верхньому регістрі: {upper}")

    # Приклад з float
    float_processor: Processor[float] = Processor([1.5, 2.7, 3.1])
    rounded = float_processor.apply(lambda x: float(int(x)))  # float -> float ✅
    print(f"Округлені float: {rounded}")

    print("\n✅ Всі операції типобезпечні!")


def main():
    """Головна функція демонстрації"""
    print("🔧 УЗАГАЛЬНЕНИЙ ПРОЦЕСОР З CALLABLE ТА GENERICS 🔧\n")

    basic_examples()
    advanced_examples()
    complex_example()
    type_safety_examples()

    print("\n" + "=" * 50)
    print("📋 ПІДСУМОК:")
    print("✅ Generic клас Processor[T]")
    print("✅ Callable[[T], T] для функцій обробки")
    print("✅ Type safety з TypeVar")
    print("✅ Розширений функціонал (map_to, filter, reduce)")
    print("✅ Ланцюжок операцій")
    print("✅ Умовне застосування")
    print("✅ Перетворення типів")


if __name__ == "__main__":
    main()