# Багатопотокова програма для підрахунку слів у файлі

import threading
import time
from collections import Counter
from pathlib import Path


class WordCounterThread(threading.Thread):
    """Потік для підрахунку слів у частині файлу"""

    def __init__(self, thread_id, lines, result_dict, lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.lines = lines
        self.result_dict = result_dict
        self.lock = lock

    def run(self):
        """Виконання підрахунку слів"""
        print(f"Потік {self.thread_id} починає роботу...")
        word_count = Counter()

        # Підрахунок слів у своїй частині
        for line in self.lines:
            words = line.strip().split()
            for word in words:
                # Очищення від розділових знаків
                clean_word = word.strip('.,!?;:()[]{}"\'-').lower()
                if clean_word:
                    word_count[clean_word] += 1

        # Безпечне додавання результатів
        with self.lock:
            for word, count in word_count.items():
                self.result_dict[word] = self.result_dict.get(word, 0) + count

        print(f"Потік {self.thread_id} завершив роботу")


def read_file_multithreaded(filename, num_threads=4):
    """
    Читає файл і підраховує слова використовуючи кілька потоків

    Args:
        filename: шлях до файлу
        num_threads: кількість потоків
    """
    start_time = time.time()

    # Читання файлу
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено!")
        return

    total_lines = len(lines)
    print(f"Прочитано {total_lines} рядків")

    # Розділення на частини
    chunk_size = total_lines // num_threads
    threads = []
    result_dict = {}
    lock = threading.Lock()

    # Створення потоків
    for i in range(num_threads):
        start_idx = i * chunk_size

        # Останній потік обробляє всі залишкові рядки
        if i == num_threads - 1:
            end_idx = total_lines
        else:
            end_idx = start_idx + chunk_size

        thread_lines = lines[start_idx:end_idx]
        thread = WordCounterThread(i + 1, thread_lines, result_dict, lock)
        threads.append(thread)
        thread.start()

    # Очікування завершення всіх потоків
    for thread in threads:
        thread.join()

    end_time = time.time()

    # Виведення результатів
    print("\n" + "=" * 50)
    print(f"Загальна кількість унікальних слів: {len(result_dict)}")
    print(f"Загальна кількість слів: {sum(result_dict.values())}")
    print(f"Час виконання: {end_time - start_time:.2f} секунд")
    print("=" * 50)

    # Топ-10 найчастіших слів
    print("\nТоп-10 найчастіших слів:")
    sorted_words = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")

    return result_dict


def create_test_file(filename="test.txt", num_lines=1000):
    """Створює тестовий файл"""
    words = ["Python", "програмування", "потік", "файл", "дані",
             "код", "функція", "клас", "метод", "змінна"]

    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            line = " ".join([words[i % len(words)] for _ in range(10)])
            f.write(line + "\n")

    print(f"Створено тестовий файл: {filename}")


if __name__ == "__main__":
    # Створення тестового файлу (опціонально)
    create_test_file("test.txt", 1000)

    # Запуск багатопотокового підрахунку
    print("\nБагатопотоковий підрахунок:")
    read_file_multithreaded("test.txt", num_threads=4)