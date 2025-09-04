class ValidateNumber:
    """Дескриптор для проверки положительных чисел"""

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{self.name} must be a number")
        if value <= 0:
            raise ValueError(f"{self.name} must be > 0")
        obj.__dict__[self.name] = value

    def __delete__(self, obj):
        del obj.__dict__[self.name]

#--------------------------------------------------------
class Book:
    """Класс для представления книги"""

    pages = ValidateNumber('_pages')

    def __init__(self, author, pages, rating):
        self.author = author
        self.pages = pages

        if not isinstance(rating, (int, float)):
            raise TypeError("Not a number!")
        if not 0 <= rating <= 10:
            raise ValueError("Rating must be from 0 untill 10")
        self.rating = rating

    def __add__(self, other):
        """Сложение книг - возвращает общее количество страниц"""
        if not isinstance(other, Book):
            raise TypeError("Its\'not a book!")
        return self.pages + other.pages

    def __eq__(self, other):
        """Сравнение книг на равенство по автору и количеству страниц"""
        if not isinstance(other, Book):
            return False
        return (self.author == other.author and
                self.pages == other.pages)

    def __str__(self):
        """Строковое представление книги"""
        return f"Книга: автор - {self.author}, страниц - {self.pages}, рейтинг - {self.rating}"

    def __len__(self):
        """Возвращает количество страниц"""
        return self.pages

#______---------------------------
# Примеры использования
if __name__ == "__main__":
    try:
        # Создание книг
        book1 = Book("Толстой", 1000, 9.5)
        book2 = Book("Достоевский", 800, 9.0)
        book3 = Book("Толстой", 1000, 9.5)

        print("=== Демонстрация методов ===")

        # __str__
        print("Строковое представление:")
        print(book1)
        print(book2)

        # __len__
        print(f"\nКоличество страниц в book1: {len(book1)}")

        # __add__
        print(f"\nОбщее количество страниц book1 + book2: {book1 + book2}")

        # __eq__
        print(f"\nbook1 == book2: {book1 == book2}")
        print(f"book1 == book3: {book1 == book3}")

        print("\n=== Проверка дескриптора ===")

        # Попытка создать книгу с отрицательным количеством страниц
        try:
            invalid_book = Book("Автор", -100, 5)
        except ValueError as e:
            print(f"Ошибка при создании книги с отрицательными страницами: {e}")

        # Попытка установить неположительное количество страниц
        try:
            book1.pages = 0
        except ValueError as e:
            print(f"Ошибка при установке нулевого количества страниц: {e}")

        # Попытка создать книгу с неверным рейтингом
        try:
            invalid_rating = Book("Автор", 200, 11)
        except ValueError as e:
            print(f"Ошибка при создании книги с неверным рейтингом: {e}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
#
#
# Створіть клас Book, який буде представляти книгу. Цей клас має:
# Використовувати дескриптор PositiveNumber для атрибутів pages (кількість сторінок) та rating (рейтинг від 0 до 10). Дескриптор повинен забезпечувати, що значення є додатним числом. Для рейтингу додатково перевірте, щоб значення було не більше 10.
# Використовувати dunder-методи для таких операцій:
# __add__: Дозволити додавати дві книги, створюючи "серію" (BookSeries). Уявіть, що ви просто додаєте об'єкти Book і отримуєте новий об'єкт, який містить обидві книги.
# __eq__: Дозволити порівнювати книги на рівність за назвою та автором.
# __str__: Створити зручне текстове представлення об'єкта книги.
# __len__: Дозволити дізнаватися кількість сторінок за допомогою len(book).
# Напишіть код для демонстрації роботи класу Book і дескриптора PositiveNumber.
# Кроки для виконання:
# Створіть дескриптор PositiveNumber.
# Створіть клас Book і прикріпіть дескриптор до атрибутів pages та rating.
# Реалізуйте необхідні dunder-методи.
# Створіть кілька об'єктів Book і перевірте їх роботу:
# Спробуйте створити книгу з від'ємною кількістю сторінок, щоб перевірити дескриптор.
# Додайте дві книги.
# Порівняйте дві однакові книги.
# Виведіть книгу на друк за допомогою print().