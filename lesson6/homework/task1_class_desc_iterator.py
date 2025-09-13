# 1. Створення власного ітератора для зворотного читання файлу
# Напишіть власний ітератор, який буде зчитувати файл у зворотному порядку — рядок за рядком з кінця файлу до початку.
# Це може бути корисно для аналізу лог-файлів, коли останні записи найважливіші.
from typing import Iterator


class ReverseFileReader:
    """
    Ітератор для зворотного читання файлу у текстовому режимі.
    """

    def __init__(self, filename: str, encoding: str = 'utf-8') -> None:
        self.filename = filename
        self.encoding = encoding

    def __iter__(self) -> Iterator[str]:
        """
        Зчитує файл повністю в пам'ять і повертає рядки у зворотному порядку.
        """
        try:
            with open(self.filename, 'r', encoding=self.encoding) as file:
                lines = file.readlines()
            for line in reversed(lines):
                yield line.rstrip('\n')
        except FileNotFoundError:
            print(f"Файл '{self.filename}' не знайдено.")
        except Exception as e:
            print(f"Сталася помилка при читанні файлу: {e}")


# ------------------------
reader = ReverseFileReader("task1.txt")
for line in reader:
    print(line)
