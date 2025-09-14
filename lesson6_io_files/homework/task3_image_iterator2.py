# 3. Збір статистики про зображення
# У вас є каталог з великою кількістю зображень.
# Напишіть ітератор, який по черзі відкриває кожне зображення
# (наприклад, за допомогою модуля PIL), витягує з нього метадані (розмір, формат тощо)
# і зберігає ці дані у файл CSV.
import os
import csv
from typing import Iterator, Dict
from PIL import Image


def collect_image_metadata(directory: str, csv_file: str) -> Iterator[Dict[str, str | int]]:
    """
    Генератор, який обходить усі зображення в каталозі, збирає метадані та зберігає їх у CSV.

    :param directory: Шлях до каталогу з зображеннями.
    :param csv_file: Шлях до CSV-файлу для запису результатів.
    """
    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    files = [f for f in os.listdir(directory) if f.lower().endswith(supported_ext)]

    # створюємо CSV із заголовками
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['filename', 'format', 'width', 'height'])

    for filename in files:
        filepath = os.path.join(directory, filename)
        try:
            with Image.open(filepath) as img:
                img_format = img.format or 'Unknown'
                width, height = img.size
        except Exception:
            img_format = 'Error'
            width = height = 0

        # дозапис у CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([filename, img_format, width, height])

        # yield: Словник з метаданими (filename, format, width, height).
        yield {
            'filename': filename,
            'format': img_format,
            'width': width,
            'height': height,
        }


# Використання:
for item in collect_image_metadata('imgs/', 'imgs/task3_metadata2.csv'):
    print(item)
