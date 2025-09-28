# Завдання 9. Аналіз даних (опціонально)
# Напишіть програму, яка аналізує лог-файл веб-сервера та виводить статистику
# за кількістю запитів з різних IP-адрес.
import re
from collections import defaultdict


def analyze_log_file(file_path: str) -> dict[str, int]:
    """
    Аналізує лог-файл веб-сервера та підраховує кількість запитів з різних IP-адрес.

    Параметри:
    ----------
    file_path : str
        Шлях до лог-файлу, який потрібно проаналізувати.

    Повертає:
    ----------
    dict[str, int]
        Словник, де ключі — IP-адреси, а значення — кількість запитів від цієї IP-адреси.
        Наприклад: {'192.168.0.1': 12, '10.0.0.5': 7}
    """
    ip_pattern = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}')
    ip_counts = defaultdict(int)  # key, value => ip, count
    # defaultdict — це майже те саме, що звичайний dict,
    # але якщо ти звертаєшся до ключа, якого ще нема,
    # він створює його автоматично із типовим значенням, яке ти задаєш.
    # У випадку defaultdict(int), типове значення — це 0,
    # тому що int() повертає 0.
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                # parts = line.split() # якщо лог файл починаеться з IP адреси
                # if parts:
                #     ip = parts[0]
                #     ip_counts[ip] += 1

                match = ip_pattern.match(line)
                if match:
                    ip = match.group()
                    ip_counts[ip] += 1

        print("Статистика запитів за IP-адресами:\n")

        # sorted(..., key=lambda x: x[1], reverse=True) : сортируеm эти пары по
        # второму элементу кортежа, то есть по количеству запросов (а не по IP)
        for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{ip}: {count} запитів")

    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


log_file_path = "access.log"
analyze_log_file(log_file_path)
#
# Статистика запитів за IP-адресами:
#
# 127.0.0.1: 5 запитів
# 127.0.3.1: 1 запитів
# 127.127.0.1: 1 запитів


# --------------------
# Як порахувати кількість рядків?
# with open('access.log', 'r') as f:
#     total_lines = sum(1 for _ in f)
#
# print(f"Всього рядків у файлі: {total_lines}")
