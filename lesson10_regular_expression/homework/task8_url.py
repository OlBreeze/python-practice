# Завдання 8. Вилучення даних
# Напишіть функцію, яка вилучає всі URL з заданого тексту.

import re


def extract_urls(text: str) -> list[str]:
    """
    Вилучає всі URL-адреси з переданого тексту.

    Функція шукає всі входження рядків, які починаються з http:// або https://
    та містять будь-які непробільні символи після цього.

    Args:
        text (str): Вхідний текст, у якому необхідно знайти URL-адреси.

    Returns:
        List[str]: Список знайдених URL-адрес. Якщо нічого не знайдено,
                   повертається порожній список.
    """

    # http или https + :// + непробельные символы
    pattern = r"https?://[^\s]+"
    return re.findall(pattern, text)


text = """
всафсавмсфыhttps://www.google.com мфымфысы:
- https://www.google.com
- http://example.org/test   явпиыпчривр
ч ви пыкиыпиывипыпиыпи.
"""

urls = extract_urls(text)
print(urls)
