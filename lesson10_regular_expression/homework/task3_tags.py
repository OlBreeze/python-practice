# Завдання 3. Видобування хеш-тегів з тексту
# Напишіть функцію, яка з тексту повертає список хеш-тегів.
# Хеш-тег — це слово, що починається з #, і може включати лише букви та цифри.
import re
from typing import List


def extract_hashtags(text: str) -> List[str]:
    """
    Повертає список хештегів із тексту.

    :param text: Вхідний текст
    :return: List[str]: Список знайдених хештегів
    """
    #  \w+ — одна або більше символів: (a-z, A-Z), цифри (0–9) і підкр _
    pattern = r'#\w+'
    return re.findall(pattern, text)


text = """Сьогодні я вчу #Python, #100DaysOfCode і
    читаю про #AI_технології!zscdasf #fefvsdgvs RRRRR"""
hashtags = extract_hashtags(text)

print(hashtags)
