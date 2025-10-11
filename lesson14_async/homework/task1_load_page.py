# Напишіть асинхронну функцію download_page(url: str),
# яка симулює завантаження сторінки за допомогою asyncio.sleep().
# Функція повинна приймати URL та "завантажувати" сторінку
# за випадковий проміжок часу від 1 до 5 секунд.
# Після завершення завантаження, функція повинна
# вивести повідомлення з URL і часом завантаження.
# Напишіть асинхронну функцію main(urls: list),
# яка приймає список з декількох URL і завантажує їх одночасно,
# використовуючи await для паралельного виконання функції download_page().

import asyncio
import random
from typing import List


async def download_page(url: str) -> None:
    """
    Асинхронно симулює завантаження веб-сторінки.

    :param url: URL сторінки, яку потрібно "завантажити".
    :type url: str
    :return: None
    """
    print(f"Початок завантаження {url}")
    load_time: int = random.randint(1, 5)
    await asyncio.sleep(load_time)
    print(f"Завантажено {url} за {load_time} секунд")


async def main(urls: List[str]) -> None:
    """
    Асинхронно запускає завантаження декількох веб-сторінок одночасно.

    :param urls: Список URL-адрес для завантаження.
    :type urls: List[str]
    :return: None
    """
    tasks: List[asyncio.Task] = [download_page(url) for url in urls]
    await asyncio.gather(*tasks)


# -----------------------------------------
if __name__ == "__main__":
    test_urls: List[str] = [
        "https://example.com",
        "https://google.com",
        "https://openai.com",
        "https://github.com"
    ]
    asyncio.run(main(test_urls))
