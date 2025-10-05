from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

# База Library
db = client.Library

# Колекції authors і books
authors = db.authors
books = db.books

print("\nAuthors:")
for author in authors.find():
    print(author)

print("\nBooks:")
for book in books.find():
    print(book)
