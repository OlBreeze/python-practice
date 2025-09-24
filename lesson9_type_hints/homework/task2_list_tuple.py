# Завдання 2: Робота зі складними структурами
#
# Реалізуйте функцію filter_adults, яка приймає список людей у форматі List[Tuple[str, int]],
# де кожен елемент – це кортеж із іменем (str) та віком (int).
# Функція повертає список лише повнолітніх (вік 18+).
from typing import List, Tuple


def filter_adults(people: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Фільтрує список людей і повертає лише тих, хто є повнолітнім (18 років і старше).
    Args:
        people (List[Tuple[str, int]]): Список кортежів, де кожен кортеж містить ім’я (str)
                                        та вік (int) людини.
    Returns:
        List[Tuple[str, int]]: Новий список, який містить лише тих людей, вік яких дорівнює або перевищує 18 років.
    """
    return [person for person in people if person[1] >= 18]

# Check in homework.py
# people = [("Андрій", 25), ("Олег", 16), ("Марія", 19), ("Ірина", 15)]
#
# print(filter_adults(people))
