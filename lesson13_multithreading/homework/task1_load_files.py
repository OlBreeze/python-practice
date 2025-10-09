# Задача 1: завантаження файлів із мережі
# Створіть програму, яка завантажує кілька файлів із мережі
# одночасно за допомогою потоків. Ваша програма повинна
# використовувати модуль threading для створення декількох потоків,
# кожен з яких відповідає за завантаження окремого файлу.
#
# Підказка:
# використайте бібліотеки requests або urllib для завантаження файлів.

from concurrent.futures import ThreadPoolExecutor
import requests
from typing import Dict


def download_file(url: str, filename: str) -> None:
    """
    Завантажує файл із заданої URL-адреси та зберігає його під вказаним ім’ям.

    Parameters:
        url (str): Посилання на файл для завантаження.
        filename (str): Ім’я, під яким зберігатиметься файл локально.

    Returns:
        None
    """
    try:
        print(f"Завантажую {filename} ...")
        response = requests.get(url, timeout=10)  # надсилаємо HTTP GET-запит
        # викликає помилку, якщо статус 4xx або 5xx:
        response.raise_for_status()

        # записуємо вміст відповіді у файл
        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"{filename} готово!")
    except requests.exceptions.RequestException as e:
        print(f"Не вдалося завантажити {filename}: {e}")


# Словник: URL-адрес та ім’я файлу, під яким зберегти результат
files: Dict[str, str] = {
    "https://www.w3.org/WAI/ER/resources/pdf/dummy.pdf":
        "file1.pdf",
    "https://www.learningcontainer.com/sample-text-file.txt":
        "file2.txt",
    "https://www.learningcontainer.com/sample-mp4-file.mp4":
        "file3.mp4",
    "https://example.com/notfoundfile.zip": "file4.zip"
    # notfoundfile.zip": "file4.zip"  # цей файл викличе помилку 404
}

# Використовуємо ThreadPoolExecutor для паралельного завантаження файлів
with ThreadPoolExecutor(max_workers=3) as executor:
    for url, filename in files.items():
        executor.submit(download_file, url, filename)

# Result
# Завантажую file1.pdf ...
# Завантажую file2.txt ...
# Завантажую file3.mp4 ...
# file1.pdf готово!
# Завантажую file4.zip ...
# file2.txt готово!
# Не вдалося завантажити file4.zip: 404 Client Error:
#   Not Found for url: https://example.com/notfoundfile.zip
# file3.mp4 готово!
