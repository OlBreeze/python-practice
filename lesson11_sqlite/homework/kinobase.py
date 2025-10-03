"""
КІНОБАЗА - Система керування базою даних фільмів та акторів
"""

import sqlite3
from datetime import datetime
from typing import Optional, Tuple, List


class MovieDatabase:
    """
    Клас для керування базою даних кінофільмів.

    Attributes:
        db_name (str): Назва файлу бази даних
        conn (Optional[sqlite3.Connection]): З'єднання з базою даних
        cursor (Optional[sqlite3.Cursor]): Курсор для виконання SQL-запитів
    """

    def __init__(self, db_name: str = "kinobase.db") -> None:
        """
        Ініціалізація підключення до існуючої бази даних.
        
        Args:
            db_name (str): Назва файлу бази даних. За замовчуванням "kinobase.db"
        """
        self.db_name: str = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
        self.connect()
        self.create_custom_function() # рееструемо кожен раз

    def connect(self) -> None:
        """
        Підключення до бази даних SQLite.
        
        Raises:
            sqlite3.Error: Якщо не вдалося підключитися до бази даних
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Увімкнення підтримки зовнішніх ключів
            self.cursor.execute("PRAGMA foreign_keys = ON")
            print(f"Підключено до бази даних '{self.db_name}'")
        except sqlite3.Error as e:
            print(f"Помилка підключення до бази даних: {e}")
            raise

    def create_custom_function(self) -> None:
        """
        Створення та реєстрація власної SQL-функції movie_age().
        
        Функція обчислює кількість років, що минули з моменту випуску
        фільму до поточного року.
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

        self.conn.create_function("movie_age", 1, movie_age)
        print("✓ Функція movie_age() зареєстрована")

    def add_movie(self) -> None:
        """
        Додавання нового фільму до бази даних.
        """
        print("\n---- ДОДАВАННЯ ФІЛЬМУ ----")
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

            # Додавання фільму
            self.cursor.execute(
                "INSERT INTO movies (title, release_year, genre) VALUES (?, ?, ?)",
                (title, release_year, genre)
            )
            movie_id = self.cursor.lastrowid

            # Додавання акторів до фільму
            add_actors = input("Додати акторів до цього фільму? (так-1/ні-2): ").lower()
            if add_actors == "1":
                self.show_all_actors()
                actor_ids = input("\nВведіть ID акторів через кому: ").strip()
                if actor_ids:
                    for actor_id in actor_ids.split(','):
                        try:
                            actor_id = int(actor_id.strip())
                            self.cursor.execute(
                                "INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                                (movie_id, actor_id)
                            )
                        except ValueError:
                            print(f"✗ Пропущено некоректний ID: {actor_id}")
                        except sqlite3.IntegrityError:
                            print(f"✗ Актор з ID {actor_id} не існує або вже доданий")

            self.conn.commit()
            print(f"✓ Фільм '{title}' успішно додано!")
        except ValueError:
            print("✗ Помилка: введіть числове значення для року")
        except sqlite3.Error as e:
            print(f"✗ Помилка додавання фільму: {e}")
            self.conn.rollback()

    def add_actor(self) -> None:
        """
        Додавання нового актора до бази даних.
        """
        print("\n---- ДОДАВАННЯ АКТОРА ----")
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

            self.cursor.execute(
                "INSERT INTO actors (name, birth_year) VALUES (?, ?)",
                (name, birth_year)
            )
            self.conn.commit()
            print(f"✓ Актор '{name}' успішно доданий!")
        except ValueError:
            print("✗ Помилка: введіть числове значення для року")
        except sqlite3.Error as e:
            print(f"✗ Помилка додавання актора: {e}")

    def add_actors_to_movie(self) -> None:
        """
        Додавання акторів до існуючого фільму.
        """
        print("\n---- ДОДАВАННЯ АКТОРІВ ДО ФІЛЬМУ ----")

        try:
            # Показуємо список всіх фільмів
            self.cursor.execute("SELECT id, title, release_year FROM movies ORDER BY title")
            movies = self.cursor.fetchall()

            if not movies:
                print("Немає фільмів у базі!")
                return

            print("\nСписок фільмів:")
            for movie in movies:
                print(f"  ID: {movie[0]}, Назва: {movie[1]} ({movie[2]})")

            # Вибір фільму
            movie_id = int(input("\nВведіть ID фільму: ").strip())

            # Перевірка існування фільму
            self.cursor.execute("SELECT title FROM movies WHERE id = ?", (movie_id,))
            movie = self.cursor.fetchone()

            if not movie:
                print(f"✗ Фільм з ID {movie_id} не знайдено!")
                return

            print(f"\nВибрано фільм: {movie[0]}")

            # Показуємо акторів, які вже є у цьому фільмі
            self.cursor.execute("""
                                SELECT a.id, a.name
                                FROM actors a
                                         INNER JOIN movie_cast mc ON a.id = mc.actor_id
                                WHERE mc.movie_id = ?
                                ORDER BY a.name
                                """, (movie_id,))
            existing_actors = self.cursor.fetchall()

            if existing_actors:
                print("\nАктори, які вже є у цьому фільмі:")
                for actor in existing_actors:
                    print(f"  ID: {actor[0]}, Ім'я: {actor[1]}")

            # Показуємо всіх акторів
            self.show_all_actors()

            # Вибір акторів
            actor_ids = input("\nВведіть ID акторів через кому: ").strip()

            if not actor_ids:
                print("✗ Не вказано жодного актора!")
                return

            added_count = 0
            for actor_id in actor_ids.split(','):
                try:
                    actor_id = int(actor_id.strip())
                    self.cursor.execute(
                        "INSERT INTO movie_cast (movie_id, actor_id) VALUES (?, ?)",
                        (movie_id, actor_id)
                    )
                    added_count += 1
                except ValueError:
                    print(f"✗ Пропущено некоректний ID: {actor_id}")
                except sqlite3.IntegrityError as e:
                    if "FOREIGN KEY" in str(e):
                        print(f"✗ Актор з ID {actor_id} не існує")
                    else:
                        print(f"✗ Актор з ID {actor_id} вже доданий до цього фільму")

            self.conn.commit()
            print(f"\n✓ Додано {added_count} актор(ів) до фільму '{movie[0]}'!")

        except ValueError:
            print("✗ Помилка: ID має бути числом!")
        except sqlite3.Error as e:
            print(f"✗ Помилка додавання акторів: {e}")
            self.conn.rollback()

    def show_all_actors(self) -> None:
        """
        Відображення списку всіх акторів з бази даних.
        """
        try:
            self.cursor.execute("SELECT id, name, birth_year FROM actors ORDER BY name")
            actors = self.cursor.fetchall()

            if not actors:
                print("\nБаза акторів порожня")
                return

            print("\nСписок акторів:")
            for actor in actors:
                print(f"  ID: {actor[0]}, Ім'я: {actor[1]}, Рік народження: {actor[2]}")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання акторів: {e}")

    def show_movies_with_actors(self) -> None:
        """
        Відображення всіх фільмів разом з акторами (використовує INNER JOIN).
        """
        print("\n---- ФІЛЬМИ ТА АКТОРИ ----")
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
            self.cursor.execute(query)
            movies = self.cursor.fetchall()

            if not movies:
                print("Немає фільмів з акторами")
                return

            for i, movie in enumerate(movies, 1):
                print(f"{i}. Фільм: \"{movie[0]}\" ({movie[1]}), Жанр: {movie[2]}")
                print(f"   Актори: {movie[3]}\n")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання даних: {e}")

    def show_unique_genres(self) -> None:
        """
        Відображення унікального списку жанрів (використовує DISTINCT).
        """
        print("\n---- УНІКАЛЬНІ ЖАНРИ DISTINCT ----")
        try:
            self.cursor.execute("SELECT DISTINCT genre FROM movies ORDER BY genre")
            genres = self.cursor.fetchall()

            if not genres:
                print("Немає жанрів у базі")
                return

            for i, genre in enumerate(genres, 1):
                print(f"{i}. {genre[0]}")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання жанрів: {e}")

    def count_movies_by_genre(self) -> None:
        """
        Підрахунок кількості фільмів за кожним жанром (використовує COUNT).
        """
        print("\n---- КІЛЬКІСТЬ ФІЛЬМІВ ЗА ЖАНРОМ - GROUP BY- ORDER BY---")
        try:
            query = '''
                    SELECT genre, COUNT(*) as count
                    FROM movies
                    GROUP BY genre
                    ORDER BY count DESC, genre \
                    '''
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                print("Немає фільмів у базі")
                return

            for i, (genre, count) in enumerate(results, 1):
                print(f"{i}. {genre}: {count} фільм(ів)")
        except sqlite3.Error as e:
            print(f"✗ Помилка підрахунку: {e}")

    def avg_actor_birth_year_by_genre(self) -> None:
        """
        Обчислення середнього року народження акторів у певному жанрі (використовує AVG).
        """
        print("\n---- СЕРЕДНІЙ РІК НАРОДЖЕННЯ АКТОРІВ AVG----")
        try:
            self.show_unique_genres()
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
            self.cursor.execute(query, (genre,))
            result = self.cursor.fetchone()

            if result[0] is None:
                print(f"Немає акторів у фільмах жанру '{genre}'")
                return

            print(f"\nСередній рік народження акторів у жанрі '{genre}': {result[0]:.1f}")
        except sqlite3.Error as e:
            print(f"✗ Помилка обчислення: {e}")

    def search_movies_by_title(self) -> None:
        """
        Пошук фільмів за ключовим словом у назві (використовує LIKE).
        """
        print("\n---- ПОШУК ФІЛЬМУ LIKE ----")
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
            self.cursor.execute(query, (f'%{keyword}%',))
            movies = self.cursor.fetchall()

            if not movies:
                print(f"Фільми з '{keyword}' не знайдено")
                return

            print(f"\nЗнайдені фільми:")
            for i, movie in enumerate(movies, 1):
                print(f"{i}. {movie[1]} ({movie[2]}), Жанр: {movie[3]}")
        except sqlite3.Error as e:
            print(f"✗ Помилка пошуку: {e}")

    def show_movies_paginated(self) -> None:
        """
        Відображення фільмів з пагінацією (використовує LIMIT та OFFSET).
        """
        print("\n---- ПЕРЕГЛЯД ФІЛЬМІВ (ПАГІНАЦІЯ) ----")
        try:
            # Підрахунок загальної кількості фільмів
            self.cursor.execute("SELECT COUNT(*) FROM movies")
            total = self.cursor.fetchone()[0]

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
                self.cursor.execute(query, (page_size, offset))
                movies = self.cursor.fetchall()

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

    def show_actors_and_movies_union(self) -> None:
        """
        Відображення об'єднаного списку акторів та фільмів (використовує UNION).
        """
        print("\n---- ІМЕНА АКТОРІВ ТА НАЗВИ ФІЛЬМІВ ----")
        try:
            query = '''
                    SELECT name as item, 'Актор' as type \
                    FROM actors
                    UNION
                    SELECT title as item, 'Фільм' as type \
                    FROM movies
                    ORDER BY item \
                    '''
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                print("База даних порожня")
                return

            for i, (item, item_type) in enumerate(results, 1):
                print(f"{i}. {item} ({item_type})")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання даних: {e}")

    def show_movies_with_age(self) -> None:
        """
        Відображення фільмів з їхнім віком (використовує власну функцію movie_age).
        """
        print("\n---- ФІЛЬМИ ТА ЇХНІЙ ВІК ----")
        try:
            query = '''
                    SELECT title, \
                           release_year, \
                           movie_age(release_year) as age
                    FROM movies
                    ORDER BY age DESC \
                    '''
            self.cursor.execute(query)
            movies = self.cursor.fetchall()

            if not movies:
                print("Немає фільмів у базі")
                return

            for i, (title, year, age) in enumerate(movies, 1):
                print(f"{i}. Фільм: \"{title}\" — {age} рок(ів) (випущено у {year})")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання даних: {e}")

    def close(self) -> None:
        """
        Закриття з'єднання з базою даних.
        """
        if self.conn:
            self.conn.close()
            print("\n✓ З'єднання з базою даних закрито")


def show_menu() -> None:
    """
    Відображення головного меню програми.
    """
    print("\n" + "~" * 50)
    print("           КІНОБАЗА - ГОЛОВНЕ МЕНЮ")
    print("~" * 50)
    print("1.  Додати фільм")
    print("2.  Додати актора")
    print("3.  Додати актора до фільму")
    print("4.  Показати всі фільми з акторами")
    print("5.  Показати унікальні жанри")
    print("6.  Показати кількість фільмів за жанром")
    print("7.  Показати середній рік народження акторів у певному жанрі")
    print("8.  Пошук фільму за назвою")
    print("9.  Показати фільми (з пагінацією)")
    print("10.  Показати імена всіх акторів та назви всіх фільмів")
    print("11. Показати фільми з їхнім віком")
    print("0.  Вихід")
    print("~" * 50)


def main() -> None:
    """
    Головна функція програми.
    
    Виконує наступні дії:
    1. Підключається до бази даних через клас MovieDatabase
    2. Запускає головний цикл меню
    3. Обробляє вибір користувача та викликає відповідні методи
    4. Закриває з'єднання при завершенні
    
    Обробляє винятки:
        - KeyboardInterrupt: Перервання програми користувачем (Ctrl+C)
        - Exception: Всі інші непередбачені помилки
    """

    # Підключення до існуючої бази даних
    try:
        db = MovieDatabase()
    except Exception as e:
        print(f"\n✗ Не вдалося підключитися до бази даних: {e}")
        return

    # Головний цикл програми
    while True:
        show_menu()

        try:
            choice = input("\nВиберіть дію: ").strip()

            # Обробка вибору користувача
            if choice == '1':
                db.add_movie()
            elif choice == '2':
                db.add_actor()
            elif choice == '3':
                db.add_actors_to_movie()
            elif choice == '4':
                db.show_movies_with_actors()
            elif choice == '5':
                db.show_unique_genres()
            elif choice == '6':
                db.count_movies_by_genre()
            elif choice == '7':
                db.avg_actor_birth_year_by_genre()
            elif choice == '8':
                db.search_movies_by_title()
            elif choice == '9':
                db.show_movies_paginated()
            elif choice == '10':
                db.show_actors_and_movies_union()
            elif choice == '11':
                db.show_movies_with_age()
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
    db.close()


if __name__ == "__main__":
    """
    Точка входу в програму.
    """
    main()
