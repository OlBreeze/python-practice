from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")
print("Connected to MongoDB")

# Выбираем базу данных
db = client["mydatabase"]
print(f"Selected Database: {db.name}")

# Выбираем коллекцию
collection = db["users"]
print(f"Selected collection: {collection.name}")

# ---------- Один документ ----------
user_data = {
    "name": "Ivan",
    "email": "ivan@example.com",
    "age": 25,
    "city": "Madrid",
    "interests": ["programming", "reading", "sports"],
    "status": "active"
}

result = collection.insert_one(user_data)
print(f"Inserted document with id: {result.inserted_id}")

# ---------- Несколько документов ----------
users_data = [
    {
        "name": "Max",
        "email": "max@example.com",
        "age": 22,
        "city": "London",
        "interests": ["communication", "reading", "sports"],
        "status": "not active"
    },
    {
        "name": "Anna",
        "email": "anna@example.com",
        "age": 28,
        "city": "Berlin",
        "interests": ["music", "travel", "art"],
        "status": "active"
    },
    {
        "name": "Olga",
        "email": "olga@example.com",
        "age": 30,
        "city": "Kyiv",
        "interests": ["cooking", "yoga", "design"],
        "status": "active"
    },
    {
        "name": "John",
        "email": "john@example.com",
        "age": 35,
        "city": "New York",
        "interests": ["finance", "reading", "chess"],
        "status": "not active"
    }
]

results = collection.insert_many(users_data)
print(f"Inserted documents with ids: {results.inserted_ids}")

# ---------- Вывод всех документов ----------
print("\nAll users in collection:")
for doc in collection.find():
    print(doc)
