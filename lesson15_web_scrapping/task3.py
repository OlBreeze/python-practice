# Скрипт повинен почати з першої сторінки (http://books.toscrape.com/).
# Скрипт повинен обійти всі сторінки каталогу (до 50 сторінок). 🚀
# Для кожної книги на кожній сторінці необхідно зібрати такі дані:
# Назва книги (Title).
# Ціна (Price, у фунтах стерлінгів).
# Рейтинг (Rating, у вигляді слів, наприклад, "Three", "Five").
# Наявність на складі (Availability – просто перевірка, чи присутній текст "In stock").
# Зберігання Результатів:
# Зібрані дані мають бути збережені у форматі CSV (Comma Separated Values) або Excel.
# Кожен рядок у файлі повинен відповідати одній книзі.
# Файл повинен мати чіткі заголовки стовпців: Назва, Ціна, Рейтинг, Наявність.
# Вимоги до Реалізації та Кроки
# HTTP-Запит (requests):
# Створіть функцію, яка приймає URL і повертає об'єкт HTML-відповіді.
# Обробіть можливі помилки запиту (наприклад, коди 404, 500) за допомогою конструкції try...except.
# Парсинг HTML (BeautifulSoup):
# Створіть функцію, яка приймає HTML-контент і парсить його, знаходячи всі елементи книг.
# Для кожного елемента книги використовуйте методи find() або select_one() для вилучення необхідних даних:
# Назва: зазвичай знаходиться в тегу <h3> або посиланням <a> всередині.
# Ціна: використовуйте відповідний CSS-клас, наприклад, .price_color.
# Рейтинг: шукайте клас, що починається з star-rating, наприклад, class="star-rating Three".
# Навігація:
# Реалізуйте логіку для переходу до наступної сторінки, шукаючи посилання з текстом "next" або відповідним CSS-класом у нижній частині поточної сторінки.
# Очищення Даних (Data Cleaning):
# Ціна: Приберіть символ валюти (наприклад, £) та перетворіть значення на числове (float).
# Наявність: Перетворіть текстове значення на булеве (True/False або Так/Ні).
# Рейтинг: Виділіть саме слово-рейтинг (наприклад, Three).
# Очікуваний Результат
# Файл, наприклад, books_data.csv, що містить сотні рядків (по одній книзі) з чітко структурованими даними.
# НазваﾠЦінаﾠРейтингﾠНаявність
# A Light in the Atticﾠ51.77ﾠThreeﾠTrue
# Tipping the Velvetﾠ53.74ﾠOneﾠTrue
# ...ﾠ...ﾠ...ﾠ...
# The Secret Gardenﾠ15.00ﾠTwoﾠTrue


import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_books(url, max_pages=5):
    """
    Скрейпер для збору інформації про книги

    Args:
        url: URL сторінки для парсингу
        max_pages: максимальна кількість сторінок для обробки
    """
    all_books = []

    for page in range(1, max_pages + 1):
        print(f"Обробка сторінки {page}...")

        # Формуємо URL з номером сторінки
        page_url = f"{url}catalogue/page-{page}.html"

        try:
            # Відправляємо запит
            response = requests.get(page_url)
            response.raise_for_status()

            # Парсимо HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Знаходимо всі книги на сторінці
            books = soup.find_all('article', class_='product_pod')

            for book in books:
                # Витягуємо дані
                title = book.h3.a['title']
                price_text = book.find('p', class_='price_color').text
                price = ''.join(char for char in price_text if char.isdigit() or char == '.')
                price = price.strip()
                availability = "In stock" in book.find('p', class_='instock availability').text

                # Рейтинг (перетворюємо текстовий у числовий)
                rating_class = book.find('p', class_='star-rating')['class'][1]
                # rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                # rating = rating_map.get(rating_class, 0)

                all_books.append({
                    'назва': title,
                    'ціна': price,
                    'наявність': availability,
                    'рейтинг': rating_class
                })

            print(f"Знайдено {len(books)} книг на сторінці {page}")

            # Додаємо затримку між запитами
            time.sleep(1)

        except requests.RequestException as e:
            print(f"Помилка при запиті сторінки {page}: {e}")
            break

    return all_books


def save_to_csv(books, filename='books.csv'):
    """Зберігає дані в CSV файл"""
    if not books:
        print("Немає даних для збереження")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    print(f"Дані збережено у {filename}")


def main():
    # URL демо-сайту для практики scraping
    base_url = "http://books.toscrape.com/"

    print("Запуск скрейпера...")
    books = scrape_books(base_url, max_pages=3)

    print(f"\nУсього зібрано книг: {len(books)}")

    # Показуємо перші 5 книг
    print("\nПриклад даних (перші 5 книг):")
    for i, book in enumerate(books[:5], 1):
        print(f"\n{i}. {book['назва']}")
        print(f"  Ціна: {book['ціна']}")
        print(f"  Рейтинг: {book['рейтинг']}")
        print(f"  Наявність: {book['наявність']}")

    # Зберігаємо в CSV
    save_to_csv(books)

if __name__ == "__main__":
    main()
#
# requests.get() - отримуємо HTML сторінки
# BeautifulSoup - парсимо HTML та витягуємо потрібні елементи
# find() і find_all() - шукаємо елементи за тегами та класами
# time.sleep(1) - затримка між запитами (важливо!)
# Обробка помилок через try/except