# Завдання 5. Видалення HTML-тегів
# Напишіть функцію, яка видаляє всі HTML-теги з тексту.

import re


def remove_html_tags(text: str) -> str:
    """
        Видаляє всі HTML-теги з переданого рядка.

        Функція знаходить усі підрядки, що починаються з символа '<'
        і закінчуються символом '>', та видаляє їх.

        Args:
            text (str): Вхідний рядок, який може містити HTML-теги.

        Returns:
            str: Рядок без HTML-тегів.

        Приклади:
            >>> remove_html_tags("<p>Hello <b>World</b></p>")
            'Hello World'

            >>> remove_html_tags("No tags here")
            'No tags here'
    """
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text


html = "<p>Сайт: <a href='https://example.com'>Example</a></p>"
print(remove_html_tags(html))

# 2v ----------------
#  from html.parser import HTMLParser
