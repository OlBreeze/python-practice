from pymongo import MongoClient

# Подключение к локальному серверу MongoDB
client = MongoClient(host="localhost", port=27017)

# Выбор базы данных и коллекции
db = client.mydatabase
collection = db.users

# Удаление одного документа (например, где name = "Yana")
delete_filter_yana = {"name": "Yana"}
result_delete_one = collection.delete_one(delete_filter_yana)
print(f"Documents removed (Yana): {result_delete_one.deleted_count}")

# Проверка, что Yana больше нет
if collection.find_one({"name": "Yana"}) is None:
    print("User Yana has been successfully deleted.")

# Удаление всех документов, где возраст > 23
delete_filter_age = {"age": {"$gt": 23}}
result_delete_many = collection.delete_many(delete_filter_age)
print(f"Documents removed (over 23): {result_delete_many.deleted_count}")

# Подсчёт оставшихся документов
remaining_count = collection.count_documents({})
print(f"Documents left in the collection: {remaining_count}")

# Вывод оставшихся документов
print("Remaining users:")
for user in collection.find():
    print(user)

# ⚠️ Осторожно: удаление ВСЕХ документов из коллекции
# collection.delete_many({})
# print("All documents in the collection have been deleted.")
