# Задача 5: паралельний пошук у файлах
# Реалізуйте програму, яка шукає певний текст у кількох
# великих файлах одночасно, використовуючи потоки або процеси.
# Для кожного файлу створіть окремий потік або процес.
# <- threading ->

import threading
from typing import List


def search_in_file(filename: str, keyword: str) -> None:
    """
    Шукає задане слово в файлі та виводить результат.

    :param filename: шлях до файлу
    :param keyword: слово або фраза для пошуку
    """
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            print(f"\nПошук у файлі: {filename}")
            for line_number, line in enumerate(file, 1):
                if keyword in line:
                    print(f"Знайдено в {filename} (рядок {line_number})")
                    return
            print(f"'{keyword}' не знайдено в {filename}")
    except FileNotFoundError:
        print(f"Файл не знайдено: {filename}")
    except Exception as e:
        print(f"Помилка при обробці {filename}: {e}")


def parallel_search(filenames: List[str], keyword: str) -> None:
    """
    Запускає пошук у кількох файлах одночасно.

    :param filenames: список шляхів до файлів
    :param keyword: слово або фраза для пошуку
    """
    threads: List[threading.Thread] = []

    for filename in filenames:
        thread = threading.Thread(target=search_in_file,
                                  args=(filename, keyword))  # Створює окремий потік для кожного файлу.
        thread.start()
        threads.append(thread)
        # thread.join() Запускается первый поток.
        # Программа сразу ждёт, пока он закончит. Только после этого запускается второй поток. Неправильно

    # Очікуємо завершення всіх потоків
    # Все потоки запускаются почти одновременно.
    # Программа не ждёт каждый поток сразу, а переходит к следующему.
    # В конце — ждёт завершения всех потоков.
    for thread in threads:
        thread.join()

    print("Пошук завершено.")


# === Точка входу ===
if __name__ == "__main__":
    files_to_search = [
        "text1.txt",
        "text2.txt"
        # "text3.txt",
        # "text4.txt"
    ]
    keyword_to_find = "переворачивает"  # !!

    parallel_search(files_to_search, keyword_to_find)
