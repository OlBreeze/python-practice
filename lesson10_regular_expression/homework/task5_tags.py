# Завдання 5. Видалення HTML-тегів
# Напишіть функцію, яка видаляє всі HTML-теги з тексту.

import re


def remove_html_tags(text: str) -> str:
    """
    Видаляє всі HTML-теги з тексту.
    """
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text


html = "<p>Сайт: <a href='https://example.com'>Example</a></p>"
print(remove_html_tags(html))

# 2v ----------------
#  from html.parser import HTMLParser
