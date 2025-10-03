"""
КІНОБАЗА - Система керування базою даних фільмів та акторів
"""

import sqlite3
from datetime import datetime
from typing import Optional, Tuple


# =====================================================
# ПІДКЛЮЧЕННЯ ДО БАЗИ ДАНИХ
# =====================================================

def connect_to_database(db_name: str = "kinobase.db") -> Tuple[Optional[sqlite3.Connection], Optional[sqlite3.Cursor]]:
    """
    Підключення до існуючої бази даних SQLite.

    Args:
        db_name (str): Назва файлу бази даних. За замовчуванням "kinobase.db"

    Returns:
        Tuple[Optional[Connection], Optional[Cursor]]: Кортеж з об'єктами підключення та курсора.
            Повертає (None, None) у разі помилки.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        print(f"Підключено до бази даних '{db_name}'")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Помилка підключення: {e}")
        return None, None


def register_custom_function(conn: sqlite3.Connection) -> None:
    """
    Реєстрація власної SQL-функції movie_age().

    Функція обчислює кількість років, що минули з моменту випуску фільму
    до поточного року.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних
    """
    def movie_age(year: int) -> int:
        """
        Обчислює вік фільму відносно поточного року.

        Args:
            year (int): Рік випуску фільму

        Returns:
            int: Кількість років з моменту випуску
        """
        current_year = datetime.now().year
        return current_year - year

    conn.create_function("movie_age", 1, movie_age)
    print("✓ Функція movie_age() зареєстрована")


# =====================================================
# ФУНКЦІЇ ДОДАВАННЯ ДАНИХ
# =====================================================

def add_movie(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Додавання нового фільму до бази даних.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== ДОДАВАННЯ ФІЛЬМУ ===")
    try:
        # Валідація назви фільму
        title = input("Введіть назву фільму: ").strip()
        if not title:
            print("✗ Назва не може бути порожньою!")
            return

        # Валідація року випуску
        release_year = int(input("Введіть рік випуску: "))
        if release_year < 1800 or release_year > datetime.now().year:
            print("✗ Некоректний рік випуску!")
            return

        # Валідація жанру
        genre = input("Введіть жанр: ").strip()
        if not genre:
            print("✗ Жанр не може бути порожнім!")
            return

        # Вставка фільму в базу даних
        cursor.execute(
            "INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
            (title, release_year, genre)
        )
        movie_id = cursor.lastrowid

        # Додавання акторів до фільму
        add_actors = input("Додати акторів до цього фільму? (так/ні): ").lower()
        if add_actors == "так":
            show_all_actors(cursor)
            actor_ids = input("\nВведіть ID акторів через кому: ").strip()
            if actor_ids:
                for actor_id in actor_ids.split(','):
                    try:
                        actor_id = int(actor_id.strip())
                        cursor.execute(
                            "INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                            (movie_id, actor_id)
                        )
                    except ValueError:
                        print(f"✗ Пропущено некоректний ID: {actor_id}")
                    except sqlite3.IntegrityError:
                        print(f"✗ Актор з ID {actor_id} не існує або вже доданий")

        conn.commit()
        print(f"✓ Фільм '{title}' успішно додано!")
    except ValueError:
        print("✗ Помилка: введіть числове значення для року")
    except sqlite3.Error as e:
        print(f"✗ Помилка додавання фільму: {e}")
        conn.rollback()


def add_actor(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Додавання нового актора до бази даних.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== ДОДАВАННЯ АКТОРА ===")
    try:
        # Валідація імені актора
        name = input("Введіть ім'я актора: ").strip()
        if not name:
            print("✗ Ім'я не може бути порожнім!")
            return

        # Валідація року народження
        birth_year = int(input("Введіть рік народження: "))
        if birth_year < 1800 or birth_year > datetime.now().year:
            print("✗ Некоректний рік народження!")
            return

        # Вставка актора в базу даних
        cursor.execute(
            "INSERT INTO actors (name, birth_year) VALUES (?, ?)",
            (name, birth_year)
        )
        conn.commit()
        print(f"✓ Актор '{name}' успішно доданий!")
    except ValueError:
        print("✗ Помилка: введіть числове значення для року")
    except sqlite3.Error as e:
        print(f"✗ Помилка додавання актора: {e}")


# =====================================================
# ФУНКЦІЇ ПЕРЕГЛЯДУ ДАНИХ
# =====================================================

def show_all_actors(cursor: sqlite3.Cursor) -> None:
    """
    Відображення списку всіх акторів з бази даних.
    Виводить ID, ім'я та рік народження кожного актора,
    відсортованих за іменем в алфавітному порядку.

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    try:
        cursor.execute("SELECT id, name, birth_year FROM actors ORDER BY name")
        actors = cursor.fetchall()

        if not actors:
            print("\nБаза акторів порожня")
            return

        print("\nСписок акторів:")
        for actor in actors:
            print(f"  ID: {actor[0]}, Ім'я: {actor[1]}, Рік народження: {actor[2]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання акторів: {e}")


def show_movies_with_actors(cursor: sqlite3.Cursor) -> None:
    """
    Відображення всіх фільмів разом з акторами (використовує INNER JOIN).

    Виконує складний SQL-запит з об'єднанням трьох таблиць:
    movies, movie_cast та actors. Групує акторів для кожного фільму.

    SQL Operations:
        - INNER JOIN: З'єднання таблиць movies, movie_cast та actors
        - GROUP_CONCAT: Об'єднання імен акторів в один рядок
        - GROUP BY: Групування результатів за фільмами

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== ФІЛЬМИ ТА АКТОРИ ===")
    try:
        query = '''
            SELECT 
                m.title, 
                m.release_year,
                m.genre,
                GROUP_CONCAT(a.name, ', ') as actors
            FROM movies m
            INNER JOIN movie_cast mc ON m.id = mc.movie_id
            INNER JOIN actors a ON mc.actor_id = a.id
            GROUP BY m.id, m.title, m.release_year, m.genre
            ORDER BY m.title
        '''
        cursor.execute(query)
        movies = cursor.fetchall()

        if not movies:
            print("Немає фільмів з акторами")
            return

        for i, movie in enumerate(movies, 1):
            print(f"{i}. Фільм: \"{movie[0]}\" ({movie[1]}), Жанр: {movie[2]}")
            print(f"   Актори: {movie[3]}\n")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


def show_unique_genres(cursor: sqlite3.Cursor) -> None:
    """
    Відображення унікального списку жанрів (використовує DISTINCT).

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== УНІКАЛЬНІ ЖАНРИ ===")
    try:
        cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        genres = cursor.fetchall()

        if not genres:
            print("Немає жанрів у базі")
            return

        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre[0]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання жанрів: {e}")


def count_movies_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Підрахунок кількості фільмів за кожним жанром (використовує COUNT).

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== КІЛЬКІСТЬ ФІЛЬМІВ ЗА ЖАНРОМ ===")
    try:
        query = '''
            SELECT genre, COUNT(*) as count
            FROM movies
            GROUP BY genre
            ORDER BY count DESC, genre
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("Немає фільмів у базі")
            return

        for i, (genre, count) in enumerate(results, 1):
            print(f"{i}. {genre}: {count} фільм(ів)")
    except sqlite3.Error as e:
        print(f"✗ Помилка підрахунку: {e}")


def avg_actor_birth_year_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Обчислення середнього року народження акторів у певному жанрі (використовує AVG).

    Функція спочатку відображає список жанрів, потім запитує у користувача
    конкретний жанр та обчислює середній рік народження акторів,
    які знімалися у фільмах цього жанру.

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== СЕРЕДНІЙ РІК НАРОДЖЕННЯ АКТОРІВ ===")
    try:
        show_unique_genres(cursor)
        genre = input("\nВведіть жанр: ").strip()

        if not genre:
            print("✗ Жанр не може бути порожнім!")
            return

        query = '''
            SELECT AVG(a.birth_year) as avg_birth_year
            FROM actors a
            INNER JOIN movie_cast mc ON a.id = mc.actor_id
            INNER JOIN movies m ON mc.movie_id = m.id
            WHERE m.genre = ?
        '''
        cursor.execute(query, (genre,))
        result = cursor.fetchone()

        if result[0] is None:
            print(f"Немає акторів у фільмах жанру '{genre}'")
            return

        print(f"\nСередній рік народження акторів у жанрі '{genre}': {result[0]:.1f}")
    except sqlite3.Error as e:
        print(f"✗ Помилка обчислення: {e}")


def search_movies_by_title(cursor: sqlite3.Cursor) -> None:
    """
    Пошук фільмів за ключовим словом у назві (використовує LIKE).

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== ПОШУК ФІЛЬМУ ===")
    try:
        keyword = input("Введіть ключове слово для пошуку: ").strip()

        if not keyword:
            print("✗ Ключове слово не може бути порожнім!")
            return

        query = '''
            SELECT id, title, release_year, genre
            FROM movies
            WHERE title LIKE ?
            ORDER BY title
        '''
        cursor.execute(query, (f'%{keyword}%',))
        movies = cursor.fetchall()

        if not movies:
            print(f"Фільми з '{keyword}' не знайдено")
            return

        print(f"\nЗнайдені фільми:")
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie[1]} ({movie[2]}), Жанр: {movie[3]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка пошуку: {e}")


def show_movies_paginated(cursor: sqlite3.Cursor) -> None:
    """
    Відображення фільмів з пагінацією (використовує LIMIT та OFFSET).

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Configuration:
        page_size (int): Кількість записів на сторінці (за замовчуванням 5)

    Example:
        >>> show_movies_paginated(cursor)
        --- Сторінка 1 з 3 ---
        1. Інтерстеллар (2014), Жанр: Наукова фантастика
        Всього фільмів: 15
    """
    print("\n=== ПЕРЕГЛЯД ФІЛЬМІВ (ПАГІНАЦІЯ) ===")
    try:
        # Підрахунок загальної кількості фільмів
        cursor.execute("SELECT COUNT(*) FROM movies")
        total = cursor.fetchone()[0]

        if total == 0:
            print("Немає фільмів у базі")
            return

        page_size = 5
        total_pages = (total + page_size - 1) // page_size
        page = 1

        while True:
            offset = (page - 1) * page_size

            query = '''
                SELECT id, title, release_year, genre
                FROM movies
                ORDER BY title
                LIMIT ? OFFSET ?
            '''
            cursor.execute(query, (page_size, offset))
            movies = cursor.fetchall()

            print(f"\n--- Сторінка {page} з {total_pages} ---")
            for i, movie in enumerate(movies, offset + 1):
                print(f"{i}. {movie[1]} ({movie[2]}), Жанр: {movie[3]}")

            print(f"\nВсього фільмів: {total}")

            if page < total_pages:
                action = input("\nНаступна сторінка (Enter) або вихід (q): ").strip().lower()
                if action == 'q':
                    break
                page += 1
            else:
                print("\nЦе остання сторінка")
                break
    except sqlite3.Error as e:
        print(f"✗ Помилка перегляду: {e}")


def show_actors_and_movies_union(cursor: sqlite3.Cursor) -> None:
    """
    Відображення об'єднаного списку акторів та фільмів (використовує UNION).

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів
    """
    print("\n=== ІМЕНА АКТОРІВ ТА НАЗВИ ФІЛЬМІВ ===")
    try:
        query = '''
            SELECT name as item, 'Актор' as type FROM actors
            UNION
            SELECT title as item, 'Фільм' as type FROM movies
            ORDER BY item
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("База даних порожня")
            return

        for i, (item, item_type) in enumerate(results, 1):
            print(f"{i}. {item} ({item_type})")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


def show_movies_with_age(cursor: sqlite3.Cursor) -> None:
    """
    Відображення фільмів з їхнім віком (використовує власну функцію movie_age).

    Функція демонструє використання користувацької SQL-функції movie_age(),
    яка обчислює, скільки років минуло з моменту випуску фільму.

    SQL Operations:
        - movie_age(): Користувацька функція для обчислення віку
        - ORDER BY: Сортування за віком (спадання)

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Note:
        Потрібно попередньо зареєструвати функцію через register_custom_function()

    Example:
        >>> show_movies_with_age(cursor)
        1. Фільм: "Матриця" — 26 рок(ів) (випущено у 1999)
        2. Фільм: "Інтерстеллар" — 11 рок(ів) (випущено у 2014)
    """
    print("\n=== ФІЛЬМИ ТА ЇХНІЙ ВІК ===")
    try:
        query = '''
            SELECT 
                title,
                release_year,
                movie_age(release_year) as age
            FROM movies
            ORDER BY age DESC
        '''
        cursor.execute(query)
        movies = cursor.fetchall()

        if not movies:
            print("Немає фільмів у базі")
            return

        for i, (title, year, age) in enumerate(movies, 1):
            print(f"{i}. Фільм: \"{title}\" — {age} рок(ів) (випущено у {year})")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


# =====================================================
# ГОЛОВНЕ МЕНЮ ТА ОСНОВНА ЛОГІКА
# =====================================================

def show_menu() -> None:
    """
    Відображення головного меню програми.

    Виводить список всіх доступних операцій з базою даних.
    Використовується в головному циклі програми.
    """
    print("\n" + "="*50)
    print("           КІНОБАЗА - ГОЛОВНЕ МЕНЮ")
    print("="*50)
    print("1.  Додати фільм")
    print("2.  Додати актора")
    print("3.  Показати всі фільми з акторами")
    print("4.  Показати унікальні жанри")
    print("5.  Показати кількість фільмів за жанром")
    print("6.  Показати середній рік народження акторів у певному жанрі")
    print("7.  Пошук фільму за назвою")
    print("8.  Показати фільми (з пагінацією)")
    print("9.  Показати імена всіх акторів та назви всіх фільмів")
    print("10. Показати фільми з їхнім віком")
    print("0.  Вихід")
    print("="*50)


def main() -> None:
    """
    Головна функція програми.

    Виконує наступні дії:
    1. Підключається до бази даних
    2. Реєструє користувацьку функцію movie_age()
    3. Запускає головний цикл меню
    4. Обробляє вибір користувача
    5. Закриває з'єднання при завершенні

    Обробляє винятки:
        - KeyboardInterrupt: Перервання програми користувачем (Ctrl+C)
        - Exception: Всі інші непередбачені помилки

    Example:
        >>> main()
        Вітаємо у системі керування КІНОБАЗОЮ!
        [Меню програми]
    """
    print("\n" + "="*50)
    print("     Вітаємо у системі керування КІНОБАЗОЮ!")
    print("="*50)

    # Підключення до бази даних
    conn, cursor = connect_to_database()

    if not conn or not cursor:
        print("\n✗ Не вдалося підключитися до бази даних!")
        print("Переконайтеся, що файл 'kinobase.db' існує та містить необхідні таблиці:")
        print("  - movies (id, title, release_year, genre)")
        print("  - actors (id, name, birth_year)")
        print("  - movie_cast (movie_id, actor_id)")
        return

    # Реєстрація власної функції
    register_custom_function(conn)

    # Головний цикл програми
    while True:
        show_menu()

        try:
            choice = input("\nВиберіть дію: ").strip()

            # Обробка вибору користувача
            if choice == '1':
                add_movie(conn, cursor)
            elif choice == '2':
                add_actor(conn, cursor)
            elif choice == '3':
                show_movies_with_actors(cursor)
            elif choice == '4':
                show_unique_genres(cursor)
            elif choice == '5':
                count_movies_by_genre(cursor)
            elif choice == '6':
                avg_actor_birth_year_by_genre(cursor)
            elif choice == '7':
                search_movies_by_title(cursor)
            elif choice == '8':
                show_movies_paginated(cursor)
            elif choice == '9':
                show_actors_and_movies_union(cursor)
            elif choice == '10':
                show_movies_with_age(cursor)
            elif choice == '0':
                print("\nДякуємо за використання Кінобази! До побачення!")
                break
            else:
                print("\n✗ Невірний вибір! Спробуйте ще раз.")

            # Пауза перед показом меню знову
            if choice != '0':
                input("\nНатисніть Enter для продовження...")

        except KeyboardInterrupt:
            print("\n\nПрограму перервано користувачем")
            break
        except Exception as e:
            print(f"\n✗ Непередбачена помилка: {e}")

    # Закриття бази даних
    if conn:
        conn.close()
        print("✓ З'єднання з базою даних закрито")


"""
КІНОБАЗА - Система керування базою даних фільмів та акторів

Цей модуль надає функціонал для роботи з базою даних SQLite,
що містить інформацію про фільми, акторів та їхні зв'язки.

Використовує функціональний підхід без об'єктно-орієнтованого програмування.

Автор: [Ваше ім'я]
Дата: 2025
Версія: 1.0

Таблиці бази даних:
    - movies: id, title, release_year, genre
    - actors: id, name, birth_year
    - movie_cast: movie_id, actor_id
"""

import sqlite3
from datetime import datetime
from typing import Optional, Tuple


# =====================================================
# ПІДКЛЮЧЕННЯ ДО БАЗИ ДАНИХ
# =====================================================

def connect_to_database(db_name: str = "kinobase.db") -> Tuple[Optional[sqlite3.Connection], Optional[sqlite3.Cursor]]:
    """
    Підключення до існуючої бази даних SQLite.

    Args:
        db_name (str): Назва файлу бази даних. За замовчуванням "kinobase.db"

    Returns:
        Tuple[Optional[Connection], Optional[Cursor]]: Кортеж з об'єктами підключення та курсора.
            Повертає (None, None) у разі помилки.

    Example:
        >>> conn, cursor = connect_to_database("kinobase.db")
        >>> if conn:
        ...     print("Підключено успішно")
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        # Увімкнення підтримки зовнішніх ключів для забезпечення цілісності даних
        cursor.execute("PRAGMA foreign_keys = ON")
        print(f"✓ Підключено до бази даних '{db_name}'")
        return conn, cursor
    except sqlite3.Error as e:
        print(f"✗ Помилка підключення: {e}")
        return None, None


def register_custom_function(conn: sqlite3.Connection) -> None:
    """
    Реєстрація власної SQL-функції movie_age().

    Функція обчислює кількість років, що минули з моменту випуску фільму
    до поточного року.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних

    Example:
        >>> register_custom_function(conn)
        >>> cursor.execute("SELECT title, movie_age(release_year) FROM movies")
    """

    def movie_age(year: int) -> int:
        """
        Обчислює вік фільму відносно поточного року.

        Args:
            year (int): Рік випуску фільму

        Returns:
            int: Кількість років з моменту випуску
        """
        current_year = datetime.now().year
        return current_year - year

    conn.create_function("movie_age", 1, movie_age)
    print("✓ Функція movie_age() зареєстрована")


# =====================================================
# ФУНКЦІЇ ДОДАВАННЯ ДАНИХ
# =====================================================

def add_movie(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Додавання нового фільму до бази даних.

    Функція запитує у користувача назву, рік випуску та жанр фільму,
    а також надає можливість додати акторів до фільму.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних
        cursor (Cursor): Курсор для виконання SQL-запитів

    Validates:
        - Назва фільму не може бути порожньою
        - Рік випуску має бути в діапазоні 1800 - поточний рік
        - Жанр не може бути порожнім

    Example:
        >>> add_movie(conn, cursor)
        Введіть назву фільму: Інтерстеллар
        Введіть рік випуску: 2014
        Введіть жанр: Наукова фантастика
    """
    print("\n=== ДОДАВАННЯ ФІЛЬМУ ===")
    try:
        # Валідація назви фільму
        title = input("Введіть назву фільму: ").strip()
        if not title:
            print("✗ Назва не може бути порожньою!")
            return

        # Валідація року випуску
        release_year = int(input("Введіть рік випуску: "))
        if release_year < 1800 or release_year > datetime.now().year:
            print("✗ Некоректний рік випуску!")
            return

        # Валідація жанру
        genre = input("Введіть жанр: ").strip()
        if not genre:
            print("✗ Жанр не може бути порожнім!")
            return

        # Вставка фільму в базу даних
        cursor.execute(
            "INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
            (title, release_year, genre)
        )
        movie_id = cursor.lastrowid

        # Додавання акторів до фільму
        add_actors = input("Додати акторів до цього фільму? (так/ні): ").lower()
        if add_actors == "так":
            show_all_actors(cursor)
            actor_ids = input("\nВведіть ID акторів через кому: ").strip()
            if actor_ids:
                for actor_id in actor_ids.split(','):
                    try:
                        actor_id = int(actor_id.strip())
                        cursor.execute(
                            "INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                            (movie_id, actor_id)
                        )
                    except ValueError:
                        print(f"✗ Пропущено некоректний ID: {actor_id}")
                    except sqlite3.IntegrityError:
                        print(f"✗ Актор з ID {actor_id} не існує або вже доданий")

        conn.commit()
        print(f"✓ Фільм '{title}' успішно додано!")
    except ValueError:
        print("✗ Помилка: введіть числове значення для року")
    except sqlite3.Error as e:
        print(f"✗ Помилка додавання фільму: {e}")
        conn.rollback()


def add_actor(conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    """
    Додавання нового актора до бази даних.

    Функція запитує у користувача ім'я та рік народження актора.

    Args:
        conn (Connection): Об'єкт з'єднання з базою даних
        cursor (Cursor): Курсор для виконання SQL-запитів

    Validates:
        - Ім'я актора не може бути порожнім
        - Рік народження має бути в діапазоні 1800 - поточний рік

    Example:
        >>> add_actor(conn, cursor)
        Введіть ім'я актора: Меттью Макконахі
        Введіть рік народження: 1969
    """
    print("\n=== ДОДАВАННЯ АКТОРА ===")
    try:
        # Валідація імені актора
        name = input("Введіть ім'я актора: ").strip()
        if not name:
            print("✗ Ім'я не може бути порожнім!")
            return

        # Валідація року народження
        birth_year = int(input("Введіть рік народження: "))
        if birth_year < 1800 or birth_year > datetime.now().year:
            print("✗ Некоректний рік народження!")
            return

        # Вставка актора в базу даних
        cursor.execute(
            "INSERT INTO actors (name, birth_year) VALUES (?, ?)",
            (name, birth_year)
        )
        conn.commit()
        print(f"✓ Актор '{name}' успішно доданий!")
    except ValueError:
        print("✗ Помилка: введіть числове значення для року")
    except sqlite3.Error as e:
        print(f"✗ Помилка додавання актора: {e}")


# =====================================================
# ФУНКЦІЇ ПЕРЕГЛЯДУ ДАНИХ
# =====================================================

def show_all_actors(cursor: sqlite3.Cursor) -> None:
    """
    Відображення списку всіх акторів з бази даних.

    Виводить ID, ім'я та рік народження кожного актора,
    відсортованих за іменем в алфавітному порядку.

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> show_all_actors(cursor)
        Список акторів:
          ID: 1, Ім'я: Меттью Макконахі, Рік народження: 1969
    """
    try:
        cursor.execute("SELECT id, name, birth_year FROM actors ORDER BY name")
        actors = cursor.fetchall()

        if not actors:
            print("\nБаза акторів порожня")
            return

        print("\nСписок акторів:")
        for actor in actors:
            print(f"  ID: {actor[0]}, Ім'я: {actor[1]}, Рік народження: {actor[2]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання акторів: {e}")


def show_movies_with_actors(cursor: sqlite3.Cursor) -> None:
    """
    Відображення всіх фільмів разом з акторами (використовує INNER JOIN).

    Виконує складний SQL-запит з об'єднанням трьох таблиць:
    movies, movie_cast та actors. Групує акторів для кожного фільму.

    SQL Operations:
        - INNER JOIN: З'єднання таблиць movies, movie_cast та actors
        - GROUP_CONCAT: Об'єднання імен акторів в один рядок
        - GROUP BY: Групування результатів за фільмами

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> show_movies_with_actors(cursor)
        1. Фільм: "Інтерстеллар" (2014), Жанр: Наукова фантастика
           Актори: Меттью Макконахі, Енн Хетеуей
    """
    print("\n=== ФІЛЬМИ ТА АКТОРИ ===")
    try:
        query = '''
                SELECT m.title, \
                       m.release_year, \
                       m.genre, \
                       GROUP_CONCAT(a.name, ', ') as actors
                FROM movies m
                         INNER JOIN movie_cast mc ON m.id = mc.movie_id
                         INNER JOIN actors a ON mc.actor_id = a.id
                GROUP BY m.id, m.title, m.release_year, m.genre
                ORDER BY m.title \
                '''
        cursor.execute(query)
        movies = cursor.fetchall()

        if not movies:
            print("Немає фільмів з акторами")
            return

        for i, movie in enumerate(movies, 1):
            print(f"{i}. Фільм: \"{movie[0]}\" ({movie[1]}), Жанр: {movie[2]}")
            print(f"   Актори: {movie[3]}\n")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


def show_unique_genres(cursor: sqlite3.Cursor) -> None:
    """
    Відображення унікального списку жанрів (використовує DISTINCT).

    Виконує SQL-запит для отримання всіх унікальних жанрів
    без повторень, відсортованих за алфавітом.

    SQL Operations:
        - DISTINCT: Вибірка тільки унікальних значень
        - ORDER BY: Сортування результатів

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> show_unique_genres(cursor)
        1. Драма
        2. Комедія
        3. Наукова фантастика
    """
    print("\n=== УНІКАЛЬНІ ЖАНРИ ===")
    try:
        cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
        genres = cursor.fetchall()

        if not genres:
            print("Немає жанрів у базі")
            return

        for i, genre in enumerate(genres, 1):
            print(f"{i}. {genre[0]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання жанрів: {e}")


def count_movies_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Підрахунок кількості фільмів за кожним жанром (використовує COUNT).

    Виконує агрегатний SQL-запит для підрахунку кількості фільмів
    у кожному жанрі, відсортованих за кількістю (спадання).

    SQL Operations:
        - COUNT(*): Підрахунок кількості записів
        - GROUP BY: Групування за жанром
        - ORDER BY: Сортування за кількістю (спадання)

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> count_movies_by_genre(cursor)
        1. Драма: 8 фільм(ів)
        2. Наукова фантастика: 5 фільм(ів)
    """
    print("\n=== КІЛЬКІСТЬ ФІЛЬМІВ ЗА ЖАНРОМ ===")
    try:
        query = '''
                SELECT genre, COUNT(*) as count
                FROM movies
                GROUP BY genre
                ORDER BY count DESC, genre \
                '''
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("Немає фільмів у базі")
            return

        for i, (genre, count) in enumerate(results, 1):
            print(f"{i}. {genre}: {count} фільм(ів)")
    except sqlite3.Error as e:
        print(f"✗ Помилка підрахунку: {e}")


def avg_actor_birth_year_by_genre(cursor: sqlite3.Cursor) -> None:
    """
    Обчислення середнього року народження акторів у певному жанрі (використовує AVG).

    Функція спочатку відображає список жанрів, потім запитує у користувача
    конкретний жанр та обчислює середній рік народження акторів,
    які знімалися у фільмах цього жанру.

    SQL Operations:
        - AVG(): Обчислення середнього значення
        - INNER JOIN: З'єднання трьох таблиць
        - WHERE: Фільтрація за жанром

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> avg_actor_birth_year_by_genre(cursor)
        Введіть жанр: Наукова фантастика
        Середній рік народження акторів у жанрі 'Наукова фантастика': 1965.5
    """
    print("\n=== СЕРЕДНІЙ РІК НАРОДЖЕННЯ АКТОРІВ ===")
    try:
        show_unique_genres(cursor)
        genre = input("\nВведіть жанр: ").strip()

        if not genre:
            print("✗ Жанр не може бути порожнім!")
            return

        query = '''
                SELECT AVG(a.birth_year) as avg_birth_year
                FROM actors a
                         INNER JOIN movie_cast mc ON a.id = mc.actor_id
                         INNER JOIN movies m ON mc.movie_id = m.id
                WHERE m.genre = ? \
                '''
        cursor.execute(query, (genre,))
        result = cursor.fetchone()

        if result[0] is None:
            print(f"Немає акторів у фільмах жанру '{genre}'")
            return

        print(f"\nСередній рік народження акторів у жанрі '{genre}': {result[0]:.1f}")
    except sqlite3.Error as e:
        print(f"✗ Помилка обчислення: {e}")


def search_movies_by_title(cursor: sqlite3.Cursor) -> None:
    """
    Пошук фільмів за ключовим словом у назві (використовує LIKE).

    Функція виконує пошук фільмів, назви яких містять введене
    користувачем ключове слово (регістр не враховується).

    SQL Operations:
        - LIKE: Пошук часткових збігів
        - Wildcards (%): Шаблони для пошуку

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> search_movies_by_title(cursor)
        Введіть ключове слово для пошуку: Мат
        1. Матриця (1999), Жанр: Наукова фантастика
    """
    print("\n=== ПОШУК ФІЛЬМУ ===")
    try:
        keyword = input("Введіть ключове слово для пошуку: ").strip()

        if not keyword:
            print("✗ Ключове слово не може бути порожнім!")
            return

        query = '''
                SELECT id, title, release_year, genre
                FROM movies
                WHERE title LIKE ?
                ORDER BY title \
                '''
        cursor.execute(query, (f'%{keyword}%',))
        movies = cursor.fetchall()

        if not movies:
            print(f"Фільми з '{keyword}' не знайдено")
            return

        print(f"\nЗнайдені фільми:")
        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie[1]} ({movie[2]}), Жанр: {movie[3]}")
    except sqlite3.Error as e:
        print(f"✗ Помилка пошуку: {e}")


def show_movies_paginated(cursor: sqlite3.Cursor) -> None:
    """
    Відображення фільмів з пагінацією (використовує LIMIT та OFFSET).

    Функція розбиває результати на сторінки та дозволяє користувачу
    переглядати їх поступово. Використовується для роботи з великими
    обсягами даних.

    SQL Operations:
        - COUNT(*): Підрахунок загальної кількості записів
        - LIMIT: Обмеження кількості результатів
        - OFFSET: Зміщення початку вибірки

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Configuration:
        page_size (int): Кількість записів на сторінці (за замовчуванням 5)

    Example:
        >>> show_movies_paginated(cursor)
        --- Сторінка 1 з 3 ---
        1. Інтерстеллар (2014), Жанр: Наукова фантастика
        Всього фільмів: 15
    """
    print("\n=== ПЕРЕГЛЯД ФІЛЬМІВ (ПАГІНАЦІЯ) ===")
    try:
        # Підрахунок загальної кількості фільмів
        cursor.execute("SELECT COUNT(*) FROM movies")
        total = cursor.fetchone()[0]

        if total == 0:
            print("Немає фільмів у базі")
            return

        page_size = 5
        total_pages = (total + page_size - 1) // page_size
        page = 1

        while True:
            offset = (page - 1) * page_size

            query = '''
                    SELECT id, title, release_year, genre
                    FROM movies
                    ORDER BY title LIMIT ? \
                    OFFSET ? \
                    '''
            cursor.execute(query, (page_size, offset))
            movies = cursor.fetchall()

            print(f"\n--- Сторінка {page} з {total_pages} ---")
            for i, movie in enumerate(movies, offset + 1):
                print(f"{i}. {movie[1]} ({movie[2]}), Жанр: {movie[3]}")

            print(f"\nВсього фільмів: {total}")

            if page < total_pages:
                action = input("\nНаступна сторінка (Enter) або вихід (q): ").strip().lower()
                if action == 'q':
                    break
                page += 1
            else:
                print("\nЦе остання сторінка")
                break
    except sqlite3.Error as e:
        print(f"✗ Помилка перегляду: {e}")


def show_actors_and_movies_union(cursor: sqlite3.Cursor) -> None:
    """
    Відображення об'єднаного списку акторів та фільмів (використовує UNION).

    Функція об'єднує два різні набори результатів (імена акторів та назви фільмів)
    в один відсортований список з позначкою типу елемента.

    SQL Operations:
        - UNION: Об'єднання результатів двох SELECT-запитів
        - ORDER BY: Сортування об'єднаних результатів

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Example:
        >>> show_actors_and_movies_union(cursor)
        1. Інтерстеллар (Фільм)
        2. Меттью Макконахі (Актор)
    """
    print("\n=== ІМЕНА АКТОРІВ ТА НАЗВИ ФІЛЬМІВ ===")
    try:
        query = '''
                SELECT name as item, 'Актор' as type \
                FROM actors
                UNION
                SELECT title as item, 'Фільм' as type \
                FROM movies
                ORDER BY item \
                '''
        cursor.execute(query)
        results = cursor.fetchall()

        if not results:
            print("База даних порожня")
            return

        for i, (item, item_type) in enumerate(results, 1):
            print(f"{i}. {item} ({item_type})")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


def show_movies_with_age(cursor: sqlite3.Cursor) -> None:
    """
    Відображення фільмів з їхнім віком (використовує власну функцію movie_age).

    Функція демонструє використання користувацької SQL-функції movie_age(),
    яка обчислює, скільки років минуло з моменту випуску фільму.

    SQL Operations:
        - movie_age(): Користувацька функція для обчислення віку
        - ORDER BY: Сортування за віком (спадання)

    Args:
        cursor (Cursor): Курсор для виконання SQL-запитів

    Note:
        Потрібно попередньо зареєструвати функцію через register_custom_function()

    Example:
        >>> show_movies_with_age(cursor)
        1. Фільм: "Матриця" — 26 рок(ів) (випущено у 1999)
        2. Фільм: "Інтерстеллар" — 11 рок(ів) (випущено у 2014)
    """
    print("\n=== ФІЛЬМИ ТА ЇХНІЙ ВІК ===")
    try:
        query = '''
                SELECT title, \
                       release_year, \
                       movie_age(release_year) as age
                FROM movies
                ORDER BY age DESC \
                '''
        cursor.execute(query)
        movies = cursor.fetchall()

        if not movies:
            print("Немає фільмів у базі")
            return

        for i, (title, year, age) in enumerate(movies, 1):
            print(f"{i}. Фільм: \"{title}\" — {age} рок(ів) (випущено у {year})")
    except sqlite3.Error as e:
        print(f"✗ Помилка отримання даних: {e}")


# =====================================================
# ГОЛОВНЕ МЕНЮ ТА ОСНОВНА ЛОГІКА
# =====================================================

def show_menu() -> None:
    """
    Відображення головного меню програми.

    Виводить список всіх доступних операцій з базою даних.
    Використовується в головному циклі програми.
    """
    print("\n" + "=" * 50)
    print("           КІНОБАЗА - ГОЛОВНЕ МЕНЮ")
    print("=" * 50)
    print("1.  Додати фільм")
    print("2.  Додати актора")
    print("3.  Показати всі фільми з акторами")
    print("4.  Показати унікальні жанри")
    print("5.  Показати кількість фільмів за жанром")
    print("6.  Показати середній рік народження акторів у певному жанрі")
    print("7.  Пошук фільму за назвою")
    print("8.  Показати фільми (з пагінацією)")
    print("9.  Показати імена всіх акторів та назви всіх фільмів")
    print("10. Показати фільми з їхнім віком")
    print("0.  Вихід")
    print("=" * 50)


def main() -> None:
    """
    Головна функція програми.
    """
    print("\n" + "=" * 50)
    print("     Вітаємо у системі керування КІНОБАЗОЮ!")
    print("=" * 50)

    # Підключення до бази даних
    conn, cursor = connect_to_database()

    if not conn or not cursor:
        print("\nНе вдалося підключитися до бази даних!")
        return

    # Реєстрація власної функції
    register_custom_function(conn)

    # Головний цикл програми
    while True:
        show_menu()

        try:
            choice = input("\nВиберіть дію: ").strip()

            # Обробка вибору користувача
            if choice == '1':
                add_movie(conn, cursor)
            elif choice == '2':
                add_actor(conn, cursor)
            elif choice == '3':
                show_movies_with_actors(cursor)
            elif choice == '4':
                show_unique_genres(cursor)
            elif choice == '5':
                count_movies_by_genre(cursor)
            elif choice == '6':
                avg_actor_birth_year_by_genre(cursor)
            elif choice == '7':
                search_movies_by_title(cursor)
            elif choice == '8':
                show_movies_paginated(cursor)
            elif choice == '9':
                show_actors_and_movies_union(cursor)
            elif choice == '10':
                show_movies_with_age(cursor)
            elif choice == '0':
                print("\nДякуємо за використання Кінобази! До побачення!")
                break
            else:
                print("\n✗ Невірний вибір! Спробуйте ще раз.")

            # Пауза перед показом меню знову
            if choice != '0':
                input("\nНатисніть Enter для продовження...")

        except KeyboardInterrupt:
            print("\n\nПрограму перервано користувачем")
            break
        except Exception as e:
            print(f"\n✗ Непередбачена помилка: {e}")

    # Закриття бази даних
    if conn:
        conn.close()
        print("✓ З'єднання з базою даних закрито")


# =====================================================
# ТОЧКА ВХОДУ В ПРОГРАМУ
# =====================================================

if __name__ == "__main__":
    """
    Точка входу в програму.
    """
    main()