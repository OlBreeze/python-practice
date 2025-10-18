# Скрипт повинен почати з першої сторінки (http://books.toscrape.com/).Скрипт повинен обійти всі сторінки каталогу (до 50 сторінок). 🚀Для кожної книги на кожній сторінці необхідно зібрати такі дані:
# * Назва книги (Title).
# * Ціна (Price, у фунтах стерлінгів).
# * Рейтинг (Rating, у вигляді слів, наприклад, "Three", "Five").
# * Наявність на складі (Availability – просто перевірка, чи присутній текст "In stock").

from bs4 import BeautifulSoup
import requests
import time
import csv


def scrape_books_catalog(max_pages=5):
    """
    Парсит каталог книг с сайта books.toscrape.com

    Args:
        max_pages: максимальное количество страниц для обработки (до 50)

    Returns:
        list: список словарей с данными о книгах
    """
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    print("🚀 Начинаем парсинг каталога книг...\n")

    for page_num in range(1, max_pages + 1):
        url = base_url.format(page_num)

        try:
            print(f"📄 Обработка страницы {page_num}...")
            response = requests.get(url)

            # Если страница не найдена, останавливаемся
            if response.status_code == 404:
                print(f"✅ Достигнут конец каталога на странице {page_num - 1}")
                break

            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Находим все книги на странице
            books = soup.find_all('article', class_='product_pod')

            if not books:
                print(f"⚠️ Книги не найдены на странице {page_num}")
                break

            # Парсим данные каждой книги
            for book in books:
                # Название книги
                title = book.h3.a['title']

                # Цена (убираем символ £ и все нечисловые символы кроме точки)
                price_text = book.find('p', class_='price_color').text
                # Удаляем все символы кроме цифр и точки
                price = ''.join(char for char in price_text if char.isdigit() or char == '.')
                price = price.strip()

                # Рейтинг (извлекаем второй класс, например "Three")
                rating_class = book.find('p', class_='star-rating')
                rating = rating_class['class'][1]  # ['star-rating', 'Three']

                # Наличие на складе
                availability_tag = book.find('p', class_='instock availability')
                availability = availability_tag.text.strip()
                in_stock = "In stock" in availability

                # Добавляем данные книги
                book_data = {
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Availability': 'In stock' if in_stock else 'Out of stock'
                }

                all_books.append(book_data)

            print(f"   ✓ Найдено {len(books)} книг на странице {page_num}")

            # Задержка между запросами (вежливость к серверу)
            time.sleep(0.5)

        except requests.RequestException as e:
            print(f"❌ Ошибка при запросе страницы {page_num}: {e}")
            break

    return all_books


def save_to_csv(books, filename='books_catalog.csv'):
    """
    Сохраняет данные о книгах в CSV файл

    Args:
        books: список словарей с данными о книгах
        filename: имя файла для сохранения
    """
    if not books:
        print("⚠️ Нет данных для сохранения")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Title', 'Price', 'Rating', 'Availability']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(books)

    print(f"\n💾 Данные сохранены в файл: {filename}")


def print_statistics(books):
    """Выводит статистику по собранным данным"""
    if not books:
        return

    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)

    print(f"📚 Всего книг собрано: {len(books)}")

    # Статистика по рейтингам
    ratings = {}
    for book in books:
        rating = book['Rating']
        ratings[rating] = ratings.get(rating, 0) + 1

    print("\n⭐ Распределение по рейтингам:")
    rating_order = ['One', 'Two', 'Three', 'Four', 'Five']
    for rating in rating_order:
        count = ratings.get(rating, 0)
        if count > 0:
            print(f"   {rating}: {count} книг")

    # Статистика по наличию
    in_stock_count = sum(1 for book in books if book['Availability'] == 'In stock')
    print(f"\n📦 В наличии: {in_stock_count} из {len(books)} книг")

    # Средняя цена
    prices = [float(book['Price']) for book in books]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)

    print(f"\n💰 Ценовая статистика:")
    print(f"   Средняя цена: £{avg_price:.2f}")
    print(f"   Минимальная цена: £{min_price:.2f}")
    print(f"   Максимальная цена: £{max_price:.2f}")

    # Примеры книг
    print(f"\n📖 Примеры собранных книг (первые 5):")
    for i, book in enumerate(books[:5], 1):
        print(f"\n   {i}. {book['Title'][:50]}...")
        print(f"      Цена: £{book['Price']} | Рейтинг: {book['Rating']} | {book['Availability']}")


def main():
    """Основная функция"""
    print("=" * 60)
    print("  ПАРСЕР КАТАЛОГА КНИГ - books.toscrape.com")
    print("=" * 60)
    print()

    # Запускаем парсинг (максимум 50 страниц)
    books = scrape_books_catalog(max_pages=50)

    # Выводим статистику
    print_statistics(books)

    # Сохраняем в CSV
    save_to_csv(books)

    print("\n✅ Парсинг успешно завершен!")
    print("=" * 60)


if __name__ == "__main__":
    main()