# 2. Напишіть програму, яка зчитує числа з текстового файлу та обчислює їхнє середнє арифметичне.
# Обробіть такі винятки:
#   FileNotFoundError (файл не знайдено)
#   ValueError (у файлі містяться нечислові дані)
# 	Додаткове завдання: реалізуйте можливість обробки порожнього файлу та файлу, що містить лише один рядок.

from decimal import Decimal, InvalidOperation
from typing import List, Optional


def read_numbers_from_file(filename: str) -> List[Decimal]:
    """
    Зчитує числа з текстового файлу.

    Args:
        filename (str): шлях до файлу

    Returns:
        List[Decimal]: список чисел з файлу

    Raises:
        FileNotFoundError: якщо файл не знайдено
        ValueError: якщо у файлі містяться нечислові дані
        Exception: інші несподівані помилки
    """
    numbers: List[Decimal] = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()

                # Пропускаємо порожні рядки
                if not line:
                    continue

                # Розділяємо рядок на окремі елементи (пробіл, табуляція тощо)
                parts = line.split()

                for part_index, part in enumerate(parts, 1):
                    try:
                        number = Decimal(part)
                        numbers.append(number)
                    except (InvalidOperation, ValueError):
                        raise ValueError(f"Рядок {line_number}, елемент {part_index}: '{part}' не є числом")

    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не знайдено")
    except PermissionError:
        raise Exception(f"Немає дозволу на читання файлу '{filename}'")

    return numbers


def calculate_average(numbers: List[Decimal]) -> Decimal:
    """Обчислює середнє арифметичне списку чисел."""
    if not numbers:
        raise ValueError("Неможливо обчислити середнє для порожнього списку")

    total = sum(numbers)
    count = len(numbers)

    return total / count


def process_file(filename: str) -> Optional[Decimal]:
    """Обробляє файл з числами та обчислює середнє арифметичне.
    Args:
        filename (str): шлях до файлу
    """
    try:
        numbers = read_numbers_from_file(filename)

        if not numbers:
            print("Файл порожній або не містить валідних чисел")
            return None

        if len(numbers) == 1:
            print(f"Файл містить лише одне число: {numbers[0]}")
            return numbers[0]

        average = calculate_average(numbers)
        print(f"Знайдено {len(numbers)} чисел")
        print(f"Середнє арифметичне: {average}")

        return average

    except FileNotFoundError as e:
        print(f"Помилка: {e}")
        return None
    except ValueError as e:
        print(f"Помилка: {e}")
        return None
    except Exception as e:
        print(f"Несподівана помилка: {e}")
        return None


def main() -> None:
    """
    Головна функція програми.
    Запитує у користувача ім'я файлу та обробляє його.
    """
    while True:
        try:
            # filename = input("Введіть ім'я файлу (або 'q' для виходу): ").strip()
            filename = "q.txt"  # просто для спрощення, або взяти строку вище для ввода файла
            if filename.lower() == 'q':
                print("До побачення!")
                break

            if not filename:
                print("Введіть коректне ім'я файлу")
                continue

            process_file(filename)

            # Пропонуємо спробувати ще раз
            retry = input("\nСпробувати з іншим файлом? (y/n): ").strip().lower()
            if retry not in ['y', 'yes', 'так', 'т']:
                break

        except KeyboardInterrupt:
            print("\nПрограму перервано користувачем")
            break
        except Exception as e:
            print(f"Несподівана помилка в головній функції: {e}")


if __name__ == "__main__":
    main()

# Варианты обработки файла
# parts = ["10.5", "20.3", "abc", "15.7"]
#
# # Без enumerate - только элементы
# for part in parts:
#     print(part)
# # Выведет: 10.5, 20.3, abc, 15.7
#
# # С enumerate(parts, 1) - индекс + элемент
# for part_index, part in enumerate(parts, 1):
#     print(f"Элемент {part_index}: {part}")
# # Выведет:
# # Элемент 1: 10.5
# # Элемент 2: 20.3
# # Элемент 3: abc
# # Элемент 4: 15.7
