# Завантаження зображень з декількох сайтів
# Уявімо, що ми розробляємо веб-скрапер, який має завантажити зображення з
# декількох сайтів одночасно. Кожне завантаження зображення - це окрема
# операція введення-виводу, яка може зайняти певний час.
#
# Створити асинхронну функцію download_image, яка приймає URL зображення та
# ім'я файлу для збереження. Вона використовуватиме aiohttp для виконання
# HTTP-запиту та збереження отриманих даних у файл.
#
# Головна асинхронна функція main створює список завдань (tasks), кожне з
# яких відповідає за завантаження одного зображення. Функція asyncio.gather
# дозволяє запускати всі завдання одночасно і очікувати їх завершення.

import asyncio
import aiohttp
from aiohttp import ClientSession, ClientError
from typing import List, Tuple
from pathlib import Path

# Семафор для обмеження одночасних завантажень
semaphore = asyncio.Semaphore(3)


async def download_image(session: ClientSession,
                         url: str,
                         filename: str) -> None:
    """
    Завантажує зображення з вказаного URL та зберігає його у файл.
    Використовує семафор для обмеження кількості одночасних завантажень.

    :param session: Сесія aiohttp.
    :param url: URL зображення.
    :param filename: Локальний шлях для збереження файлу.
    """
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                image_data: bytes = await response.read()
                with open(filename, "wb") as f:
                    f.write(image_data)
                print(f"✅ Завантажено: {filename}")
        except ClientError as e:
            print(f"❌ Помилка при завантаженні {url}: {e}")
        except Exception as e:
            print(f"❌ Неочікувана помилка з {url}: {e}")


async def main(image_list: List[Tuple[str, str]]) -> None:
    """
    Запускає асинхронне завантаження всіх зображень

    :param image_list: Список кортежів (url, filename).
    """
    async with aiohttp.ClientSession() as session:
        tasks: List[asyncio.Task] = [
            asyncio.create_task(download_image(session, url, filename))
            for url, filename in image_list
        ]
        await asyncio.gather(*tasks)
    #     # Прогрес-бар з tqdm
    #     for task in tqdm(asyncio.as_completed(tasks),
    #       total=len(tasks), desc="Завантаження"):
    #         await task


# --------------------------------------------------------------------------------
if __name__ == "__main__":
    images_to_download: List[Tuple[str, str]] = [
        (
            "https://list-kalendarya.ru/image/prikol/zavtra-rabota(1).jpg",
            "img1.jpg",
        ),
        (
            "https://cdn.humoraf.ru/wp-content/uploads/2017/07/22-12.jpg",
            "img2.jpg",
        ),
        (
            "https://encrypted-tbn0.gstatic.com/"
            "images?q=tbn:ANd9GcTb41_DhTxr8aSAa4iojpLhnWGG5pXYRLGWPQ&s",
            "img3.jpg",
        ),
        (
            "https://klike.net/uploads/posts/2019-05/1557043030_3.jpg",
            "img4.jpg",
        ),
    ]

    Path("downloads").mkdir(exist_ok=True)
    images_to_download = [(url, f"downloads/{filename}")
                          for url, filename in images_to_download]

    asyncio.run(main(images_to_download))
