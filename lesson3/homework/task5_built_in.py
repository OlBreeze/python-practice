# 5. For built-in functions implementation
# 1.	Реалізуйте власну версію функцій len(), sum(), та min().
#       Використовуйте спеціальні методи __len__, __iter__, __getitem__, якщо необхідно.
# 2.	Напишіть тест для кожної з реалізованих функцій.

from typing import Iterable, TypeVar, Any, Union

T = TypeVar('T')


def my_sum(iterable: Iterable[Union[int, float]]) -> Union[int, float]:
    """
    Складає всі елементи ітерабельного об'єкта.

    :param iterable: Ітерабельний об'єкт чисел
    :return: Сума всіх елементів
    """
    total: Union[int, float] = 0
    if hasattr(iterable, '__iter__'):
        for item in iterable:
            total += item
    else:
        raise TypeError(f"'{type(iterable).__name__}' object is not iterable")
    return total


def my_len(obj: Any) -> int:
    """
    Повертає довжину об'єкта, використовуючи метод __len__ або __getitem__.

    :param obj: Об'єкт з методом __len__ або __getitem__
    :return: Ціле число — довжина
    """
    if hasattr(obj, '__len__'):
        return obj.__len__()
    elif hasattr(obj, '__getitem__'):
        count = 0
        while True:
            try:
                count += 1
            except IndexError:
                return count
    else:
        raise TypeError("Object has no len() or __getitem__ method")


def my_min(iterable: Iterable[T]) -> T:
    """
    Знаходить мінімальний елемент в ітерабельному об'єкті.

    :param iterable: Ітерабельний об'єкт
    :return: Мінімальне значення
    """
    iterator = iter(iterable)
    try:
        minimum = next(iterator)
    except StopIteration:
        raise ValueError("my_min() arg is an empty iterable")

    for item in iterator:
        if item < minimum:
            minimum = item
    return minimum


# ========================== test =========
class CustomList:
    def __init__(self, data: list[int]) -> None:
        """Реализация __init__"""
        self.data = data

    def __len__(self) -> int:
        """Реализация __len__"""
        return len(self.data)

    def __iter__(self):
        """Реализация __iter__"""
        return iter(self.data)


my_obj = CustomList([1, 2, 3, 4])
numbers = [1, 2, 3, 4, 5]
data = [5, 3, 7, 2, 8]
# -------------------------------------

if my_len(my_obj) == 4:
    print("my_len пройшов тест")

if my_sum(numbers) == 15:
    print("my_sum пройшов тест")
if my_sum(my_obj) == 10:
    print("my_sum пройшов тест")

if my_min(data) == 2:
    print("my_min пройшов тест")
