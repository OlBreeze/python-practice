# 3. Збір статистики про зображення
# У вас є каталог з великою кількістю зображень.
# Напишіть ітератор, який по черзі відкриває кожне зображення
# (наприклад, за допомогою модуля PIL), витягує з нього метадані (розмір, формат тощо)
# і зберігає ці дані у файл CSV.

import os
import csv
from typing import Iterator, Optional
from PIL import Image


class ImageMetadataCollector:
    """
    Ітератор для збору метаданих про зображення у вказаному каталозі
    та збереження їх у CSV-файл.

    Метадані: ім'я файлу, формат, ширина, висота.
    """

    SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

    def __init__(self, directory: str, csv_file: str) -> None:
        """
        Ініціалізує збирач метаданих.

        :param directory: Шлях до каталогу з зображеннями.
        :param csv_file: Шлях до CSV-файлу для запису результатів.
        """
        self.directory = directory
        self.csv_file = csv_file
        self.files = [
            f for f in os.listdir(directory)
            if f.lower().endswith(self.SUPPORTED_EXTENSIONS)
        ]
        self.index = 0

        # Відкриваємо CSV і пишемо заголовки
        with open(self.csv_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['filename', 'format', 'width', 'height'])

    def __iter__(self) -> Iterator[Optional[dict]]:
        return self

    def __next__(self) -> dict:
        """
        Відкриває наступне зображення, збирає метадані та записує в CSV.

        :return: Словник з метаданими.
        :raises StopIteration: Якщо всі файли оброблені.
        """
        if self.index >= len(self.files):
            raise StopIteration

        filename = self.files[self.index]
        self.index += 1

        filepath = os.path.join(self.directory, filename)
        try:
            with Image.open(filepath) as img:
                img_format = img.format or 'Unknown'
                width, height = img.size
        except Exception as e:
            # Якщо не вдалося відкрити файл, повернемо метадані з помилкою
            img_format = 'Error'
            width = height = 0

        # Запис у CSV
        with open(self.csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([filename, img_format, width, height])

        return {
            'filename': filename,
            'format': img_format,
            'width': width,
            'height': height,
        }


collector = ImageMetadataCollector('imgs/', 'imgs/task3_metadata.csv')
for item in collector:
    print(item)
