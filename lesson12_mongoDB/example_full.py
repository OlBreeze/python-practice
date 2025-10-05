from pymongo import MongoClient

# Подключение к MongoDB (локально)
client = MongoClient("mongodb://localhost:27017/")
print("✅ Connected to MongoDB")

# Выбираем базу и коллекцию
db = client["mydatabase"]
collection = db["users"]

# Очистим коллекцию для чистого запуска
collection.drop()

# ---------- CREATE ----------
print("\n=== INSERT DOCUMENTS ===")
user = {"name": "Ivan", "age": 25, "city": "Madrid", "status": "active"}
collection.insert_one(user)

users = [
    {"name": "Anna", "age": 28, "city": "Berlin", "status": "active"},
    {"name": "John", "age": 35, "city": "New York", "status": "not active"},
    {"name": "Olga", "age": 30, "city": "Kyiv", "status": "active"},
    {"name": "Max", "age": 22, "city": "London", "status": "not active"}
]
collection.insert_many(users)

print("Inserted users successfully!")

# ---------- READ ----------
print("\n=== FIND ALL USERS ===")
for doc in collection.find():
    print(doc)

print("\n=== FIND ONE USER (Ivan) ===")
print(collection.find_one({"name": "Ivan"}))

print("\n=== FILTER (age > 27) ===")
for doc in collection.find({"age": {"$gt": 27}}):
    print(doc)

print("\n=== FILTER (city=Kyiv AND status=active) ===")
for doc in collection.find({"$and": [{"city": "Kyiv"}, {"status": "active"}]}):
    print(doc)

print("\n=== PROJECTION (only name, city) ===")
for doc in collection.find({}, {"name": 1, "city": 1, "_id": 0}):
    print(doc)

# ---------- UPDATE ----------
print("\n=== UPDATE ONE (Ivan -> city=Barcelona) ===")
collection.update_one(
    {"name": "Ivan"},
    {"$set": {"city": "Barcelona"}}
)
print(collection.find_one({"name": "Ivan"}))

print("\n=== UPDATE MANY (set all not active -> active) ===")
collection.update_many(
    {"status": "not active"},
    {"$set": {"status": "active"}}
)
for doc in collection.find():
    print(doc)

# ---------- DELETE ----------
print("\n=== DELETE ONE (John) ===")
collection.delete_one({"name": "John"})
for doc in collection.find():
    print(doc)

print("\n=== DELETE MANY (age < 28) ===")
collection.delete_many({"age": {"$lt": 28}})
for doc in collection.find():
    print(doc)

# ---------- SORT & LIMIT ----------
print("\n=== SORT BY AGE DESC, LIMIT 2 ===")
for doc in collection.find().sort("age", -1).limit(2):
    print(doc)

# ---------- AGGREGATION ----------
print("\n=== AGGREGATION: count users by city ===")
pipeline = [
    {"$group": {"_id": "$city", "count": {"$sum": 1}}}
]
for doc in collection.aggregate(pipeline):
    print(doc)
