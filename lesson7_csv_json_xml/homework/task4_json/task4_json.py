# Напиши програму, яка: Завантажує JSON-файл.
# Виводить список доступних книг (наявність True).
# Додає нову книгу в цей файл.
import json
from typing import List, Dict
import os


def create_json_file(filename: str = "books.json") -> None:
    """
    Створює JSON файл з початковими книгами, якщо його немає.
    """
    if not os.path.exists(filename):
        initial_books = [
            {"назва": "Кобзар", "автор": "Тарас Шевченко", "рік": 1840, "наявність": True},
            {"назва": "Лісова пісня", "автор": "Леся Українка", "рік": 1911, "наявність": False},
            {"назва": "Тіні забутих предків", "автор": "Михайло Коцюбинський", "рік": 1913, "наявність": True},
        ]

        with open(filename, "w", encoding="utf-8") as jsonfile:
            json.dump(initial_books, jsonfile, ensure_ascii=False, indent=2)
        print(f"Створено файл {filename} з початковими книгами")


def add_book_to_json(title: str, author: str, year: int, available: bool = True, filename: str = "books.json") -> None:
    """
    Додає нову книгу до існуючого JSON файлу.
    """
    # Завантажуємо існуючі книги
    books = read_json(filename)

    # Додаємо нову книгу
    new_book = {"назва": title, "автор": author, "рік": year, "наявність": available}
    books.append(new_book)

    # Зберігаємо оновлений список
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(books, jsonfile, ensure_ascii=False, indent=2)

    status = "доступна" if available else "недоступна"
    print(f"Додано книгу '{title}' від {author} ({status}) до {filename}")


def read_json(filename: str = "books.json") -> List[Dict[str, any]]:
    """
    Читає дані з JSON файлу та повертає список книг.
    """
    try:
        with open(filename, "r", encoding="utf-8") as jsonfile:
            books_data = json.load(jsonfile)
            return books_data
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
        return []
    except json.JSONDecodeError as e:
        print(f"Помилка читання JSON файлу: {e}")
        return []


def get_available_books(filename: str = "books.json") -> List[Dict[str, any]]:
    """
    Повертає список доступних книг (наявність True).

    Args:
        filename (str): Ім'я файлу. За замовчуванням "books.json"

    Returns:
        List[Dict[str, any]]: Список доступних книг
    """
    books = read_json(filename)
    available_books = [book for book in books if book["наявність"]]
    return available_books


def display_all_books(filename: str = "books.json") -> None:
    """
    Виводить інформацію про всі книги.
    """
    books = read_json(filename)
    if books:
        print("\nВсі книги в бібліотеці:")
        print(f"{'Назва':<25} {'Автор':<20} {'Рік':<6} {'Статус':<12}")
        print("-" * 70)
        for book in books:
            status = "✓ Доступна" if book["наявність"] else "✗ Недоступна"
            print(f"{book['назва']:<25} {book['автор']:<20} {book['рік']:<6} {status:<12}")
        print("-" * 70)
    else:
        print("Бібліотека порожня або файл не знайдено")


def display_available_books(filename: str = "books.json") -> None:
    """
    Виводить інформацію про доступні книги.
    """
    available_books = get_available_books(filename)

    if available_books:
        print(f"\nДоступні книги ({len(available_books)} шт.):")
        print(f"{'Назва':<25} {'Автор':<20} {'Рік':<6}")
        print("-" * 55)
        for book in available_books:
            print(f"{book['назва']:<25} {book['автор']:<20} {book['рік']:<6}")
        print("-" * 55)
    else:
        print("Немає доступних книг у бібліотеці")


def main() -> None:
    """
    Головна функція для демонстрації роботи з JSON файлами та бібліотекою книг.
    """
    filename = "books.json"

    # Створюємо файл з початковими книгами, якщо його немає
    create_json_file(filename)

    # Завантажуємо JSON файл та показуємо всі книги
    print("\nЗавантажуємо JSON файл:")
    display_all_books(filename)

    # Додаємо нові книги
    print("\nДодаємо нові книги:")
    books_to_add = [
        ("Маруся Чурай", "Ліна Костенко", 1979, True),
        ("Слово о полку Ігоревім", "Невідомий автор", 1185, False)
    ]

    for title, author, year, available in books_to_add:
        add_book_to_json(title, author, year, available, filename)

    print("\nДоступні книги після додавання:")
    display_available_books(filename)

    available_count = len(get_available_books(filename))
    print(f"Доступних книг: {available_count}")


if __name__ == "__main__":
    main()
