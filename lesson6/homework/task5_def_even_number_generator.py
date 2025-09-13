# 5. Генератор для створення нескінченної послідовності
#
# Створіть генератор, який генерує нескінченну послідовність парних чисел.
# Використайте менеджер контексту для обмеження кількості генерованих чисел до 100 і збереження їх у файл.

from typing import Iterator
from contextlib import contextmanager


def even_number_generator(start: int = 0) -> Iterator[int]:
    """
    Генератор нескінченної послідовності парних чисел.
    """
    num: int = start if start % 2 == 0 else start + 1
    while True:
        yield num
        num += 2


@contextmanager
def limited_number_writer(generator: Iterator[int], limit: int, file_path: str):
    """
    Менеджер контексту, який записує певну кількість чисел із генератора у файл.

    :param generator: Генератор чисел (наприклад, нескінченний).
    :param limit: Кількість чисел для запису.
    :param file_path: Шлях до файлу для запису.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for _ in range(limit):
            number = next(generator)
            file.write(f"{number}\n")
    yield  # Контекст завершується тут — після запису

if __name__ == "__main__":
    gen = even_number_generator(200)
    with limited_number_writer(gen, limit=100, file_path="task5_files/task5_even_numbers2.txt"):
        print("Числа записані у файл.")

# добавить ексепшены