import sqlite3
from datetime import datetime


class MovieDatabase:
    """Клас для керування базою даних кінофільмів"""

    def __init__(self, db_name="kinobase.db"):
        """Ініціалізація підключення до існуючої бази даних"""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_custom_function()

    def connect(self):
        """Підключення до бази даних"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            # Увімкнення підтримки зовнішніх ключів
            self.cursor.execute("PRAGMA foreign_keys = ON")
            print(f"✓ Підключено до бази даних '{self.db_name}'")
        except sqlite3.Error as e:
            print(f"✗ Помилка підключення до бази даних: {e}")
            raise

    def create_custom_function(self):
        """Створення власної функції movie_age()"""

        def movie_age(year):
            """Обчислює вік фільму відносно поточного року"""
            current_year = datetime.now().year
            return current_year - year

        self.conn.create_function("movie_age", 1, movie_age)
        print("✓ Функція movie_age() зареєстрована")

    def add_movie(self):
        """Додавання нового фільму"""
        print("\n=== ДОДАВАННЯ ФІЛЬМУ ===")
        try:
            title = input("Введіть назву фільму: ").strip()
            if not title:
                print("✗ Назва не може бути порожньою!")
                return

            release_year = int(input("Введіть рік випуску: "))
            if release_year < 1800 or release_year > datetime.now().year:
                print("✗ Некоректний рік випуску!")
                return

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
            add_actors = input("Додати акторів до цього фільму? (так/ні): ").lower()
            if add_actors == "так":
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

    def add_actor(self):
        """Додавання нового актора"""
        print("\n=== ДОДАВАННЯ АКТОРА ===")
        try:
            name = input("Введіть ім'я актора: ").strip()
            if not name:
                print("✗ Ім'я не може бути порожнім!")
                return

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

    def show_all_actors(self):
        """Показати всіх акторів"""
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

    def show_movies_with_actors(self):
        """Показати всі фільми з акторами (INNER JOIN)"""
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

    def show_unique_genres(self):
        """Показати унікальні жанри (DISTINCT)"""
        print("\n=== УНІКАЛЬНІ ЖАНРИ ===")
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

    def count_movies_by_genre(self):
        """Показати кількість фільмів за жанром (COUNT)"""
        print("\n=== КІЛЬКІСТЬ ФІЛЬМІВ ЗА ЖАНРОМ ===")
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

    def avg_actor_birth_year_by_genre(self):
        """Середній рік народження акторів у певному жанрі (AVG)"""
        print("\n=== СЕРЕДНІЙ РІК НАРОДЖЕННЯ АКТОРІВ ===")
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

    def search_movies_by_title(self):
        """Пошук фільмів за назвою (LIKE)"""
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

    def show_movies_paginated(self):
        """Показати фільми з пагінацією (LIMIT та OFFSET)"""
        print("\n=== ПЕРЕГЛЯД ФІЛЬМІВ (ПАГІНАЦІЯ) ===")
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

    def show_actors_and_movies_union(self):
        """Показати імена акторів та назви фільмів (UNION)"""
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
            self.cursor.execute(query)
            results = self.cursor.fetchall()

            if not results:
                print("База даних порожня")
                return

            for i, (item, item_type) in enumerate(results, 1):
                print(f"{i}. {item} ({item_type})")
        except sqlite3.Error as e:
            print(f"✗ Помилка отримання даних: {e}")

    def show_movies_with_age(self):
        """Показати фільми з їхнім віком (власна функція movie_age)"""
        print("\n=== ФІЛЬМИ ТА ЇХНІЙ ВІК ===")
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

    def close(self):
        """Закриття з'єднання з базою даних"""
        if self.conn:
            self.conn.close()
            print("\n✓ З'єднання з базою даних закрито")


def show_menu():
    """Відображення головного меню"""
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


def main():
    """Головна функція програми"""
    print("\n" + "=" * 50)
    print("     Вітаємо у системі керування КІНОБАЗОЮ!")
    print("=" * 50)

    # Підключення до існуючої бази даних
    try:
        db = MovieDatabase()
    except Exception as e:
        print(f"\n✗ Не вдалося підключитися до бази даних: {e}")
        print("Переконайтеся, що файл 'kinobase.db' існує та містить необхідні таблиці:")
        print("  - movies (id, title, release_year, genre)")
        print("  - actors (id, name, birth_year)")
        print("  - movie_cast (movie_id, actor_id)")
        return

    while True:
        show_menu()

        try:
            choice = input("\nВиберіть дію: ").strip()

            if choice == '1':
                db.add_movie()
            elif choice == '2':
                db.add_actor()
            elif choice == '3':
                db.show_movies_with_actors()
            elif choice == '4':
                db.show_unique_genres()
            elif choice == '5':
                db.count_movies_by_genre()
            elif choice == '6':
                db.avg_actor_birth_year_by_genre()
            elif choice == '7':
                db.search_movies_by_title()
            elif choice == '8':
                db.show_movies_paginated()
            elif choice == '9':
                db.show_actors_and_movies_union()
            elif choice == '10':
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
    main()