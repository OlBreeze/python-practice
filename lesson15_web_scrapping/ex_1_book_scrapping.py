import requests
from bs4 import BeautifulSoup
import csv
import time


def scrape_books(url, max_pages=3):
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
                price = book.find('p', class_='price_color').text
                availability = book.find('p', class_='instock availability').text.strip()

                # Рейтинг (перетворюємо текстовий у числовий)
                rating_class = book.find('p', class_='star-rating')['class'][1]
                rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
                rating = rating_map.get(rating_class, 0)

                all_books.append({
                    'назва': title,
                    'ціна': price,
                    'наявність': availability,
                    'рейтинг': rating
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
        print(f"   Ціна: {book['ціна']}")
        print(f"   Рейтинг: {book['рейтинг']}/5")
        print(f"   {book['наявність']}")

    # Зберігаємо в CSV
    save_to_csv(books)

    # Базова аналітика
    if books:
        avg_rating = sum(b['рейтинг'] for b in books) / len(books)
        print(f"\nСередній рейтинг: {avg_rating:.2f}/5")


if __name__ == "__main__":
    main()
#
# requests.get() - отримуємо HTML сторінки
# BeautifulSoup - парсимо HTML та витягуємо потрібні елементи
# find() і find_all() - шукаємо елементи за тегами та класами
# time.sleep(1) - затримка між запитами (важливо!)
# Обробка помилок через try/except