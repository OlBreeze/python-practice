# Завдання 4: Узагальнені типи (Generics)
#
# Реалізуйте функцію get_first, яка приймає список будь-якого типу List[T] і повертає його перший елемент.
# Якщо список порожній – повертає None.

from typing import List, TypeVar, Optional

T = TypeVar('T')  # Узагальнений тип


def get_first(items: List[T]) -> Optional[T]:
    """
    Повертає перший елемент зі списку будь-якого типу. Якщо список порожній – повертає None.

    Args:
        items (List[T]): Список елементів будь-якого типу.

    Returns:
        Optional[T]: Перший елемент списку або None, якщо список порожній.
    """
    if items:
        return items[0]
    return None

# Check in homework.py
# print(get_first([1, 2, 3]))
# print(get_first(["a", "b", "c"]))
# print(get_first([]))
