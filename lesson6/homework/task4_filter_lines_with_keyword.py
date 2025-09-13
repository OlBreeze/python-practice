# 4. Генератор для обробки великих файлів
# Реалізуйте генератор, який читає великий текстовий файл рядок за рядком (наприклад, лог-файл)
# і повертає лише ті рядки, що містять певне ключове слово.
# Використайте цей генератор для фільтрації файлу та запису відповідних рядків у новий файл.

from typing import Iterator


def filter_lines_with_keyword(file_path: str, keyword: str) -> Iterator[str]:
    """
    Генератор, який читає великий файл пострічково та повертає лише ті рядки, що містять задане ключове слово.

    :param file_path: Шлях до великого текстового файлу.
    :param keyword: Ключове слово для пошуку у рядках.
    :return: Ітератор рядків, які містять ключове слово.
    """
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                if keyword in line:
                    yield line
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")


def write_filtered_lines(source_file: str, destination_file: str, keyword: str) -> None:
    """
    Записує у новий файл всі рядки з вхідного файлу, які містять ключове слово.

    :param source_file: Шлях до вхідного великого файлу.
    :param destination_file: Шлях до вихідного файлу для збереження результатів.
    :param keyword: Ключове слово для пошуку у рядках.
    """
    with open(destination_file, mode='w', encoding='utf-8') as out_file:
        for line in filter_lines_with_keyword(source_file, keyword):
            out_file.write(line)


if __name__ == "__main__":
    source = 'task4_files/text4.txt'
    destination = 'task4_files/dream_only.txt'
    keyword = 'dream'

    write_filtered_lines(source, destination, keyword)
    print(f"✅ Рядки з '{keyword}' збережено у файл: {destination}")
