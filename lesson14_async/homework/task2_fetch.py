# Використовуючи бібліотеку aiohttp, створіть асинхронну функцію
# fetch_content(url: str), яка виконує HTTP-запит до вказаного
# URL і повертає вміст сторінки.
# Створіть асинхронну функцію fetch_all(urls: list),
# яка приймає список URL і завантажує вміст усіх сторінок паралельно.
# Використайте await та об'єднання кількох завдань (asyncio.gather()),
# щоб завантаження всіх сторінок виконувалося одночасно.
# Обробіть можливі помилки запитів, щоб у разі проблеми з підключенням
# функція повертала відповідне повідомлення про помилку.

import asyncio
from typing import List, Union
import aiohttp
from aiohttp import ClientError, ClientSession


async def fetch_content(url: str, session: ClientSession) -> Union[str, None]:
    """
    Асинхронно виконує HTTP-запит до вказаного URL і повертає вміст сторінки.

    У разі помилки повертає повідомлення про помилку.

    :param url: URL сторінки для завантаження.
    :param session: Сесія aiohttp для виконання запиту.
    :return: Вміст сторінки як рядок, або повідомлення про помилку.
    """
    try:
        async with session.get(url) as response:
            response.raise_for_status()  # помилка для статусів 4xx/5xx
            content: str = await response.text()
            print(f"[УСПІХ] Завантажено: {url}")
            return content
    except ClientError as e:
        print(f"[ПОМИЛКА] Неможливо завантажити {url}: {str(e)}")
        return None
    except asyncio.TimeoutError:
        print(f"[ПОМИЛКА] Тайм-аут при спробі завантажити {url}")
        return None
    except Exception as e:
        print(f"Невідома помилка: {e}")


async def fetch_all(urls: List[str]) -> List[Union[str, None]]:
    """
    Асинхронно завантажує вміст декількох веб-сторінок одночасно.

    :param urls: Список URL-адрес для завантаження.
    :return: Список вмісту сторінок або None для невдалих запитів.
    """
    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task] = [
            asyncio.create_task(fetch_content(url, session)) for url in urls]
        return await asyncio.gather(*tasks)


# ----------------------------------------------------
if __name__ == "__main__":
    test_urls: List[str] = [
        "https://example.com",
        "https://openai.com",
        "https://nonexistent.openai.com",  # Помилковий URL
        "https://httpstat.us/404",  # Сторінка з помилкою 404
    ]

    results = asyncio.run(fetch_all(test_urls))

    # Виведення перших 50 символів кожної відповіді (якщо є)
    for i, content in enumerate(results):
        if content:
            print(f"\n[{test_urls[i]}] Вміст (перші 50 символів):"
                  f"\n{content[:50]}...")
        else:
            print(f"\n[{test_urls[i]}] Вміст: недоступний.")
