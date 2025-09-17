import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class Book:
    """
    Клас для представлення книги.

    Attributes:
        назва (str): Назва книги
        автор (str): Автор книги
        рік (int): Рік видання
        наявність (bool): Чи доступна книга
    """

    def __init__(self, назва: str, автор: str, рік: int, наявність: bool) -> None:
        """
        Ініціалізація об'єкта книги.

        Args:
            назва: Назва книги
            автор: Автор книги
            рік: Рік видання
            наявність: Чи доступна книга
        """
        self.назва = назва
        self.автор = автор
        self.рік = рік
        self.наявність = наявність

    def to_dict(self) -> Dict[str, Any]:
        """
        Перетворює об'єкт книги в словник для JSON серіалізації.

        Returns:
            Dict[str, Any]: Словник з даними книги
        """
        return {
            "назва": self.назва,
            "автор": self.автор,
            "рік": self.рік,
            "наявність": self.наявність
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Book':
        """
        Створює об'єкт книги зі словника.

        Args:
            data: Словник з даними книги

        Returns:
            Book: Новий об'єкт книги
        """
        return cls(
            назва=data["назва"],
            автор=data["автор"],
            рік=data["рік"],
            наявність=data["наявність"]
        )

    def __str__(self) -> str:
        """Строкове представлення книги."""
        status = "✓ Доступна" if self.наявність else "✗ Недоступна"
        return f'"{self.назва}" від {self.автор} ({self.рік}) - {status}'


class LibraryManager:
    """
    Клас для управління бібліотекою книг.

    Attributes:
        file_path (Path): Шлях до JSON файлу з книгами
        books (List[Book]): Список книг у бібліотеці
    """

    def __init__(self, file_path: str = "books.json") -> None:
        """
        Ініціалізація менеджера бібліотеки.

        Args:
            file_path: Шлях до JSON файлу з книгами
        """
        self.file_path = Path(file_path)
        self.books: List[Book] = []
        self._create_initial_json()
        self.load_books()

    def _create_initial_json(self) -> None:
        """Створює початковий JSON файл, якщо він не існує."""
        if not self.file_path.exists():
            initial_books = [
                {
                    "назва": "Кобзар",
                    "автор": "Тарас Шевченко",
                    "рік": 1840,
                    "наявність": True
                },
                {
                    "назва": "Лісова пісня",
                    "автор": "Леся Українка",
                    "рік": 1911,
                    "наявність": True
                },
                {
                    "назва": "Захар Беркут",
                    "автор": "Іван Франко",
                    "рік": 1883,
                    "наявність": False
                },
                {
                    "назва": "Тіні забутих предків",
                    "автор": "Михайло Коцюбинський",
                    "рік": 1913,
                    "наявність": True
                },
                {
                    "назва": "Енеїда",
                    "автор": "Іван Котляревський",
                    "рік": 1798,
                    "наявність": False
                }
            ]

            self.save_books_to_file(initial_books)
            print(f"✓ Створено початковий файл {self.file_path}")

    def load_books(self) -> None:
        """
        Завантажує книги з JSON файлу.

        Raises:
            FileNotFoundError: Якщо файл не знайдено
            json.JSONDecodeError: Якщо файл містить некоректний JSON
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                books_data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in books_data]
            print(f"✓ Завантажено {len(self.books)} книг з {self.file_path}")

        except FileNotFoundError:
            print(f"✗ Файл {self.file_path} не знайдено")
            self.books = []
        except json.JSONDecodeError as e:
            print(f"✗ Помилка читання JSON: {e}")
            self.books = []
        except KeyError as e:
            print(f"✗ Відсутнє обов'язкове поле в JSON: {e}")
            self.books = []

    def save_books(self) -> None:
        """Зберігає поточний список книг у JSON файл."""
        books_data = [book.to_dict() for book in self.books]
        self.save_books_to_file(books_data)

    def save_books_to_file(self, books_data: List[Dict[str, Any]]) -> None:
        """
        Зберігає список книг у JSON файл.

        Args:
            books_data: Список словників з даними книг
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(books_data, file, ensure_ascii=False, indent=2)
            print(f"✓ Книги збережено в {self.file_path}")
        except IOError as e:
            print(f"✗ Помилка збереження файлу: {e}")

    def get_available_books(self) -> List[Book]:
        """
        Повертає список доступних книг (наявність = True).

        Returns:
            List[Book]: Список доступних книг
        """
        return [book for book in self.books if book.наявність]

    def display_available_books(self) -> None:
        """Виводить список доступних книг."""
        available_books = self.get_available_books()

        if not available_books:
            print("📚 Немає доступних книг у бібліотеці")
            return

        print(f"\n📚 Доступні книги ({len(available_books)} шт.):")
        print("=" * 60)
        for i, book in enumerate(available_books, 1):
            print(f"{i}. {book}")

    def display_all_books(self) -> None:
        """Виводить список усіх книг."""
        if not self.books:
            print("📚 Бібліотека порожня")
            return

        print(f"\n📚 Усі книги ({len(self.books)} шт.):")
        print("=" * 60)
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

    def add_book(self, назва: str, автор: str, рік: int, наявність: bool = True) -> None:
        """
        Додає нову книгу в бібліотеку.

        Args:
            назва: Назва книги
            автор: Автор книги
            рік: Рік видання
            наявність: Чи доступна книга (за замовчуванням True)
        """
        # Перевіряємо, чи вже існує така книга
        for book in self.books:
            if book.назва.lower() == назва.lower() and book.автор.lower() == автор.lower():
                print(f"⚠️  Книга '{назва}' від {автор} вже існує в бібліотеці")
                return

        new_book = Book(назва, автор, рік, наявність)
        self.books.append(new_book)
        self.save_books()

        print(f"✓ Додано нову книгу: {new_book}")

    def find_books_by_author(self, автор: str) -> List[Book]:
        """
        Знаходить книги за автором.

        Args:
            автор: Ім'я автора для пошуку

        Returns:
            List[Book]: Список книг знайденого автора
        """
        return [book for book in self.books if автор.lower() in book.автор.lower()]

    def find_books_by_title(self, назва: str) -> List[Book]:
        """
        Знаходить книги за назвою.

        Args:
            назва: Назва для пошуку

        Returns:
            List[Book]: Список книг з відповідною назвою
        """
        return [book for book in self.books if назва.lower() in book.назва.lower()]

    def update_book_availability(self, назва: str, автор: str, наявність: bool) -> bool:
        """
        Оновлює доступність книги.

        Args:
            назва: Назва книги
            автор: Автор книги
            наявність: Нова доступність

        Returns:
            bool: True, якщо книгу знайдено та оновлено
        """
        for book in self.books:
            if book.назва.lower() == назва.lower() and book.автор.lower() == автор.lower():
                old_status = book.наявність
                book.наявність = наявність
                self.save_books()

                status_text = "доступною" if наявність else "недоступною"
                print(f"✓ Книга '{назва}' тепер {status_text}")
                return True

        print(f"✗ Книгу '{назва}' від {автор} не знайдено")
        return False


def interactive_menu() -> None:
    """Інтерактивне меню для роботи з бібліотекою."""
    library = LibraryManager()

    while True:
        print("\n" + "=" * 50)
        print("🏛️  СИСТЕМА УПРАВЛІННЯ БІБЛІОТЕКОЮ")
        print("=" * 50)
        print("1. Показати доступні книги")
        print("2. Показати всі книги")
        print("3. Додати нову книгу")
        print("4. Знайти книги за автором")
        print("5. Знайти книги за назвою")
        print("6. Змінити доступність книги")
        print("7. Перезавантажити дані з файлу")
        print("0. Вийти")
        print("-" * 50)

        choice = input("Ваш вибір: ").strip()

        if choice == "1":
            library.display_available_books()

        elif choice == "2":
            library.display_all_books()

        elif choice == "3":
            print("\n➕ Додавання нової книги:")
            назва = input("Введіть назву книги: ").strip()
            автор = input("Введіть автора: ").strip()

            try:
                рік = int(input("Введіть рік видання: ").strip())
                доступна = input("Чи доступна книга? (y/n): ").strip().lower()
                наявність = доступна in ['y', 'yes', 'так', 'т', '1']

                library.add_book(назва, автор, рік, наявність)
            except ValueError:
                print("✗ Некоректний рік видання")

        elif choice == "4":
            автор = input("\n🔍 Введіть ім'я автора для пошуку: ").strip()
            books = library.find_books_by_author(автор)

            if books:
                print(f"\n📖 Знайдено {len(books)} книг автора '{автор}':")
                for i, book in enumerate(books, 1):
                    print(f"{i}. {book}")
            else:
                print(f"📭 Книг автора '{автор}' не знайдено")

        elif choice == "5":
            назва = input("\n🔍 Введіть назву для пошуку: ").strip()
            books = library.find_books_by_title(назва)

            if books:
                print(f"\n📖 Знайдено {len(books)} книг з назвою '{назва}':")
                for i, book in enumerate(books, 1):
                    print(f"{i}. {book}")
            else:
                print(f"📭 Книг з назвою '{назва}' не знайдено")

        elif choice == "6":
            print("\n🔄 Зміна доступності книги:")
            назва = input("Введіть назву книги: ").strip()
            автор = input("Введіть автора: ").strip()
            доступна = input("Зробити доступною? (y/n): ").strip().lower()
            наявність = доступна in ['y', 'yes', 'так', 'т', '1']

            library.update_book_availability(назва, автор, наявність)

        elif choice == "7":
            library.load_books()

        elif choice == "0":
            print("👋 До побачення!")
            break

        else:
            print("❌ Некоректний вибір. Спробуйте ще раз.")

        input("\nНатисніть Enter для продовження...")


def demo_usage() -> None:
    """Демонстрація використання системи."""
    print("🎯 ДЕМОНСТРАЦІЯ РОБОТИ СИСТЕМИ")
    print("=" * 40)

    # Створення менеджера бібліотеки
    library = LibraryManager("demo_books.json")

    # Показ доступних книг
    print("\n1️⃣ Показуємо доступні книги:")
    library.display_available_books()

    # Додавання нової книги
    print("\n2️⃣ Додаємо нову книгу:")
    library.add_book("Маруся Чурай", "Ліна Костенко", 1979, True)

    # Показ усіх книг
    print("\n3️⃣ Показуємо всі книги після додавання:")
    library.display_all_books()

    # Пошук за автором
    print("\n4️⃣ Шукаємо книги Ліни Костенко:")
    books_by_author = library.find_books_by_author("Ліна Костенко")
    for book in books_by_author:
        print(f"  📖 {book}")

    # Зміна доступності
    print("\n5️⃣ Змінюємо доступність книги:")
    library.update_book_availability("Захар Беркут", "Іван Франко", True)

    print("\n6️⃣ Остаточний список доступних книг:")
    library.display_available_books()


if __name__ == "__main__":
    print("Оберіть режим роботи:")
    print("1. Демонстрація")
    print("2. Інтерактивне меню")

    mode = input("Ваш вибір (1/2): ").strip()

    if mode == "1":
        demo_usage()
    else:
        interactive_menu()