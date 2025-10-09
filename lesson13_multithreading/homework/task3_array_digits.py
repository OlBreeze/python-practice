# Задача 3: підрахунок суми чисел у великому масиві
# Створіть програму, яка ділить великий масив чисел на кілька частин
# і рахує суму кожної частини паралельно в різних процесах.
# Використовуйте модуль multiprocessing.

from multiprocessing import Pool, cpu_count
from typing import List
import random
import time


def chunk_sum(numbers: List[int]) -> int:
    """
    Обчислює суму елементів у підмасиві.

    Parameters:
        numbers (List[int]): Підмасив чисел.

    Returns:
        int: Сума чисел у підмасиві.
    """
    return sum(numbers)


def parallel_sum(array: List[int], num_processes: int) -> int:
    """
    Паралельно обчислює суму великого масиву чисел.

    Parameters:
        array (List[int]): Вхідний масив чисел.
        num_processes (int): Кількість процесів для обробки.

    Returns:
        int: Загальна сума всіх чисел у масиві.
    """
    # Ділимо масив на частини для кожного процесу
    chunk_size: int = len(array) // num_processes
    chunks: List[List[int]] = [array[i:i + chunk_size] for i in range(0, len(array), chunk_size)]

    # Обробка в пулі процесів
    with Pool(processes=num_processes) as pool:
        partial_sums: List[int] = pool.map(chunk_sum, chunks)
        # Функція map() виконує вказану функцію до кожного елементу ітерованого об'єкта
        # (списку, кортежу тощо) та повертає ітератор, який містить результати.

    # Повертаємо загальну суму
    return sum(partial_sums)


# --------------------------------------
if __name__ == "__main__":
    # Створюємо великий масив випадкових чисел
    N = 10_000_000  # 10 мільйонів
    big_array: List[int] = [random.randint(1, 100) for _ in range(N)]

    # Кількість процесів (можна вручну або cpu_count())
    processes = cpu_count()

    print(f"Обчислення суми {N} чисел за допомогою {processes} процесів...")

    start = time.time()
    total = parallel_sum(big_array, processes)
    end = time.time()

    print(f"Сума: {total}")
    print(f"Час виконання: {end - start:.2f} секунд")

# chunk_size = 10_000_000 // 4 = 2_500_000
# chunks = [array[i:i + chunk_size] for i in range(0, 10_000_000, 2_500_000)]
# i = 0
# i = 2_500_000
# i = 5_000_000
# i = 7_500_000
# chunks — список частин, наприклад:
#
# [
#     array[0:250000],        # 1-й шматок
#     array[250000:500000],   # 2-й шматок
#     array[500000:750000],   # 3-й шматок
#     array[750000:1000000]   # 4-й шматок
# ]
