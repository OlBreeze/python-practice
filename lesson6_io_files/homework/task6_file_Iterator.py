# 6. Ітерація через файли в каталозі
# Напишіть ітератор, який буде повертати всі файли в заданому каталозі по черзі.
# Для кожного файлу виведіть його назву та розмір.

import os
from typing import Iterator, Tuple


def file_iterator(directory: str) -> Iterator[Tuple[str, int]]:
    """
    Генератор для обходу всіх файлів у заданому каталозі.

    Args:
        directory (str): шлях до каталогу.
    """
    for file_name in os.listdir(directory):
        file_path: str = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            file_size: int = os.path.getsize(file_path)
            yield file_name, file_size  # yield: Tuple[str, int]: кортеж (ім'я файлу, розмір у байтах).


if __name__ == "__main__":
    folder = "."  # поточний каталог
    for name, size in file_iterator(folder):
        print(f"{name}: {size} байт")
