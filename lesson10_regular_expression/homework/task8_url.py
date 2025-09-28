# Завдання 8. Вилучення даних
# Напишіть функцію, яка вилучає всі URL з заданого тексту.

import re


def extract_urls(text: str) -> list[str]:
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
