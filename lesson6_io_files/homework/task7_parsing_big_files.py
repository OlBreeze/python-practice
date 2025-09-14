# 7. Парсинг великих лог-файлів для аналітики
#
# Уявіть, що у вас є великий лог-файл від веб-сервера.
# Створіть генератор, який зчитує файл порціями (по рядку) і повертає тільки рядки з помилками
# (код статусу 4XX або 5XX). Запишіть ці помилки в окремий файл для подальшого аналізу.

from typing import Generator


def log_parser(file_path: str) -> Generator[str, None, None]:
    """
    Генератор для построкового читання лог-файлу та відбору рядків з помилками.

    :param file_path: шлях до лог-файлу
    """
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) < 9:
                # якщо рядок не відповідає формату — пропускаємо
                continue
            try:
                status_code = int(parts[-2])  # код статусу у звичайних access.log знаходиться перед розміром відповіді
                if 400 <= status_code < 600:
                    yield line.strip()  # yield: рядки з кодами статусу 4XX або 5XX
                    # Розбили рядок на частини.
                    # Взяли код статусу.
                    # Якщо це помилка — повернули весь рядок.
            except ValueError:
                # якщо код статусу не вдалося перетворити у число
                continue


def save_errors(input_file: str, output_file: str) -> None:
    """
    Зчитує лог-файл, знаходить рядки з помилками та записує їх у новий файл.

    :param input_file: шлях до вхідного лог-файлу
    :param output_file: шлях до вихідного файлу з помилками
    """
    with open(output_file, "w", encoding="utf-8") as out_file:
        for error_line in log_parser(input_file):
            out_file.write(error_line + "\n")


if __name__ == "__main__":
    input_log = "task7_files/access.log"
    output_log = "task7_files/errors.log"

    save_errors(input_log, output_log)
    print(f"Помилки з логів збережено у файл {output_log}")
