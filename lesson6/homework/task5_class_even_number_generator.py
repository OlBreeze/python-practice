# 5. Генератор для створення нескінченної послідовності
#
# Створіть генератор, який генерує нескінченну послідовність парних чисел.
# Використайте менеджер контексту для обмеження кількості генерованих чисел до 100 і збереження їх у файл.

from typing import Iterator


def even_number_generator(start: int = 0) -> Iterator[int]:
    """
    Нескінченний генератор парних чисел, починаючи з 'start'.

    :param start: Початкове число (за замовчуванням 0).
    :return: Ітератор парних чисел.
    """
    num: int = start if start % 2 == 0 else start + 1
    while True:
        yield num
        num += 2


class LimitGeneratorToFile:
    """
    Менеджер контексту для обмеження генерації чисел до певної кількості
    та запису їх у файл.
    """

    def __init__(self, generator: Iterator[int], limit: int, file_path: str) -> None:
        """
        :param generator: Генератор чисел (наприклад, нескінченний).
        :param limit: Максимальна кількість значень для генерації.
        :param file_path: Шлях до файлу для запису результатів.
        """
        self.generator = generator
        self.limit = limit
        self.file_path = file_path

    def __enter__(self) -> None:
        """
        При вході в контекст запускає генератор і записує значення у файл.
        """
        with open(self.file_path, mode='w', encoding='utf-8') as file:
            for _ in range(self.limit):
                value = next(self.generator)
                file.write(f"{value}\n")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Закриває контекст. Обробка помилок не потрібна, тому повертає None.
        """
        pass


if __name__ == "__main__":
    gen = even_number_generator()
    file_name = "task5_files/task5_even_numbers.txt"

    with LimitGeneratorToFile(gen, limit=100, file_path=file_name):
        print(f"Збережено файл: {file_name}")
