# Створіть базу даних LibraryDB та колекції authors (Автори) та books (Книги).
# 2. Вставка даних:
# Автори: Вставте трьох авторів у колекцію authors.
# Книги: Вставте п'ять книг у колекцію books.
# Використовуйте _id автора як посилання (author_id) у документах книг
# (приклад: {"title": "The Hitchhiker's Guide to the Galaxy", "year": 1979, "author_id": author1_id, "genres": ["Sci-Fi", "Comedy"]}).
from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

# База Library
db = client.Library

# Колекції authors і books
authors = db.authors
books = db.books

# Очистимо колекції
authors.drop()
books.drop()

author_docs = [
    {"name": "Тарас Шевченко", "country": "Україна"},
    {"name": "Лев Толстой", "country": "Росія"},
    {"name": "Ернест Хемінгуей", "country": "США"}
]
author_ids = authors.insert_many(author_docs).inserted_ids

books_docs = [
    {"title": "Кобзар", "year": 1840, "author_id": author_ids[0], "genres": ["Поезія", "Класика"]},
    {"title": "Війна і мир", "year": 1869, "author_id": author_ids[1], "genres": ["Роман", "Історія"]},
    {"title": "Анна Кареніна", "year": 1877, "author_id": author_ids[1], "genres": ["Роман", "Драма"]},
    {"title": "Старий і море", "year": 1952, "author_id": author_ids[2], "genres": ["Повість", "Пригоди"]},
    {"title": "По кому подзвін", "year": 1940, "author_id": author_ids[2], "genres": ["Роман", "Війна"]}
]
books.insert_many(books_docs)

# --------------------------------------------
# Перевіримо результат
print("\nAuthors:")
for author in authors.find():
    print(author)

print("\nBooks:")
for book in books.find():
    print(book)
