# Завдання 7: Порівняння багатопотоковості/багатопроцесорності/асинхронності
# Реалізуйте та дослідіть виконання 500 запитів за допомогою синхронного/
# багатопотокового/багатопроцесорного/асинхронного режимів за часом.

import time
import requests
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from typing import List

NUM_REQUESTS: int = 50  # 500 - довго))
URL: str = "https://httpbin.org/delay/1"


# ---------- 1. Синхронний підхід ----------

def sync_request(url: str) -> str:
    """
    Виконує HTTP-запит синхронно за допомогою requests.

    :param url: Адреса для запиту.
    :return: Текст відповіді.
    """
    response = requests.get(url)
    return response.text


def run_sync() -> None:
    """
    Виконує NUM_REQUESTS HTTP-запитів послідовно.
    """
    print("\nСИНХРОННИЙ:")
    start: float = time.perf_counter()

    for _ in range(NUM_REQUESTS):
        sync_request(URL)

    duration: float = time.perf_counter() - start
    print(f"⏱️ Час виконання: {duration:.2f} секунд")


# ---------- 2. Багатопотоковий підхід ----------

def run_threaded() -> None:
    """
    Виконує NUM_REQUESTS HTTP-запитів паралельно в потоках.
    """
    print("\nБАГАТОПОТОКОВИЙ:")
    start: float = time.perf_counter()

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(sync_request, [URL] * NUM_REQUESTS)

    duration: float = time.perf_counter() - start
    print(f"⏱️ Час виконання: {duration:.2f} секунд")


# ---------- 3. Багатопроцесорний підхід ----------

def run_multiprocess() -> None:
    """
    Виконує NUM_REQUESTS HTTP-запитів паралельно у кількох процесах.
    """
    print("\nБАГАТОПРОЦЕСОРНИЙ:")
    start: float = time.perf_counter()

    with Pool(processes=8) as pool:
        pool.map(sync_request, [URL] * NUM_REQUESTS)

    duration: float = time.perf_counter() - start
    print(f"⏱️ Час виконання: {duration:.2f} секунд")


# ---------- 4. Асинхронний підхід ----------

async def async_request(session: aiohttp.ClientSession, url: str) -> str:
    """
    Асинхронно виконує HTTP-запит через aiohttp.

    :param session: Сесія aiohttp.
    :param url: Адреса для запиту.
    :return: Текст відповіді.
    """
    async with session.get(url) as response:
        return await response.text()


async def run_async() -> None:
    """
    Виконує NUM_REQUESTS HTTP-запитів одночасно
     за допомогою asyncio та aiohttp.
    """
    print("\nАСИНХРОННИЙ:")
    start: float = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task] = [
            asyncio.create_task(async_request(session, URL))
            for _ in range(NUM_REQUESTS)
        ]
        await asyncio.gather(*tasks)

    duration: float = time.perf_counter() - start
    print(f"⏱️ Час виконання: {duration:.2f} секунд")


# ---------- Запуск усіх режимів ----------

def main() -> None:
    """
    Запускає всі 4 реалізації та виводить час виконання кожної.
    """
    run_sync()
    run_threaded()
    run_multiprocess()
    asyncio.run(run_async())


# --------------------------------------------------------------------
if __name__ == "__main__":
    main()

# 50 запросов
# СИНХРОННИЙ:
# ⏱️ Час виконання: 223.24 секунд
#
# БАГАТОПОТОКОВИЙ:
# ⏱️ Час виконання: 6.75 секунд
#
# БАГАТОПРОЦЕСОРНИЙ:
# ⏱️ Час виконання: 12.60 секунд
#
# АСИНХРОННИЙ:
# ⏱️ Час виконання: 0.86 секунд
