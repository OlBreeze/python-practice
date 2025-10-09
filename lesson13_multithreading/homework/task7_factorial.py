# Задача 7: обчислення факторіалу великих чисел
# Напишіть програму, яка обчислює факторіал великого числа
# за допомогою декількох потоків або процесів, розподіляючи обчислення між ними.

import multiprocessing
import sys
from functools import reduce
from typing import Tuple
import math
sys.set_int_max_str_digits(1000000)  # Підвищує ліміт для конвертації int -> str. обмеження - за замовчуванням 4300 цифр

def partial_factorial(start: int, end: int) -> int:
    """
    Обчислює добуток чисел у діапазоні [start, end].

    Parameters:
        start (int): Початок діапазону.
        end (int): Кінець діапазону.

    Returns:
        int: Добуток чисел у діапазоні.
    """
    result = 1
    for i in range(start, end + 1):
        result *= i
    return result


def chunk_ranges(n: int, num_chunks: int) -> list[Tuple[int, int]]:
    """
    Ділить діапазон [1, n] на приблизно рівні частини.

    Parameters:
        n (int): Кінцеве число факторіалу.
        num_chunks (int): Кількість частин/процесів.

    Returns:
        list of tuples: Список кортежів (start, end) для кожного процесу.
    """
    chunk_size = n // num_chunks
    ranges = []
    start = 1
    for i in range(num_chunks):
        end = start + chunk_size - 1
        if i == num_chunks - 1:  # Останній процес бере залишок
            end = n
        ranges.append((start, end))
        start = end + 1
    return ranges


def parallel_factorial(n: int, num_processes: int = None) -> int:
    """
    Обчислює факторіал числа n паралельно з використанням кількох процесів.

    Parameters:
        n (int): Число, факторіал якого потрібно обчислити.
        num_processes (int, optional): Кількість процесів. Якщо None, береться кількість CPU ядер.

    Returns:
        int: Факторіал числа n.
    """
    if n == 0 or n == 1:
        return 1

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()

    ranges = chunk_ranges(n, num_processes)

    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_results = pool.starmap(partial_factorial, ranges)

    # Об'єднуємо часткові добутки
    return reduce(lambda x, y: x * y, partial_results)


if __name__ == "__main__":
    import time

    n = 100000  # ВЕЛИКЕ ЧИСЛО
    print(f"Обчислення {n}! за допомогою мультипроцесингу...")

    start_time = time.time()
    result = parallel_factorial(n)
    end_time = time.time()

    print(f"Факторіал {n} обчислено (довжина результату: {len(str(result))} цифр)")
    print(f"Час виконання: {end_time - start_time:.2f} секунд")
