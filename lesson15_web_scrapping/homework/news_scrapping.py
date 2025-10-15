"""
Модуль для парсингу новинного сайту з підтримкою декількох сторінок.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import csv
import time
import re


def get_page(url: str) -> Optional[BeautifulSoup]:
    """
    Завантажує HTML-код сторінки за вказаною URL
     та повертає BeautifulSoup-об'єкт.

    Args:
        url: URL адреса сторінки для завантаження

    Returns:
        BeautifulSoup об'єкт або None у випадку помилки
    """
    try:
        # User-Agent маскує ваш скрипт щоб ідентифікувати ваш скрипт як
        # звичайний браузер, а не як бота.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except requests.RequestException as e:
        print(f"Помилка при завантаженні сторінки {url}: {e}")
        return None


def split_title(full_title: str) -> tuple[str, str]:
    """
    Розділяє повний заголовок на першу частину (до крапки) та повний текст.

    Args:
        full_title: Повний текст заголовка

    Returns:
        Кортеж (перше речення, повний заголовок)
    """
    # Шукаємо першу крапку, після якої йде пробіл або великий символ
    match = re.search(r'\.(\s+[А-ЯІЇЄҐA-Z]|$)', full_title)

    if match:
        # Знайдено крапку - беремо текст до неї включно
        first_sentence = full_title[:match.start() + 1].strip()
        return first_sentence, full_title
    else:
        # Крапки не знайдено - повертаємо весь заголовок
        return full_title, full_title


def parse_news(soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
    """
    Отримує soup-об'єкт сторінки та витягує всі новини.

    Args:
        soup: BeautifulSoup об'єкт HTML-сторінки
        base_url: Базова URL сайту для формування повних посилань

    Returns:
        Список словників з інформацією про новини
        Кожен словник містить ключі: title, link, date, summary
    """
    news_list = []

    try:
        # Пошук всіх блоків новин з класом 'lenta-news'
        articles = soup.find_all('article', class_='lenta-news')

        if not articles:
            print("Новини не знайдено на сторінці")
            return news_list

        for article in articles:
            news_item = {}

            # Повний заголовок (знаходиться в div class="title" > a)
            title_div = article.find('div', class_='title')
            if title_div:
                title_link = title_div.find('a', class_='article')
                full_title = title_link.get_text(strip=True) \
                    if title_link else 'Без заголовку'

                # Розділяємо заголовок на першу частину та повний текст
                short_title, full_description = split_title(full_title)

                news_item['title'] = short_title
                news_item['summary'] = full_description
            else:
                news_item['title'] = 'Без заголовку'
                news_item['summary'] = 'Опис відсутній'

            # Посилання
            link_tag = article.find('a', href=True)
            if link_tag and link_tag.get('href'):
                link = link_tag['href']
                # Якщо посилання відносне, додаємо базову URL
                if link.startswith('/'):
                    link = base_url + link
                news_item['link'] = link
            else:
                news_item['link'] = 'Посилання відсутнє'

            # Дата публікації (знаходиться в time class="date")
            date_tag = article.find('time', class_='date')
            if date_tag:
                # Шукаємо span з класом 'strana-adate'
                date_span = date_tag.find('span', class_='strana-adate')
                if date_span:
                    # Беремо текст з атрибуту data-time або з тексту
                    date_text = (date_span.get('data-time')
                                 or date_span.get_text(strip=True))
                    news_item['date'] = date_text
                else:
                    news_item['date'] = date_tag.get_text(strip=True)
            else:
                news_item['date'] = datetime.now().strftime('%Y-%m-%d')

            # Якщо є додатковий опис в div class="subtitle", додаємо його
            subtitle_div = article.find('div', class_='subtitle')
            if subtitle_div:
                subtitle_text = subtitle_div.get_text(strip=True)
                if subtitle_text:
                    # Додаємо subtitle до summary
                    news_item['summary'] = (f"{news_item['summary']}."
                                            f" {subtitle_text}")

            news_list.append(news_item)

    except Exception as e:
        print(f"Помилка при парсингу новин: {e}")

    return news_list


def parse_multiple_pages(base_url: str,
                         num_pages: int = 3) -> List[Dict[str, str]]:
    """
    Парсить декілька сторінок новин.

    Args:
        base_url: Базова URL сайту
        num_pages: Кількість сторінок для парсингу

    Returns:
        Список всіх новин з усіх сторінок
    """
    all_news = []

    for page_num in range(1, num_pages + 1):
        # Формування URL для кожної сторінки
        if page_num == 1:
            url = f"{base_url}/ukr/news/"
        else:
            url = f"{base_url}/ukr/news/page-{page_num}.html"

        print(f"\nЗавантаження сторінки {page_num}: {url}")

        soup = get_page(url)

        if soup is None:
            print(f"Пропускаємо сторінку {page_num}")
            continue

        news_data = parse_news(soup, base_url)

        if news_data:
            all_news.extend(news_data)
            print(f"Знайдено {len(news_data)} новин на сторінці {page_num}")
        else:
            print(f"Новин не знайдено на сторінці {page_num}")

        # Затримка між запитами, щоб не перевантажувати сервер
        if page_num < num_pages:
            time.sleep(1)

    return all_news


def filter_by_date(data: List[Dict[str, str]],
                   days: int = 2) -> List[Dict[str, str]]:
    """
    Фільтрує новини за останні кілька днів.

    Args:
        data: Список словників з інформацією про новини
        days: Кількість днів для фільтрації (за замовчуванням 2)

    Returns:
        Відфільтрований список новин
    """
    filtered_news = []
    cutoff_date = datetime.now() - timedelta(days=days)

    for news in data:
        try:
            # Спроба розпізнати дату у форматі YYYY-MM-DD
            news_date = datetime.strptime(news['date'], '%Y-%m-%d')
            if news_date >= cutoff_date:
                filtered_news.append(news)
        except (ValueError, KeyError):
            # Якщо дата не вдалося розпізнати, включаємо новину
            filtered_news.append(news)

    return filtered_news


def show_statistics(data: List[Dict[str, str]]) -> None:
    """
    Виводить статистичний звіт про зібрані новини.

    Args:
        data: Список словників з інформацією про новини
    """
    try:
        df = pd.DataFrame(data)

        print("\n" + "=" * 50)
        print("---> СТАТИСТИКА НОВИН <---")
        print("-" * 50)
        print(f"Загальна кількість новин: {len(df)}")

        if 'date' in df.columns:
            print("\nКількість новин по датах:")
            # .value_counts() - підрах, скільк разів зустрічається кожна дата
            date_counts = df['date'].value_counts()
            for date, count in date_counts.head(10).items():
                print(f"  {date}: {count} новин")

            # print(f"  ВСЬОГО: {date_counts.sum()} новин")

        if 'title' in df.columns:
            print("\n" + "-" * 50)
            print("Перші 10 заголовків:")
            print("-" * 50)
            for i, row in df.head(10).iterrows():
                print(f"\n{i + 1}. Заголовок: {row['title']}")
                print(f"   Опис: {row['summary']}")

        print("\n" + "*" * 100)

    except Exception as e:
        print(f"Помилка при створенні статистики: {e}")


def save_to_csv(data: List[Dict[str, str]],
                filename: str = 'news.csv') -> None:
    """
    Приймає список новин та зберігає його в CSV-файлі.

    Args:
        data: Список словників з інформацією про новини
        filename: Назва файлу для збереження (за замовчуванням 'news.csv')
    """
    try:
        if not data:
            print("Немає даних для збереження")
            return

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['title', 'link', 'date', 'summary']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(data)

        print(f"\nДані успішно збережено у файл {filename}")

    except IOError as e:
        print(f"Помилка при збереженні файлу: {e}")


def get_user_input() -> tuple[int, int]:
    """
    Отримує від користувача параметри парсингу.

    Returns:
        Кортеж (кількість сторінок, кількість днів для фільтрації)
    """
    print("\n" + "-" * 50)
    print("НАЛАШТУВАННЯ ПАРСИНГУ")
    print("-" * 50)

    # Отримання кількості сторінок
    while True:
        try:
            num_pages = input("\nСкільки сторінок парсити? "
                              "(за замовчуванням 3): ").strip()
            if num_pages == "":
                num_pages = 3
                break
            num_pages = int(num_pages)
            if num_pages > 0:
                break
            else:
                print("Будь ласка, введіть число більше 0")
        except ValueError:
            print("Будь ласка, введіть коректне число")

    # Отримання кількості днів для фільтрації
    while True:
        try:
            filter_days = input(
                "\nЗа скільки останніх днів виводити новини? "
                "(за замовчуванням 2, 0 = всі новини): ").strip()
            if filter_days == "":
                filter_days = 2
                break
            filter_days = int(filter_days)
            if filter_days >= 0:
                break
            else:
                print("Будь ласка, введіть число більше або рівне 0")
        except ValueError:
            print("Будь ласка, введіть коректне число")

    print("\n" + "-" * 50)
    print("Налаштування прийнято:")
    print(f"  - Кількість сторінок: {num_pages}")
    print(
        f"  - Фільтр по датах: "
        f"{'всі новини' if filter_days == 0 else f'останні {filter_days} '
                                                 f'днів'}"
    )

    print("~" * 50)

    return num_pages, filter_days


def main() -> None:
    """
    Головна функція для запуску скрипта парсингу новин.
    """
    # URL новинного сайту
    base_url = "https://ctrana.one"

    # Отримання параметрів від користувача
    num_pages, filter_days = get_user_input()

    print(f"ПОЧАТОК ПАРСИНГУ {num_pages} СТОРІНОК")
    print("~" * 50)

    # Парсинг декількох сторінок
    all_news = parse_multiple_pages(base_url, num_pages)

    if not all_news:
        print("\nНовини не знайдено на жодній сторінці")
        return

    print(f"\n{'-' * 50}")
    print(f"ВСЬОГО знайдено {len(all_news)} новин з {num_pages} сторінок")
    print("-" * 50)

    # Фільтрація за датою (якщо filter_days > 0)
    if filter_days > 0:
        filtered_news = filter_by_date(all_news, days=filter_days)
        print(f"\nНовин за останні {filter_days} днів: {len(filtered_news)}")

        # Зберігаємо відфільтровані новини
        if filtered_news:
            save_to_csv(filtered_news, filename='result.csv')
            show_statistics(filtered_news)
        else:
            print(f"\nНемає новин за останні {filter_days} днів")
    else:
        # Зберігаємо всі новини без фільтрації
        save_to_csv(all_news)
        show_statistics(all_news)


if __name__ == "__main__":
    main()
