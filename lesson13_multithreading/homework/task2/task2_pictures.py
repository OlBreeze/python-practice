# Задача 2: паралельна обробка зображень
# Напишіть програму, яка обробляє кілька зображень одночасно
# (наприклад, змінює їх розмір або застосовує фільтр).
# Використовуйте модуль concurrent.futures і виконуйте обробку зображень у кількох процесах або потоках.
#
# Підказка: можна використовувати бібліотеку Pillow для обробки зображень.

from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageFilter
import os
from typing import List


def process_image(image_path: str, output_dir: str, size: tuple[int, int]) -> None:
    """
    Обробляє одне зображення: змінює його розмір та застосовує фільтр, після чого зберігає результат.

    Parameters:
        image_path (str): Шлях до вхідного зображення.
        output_dir (str): Каталог для збереження обробленого зображення.
        size (tuple[int, int]): Новий розмір зображення (ширина, висота).

    Returns:
        None
    """
    try:
        img = Image.open(image_path)

        # Зміна розміру
        img = img.resize(size)

        # Додатково: застосування фільтра (наприклад, розмиття)
        img = img.filter(ImageFilter.GaussianBlur(radius=2))

        # Формування імені вихідного файлу
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, f"processed_{filename}")

        # Збереження
        img.save(output_path)
        print(f"✅ Оброблено: {output_path}")
    except Exception as e:
        print(f"❌ Помилка при обробці {image_path}: {e}")


def batch_process_images(image_paths: List[str], output_dir: str, size: tuple[int, int]) -> None:
    """
    Обробляє список зображень паралельно.

    Parameters:
        image_paths (List[str]): Список шляхів до зображень.
        output_dir (str): Каталог для збереження результатів.
        size (tuple[int, int]): Новий розмір кожного зображення.

    Returns:
        None
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=3) as executor:
        for path in image_paths:
            executor.submit(process_image, path, output_dir, size)


# -------------------------------------------------------------
if __name__ == "__main__":
    # Список зображень для обробки
    image_files = [
        "images/image1.jpg",
        "images/image2.jpg",
        # "images/image3.jpeg",
        # "images/image4.png"
    ]

    # Папка для збереження результатів
    output_folder = "output"

    # Розмір до якого масштабуються зображення
    new_size = (800, 600)

    # Запуск обробки
    batch_process_images(image_files, output_folder, new_size)
