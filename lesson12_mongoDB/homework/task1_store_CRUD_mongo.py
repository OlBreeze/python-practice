"""
Онлайн-магазин
"""
from datetime import datetime, timedelta

from pymongo import MongoClient, ASCENDING, DESCENDING
import time

client = MongoClient('mongodb://localhost:27017/')

# Створення/вибір бази даних
db = client.Store

# Колекції products і orders
products = db.products
orders = db.orders

print("\nREAD ОПЕРАЦІЇ:")
start_time = time.time()
# Витягнути всі замовлення за останні 30 днів
thirty_days_ago = datetime.now() - timedelta(days=30)

recent_orders = orders.find({
    "orderDate": {"$gte": thirty_days_ago}
})

print(f"\nЗамовлення за останні 30 днів:")
for order in recent_orders:
    print(f"  - {order['orderNumber']}: {order['customer']['name']} - {order['totalAmount']} грн")
mongo_read_time = time.time() - start_time
# ------------------------

# Знайти всі продукти певної категорії
electronics = products.find({"category": "Електроніка"})
print(f"\nЕлектроніка:")
for product in electronics:
    print(f"  - {product['name']}: {product['price']} грн (запас: {product['stock']})")

print("\nUPDATE ОПЕРАЦІЇ:")

# Оновити кількість продукту на складі після покупки (куплено 2 ноутбуки)
start_time = time.time()
result = products.update_one(
    {"name": "Ноутбук Lenovo IdeaPad"},
    {"$inc": {"stock": -2}}
)
mongo_update_time = time.time() - start_time

print(f"Час виконання UPDATE: {mongo_update_time*1000:.2f} мс")
print(f"Оновлено запас ноутбуків (змінено документів: {result.modified_count})")

# Оновити статус замовлення
result = orders.update_one(
    {"orderNumber": "ORD-002"},
    {"$set": {"status": "Доставлено"}}
)
print(f"Оновлено статус замовлення (змінено документів: {result.modified_count})")

print("\nDELETE ОПЕРАЦІЇ:")
start_time = time.time()
# Видалити продукти, які більше не доступні (stock = 0)
result = products.delete_many({"stock": 0})
mongo_delete_time = time.time() - start_time

print(f"Час виконання DELETE: {mongo_delete_time*1000:.2f} мс")
print(f"Видалено продукти без запасу (видалено: {result.deleted_count})")

print("\nАГРЕГАЦІЯ ДАНИХ:")

# Порахувати загальну кількість проданих продуктів за період/ # дивитись в файлi pipeline.md детальне пояснення !!!
pipeline1 = [
    {
        "$match": {
            "orderDate": {
                "$gte": datetime(2024, 9, 1),
                "$lte": datetime(2024, 9, 30)
            }
        }
    },
    {"$unwind": "$products"}, # дивитись в файлi pipeline.md детальне пояснення !!!
    {
        "$group": {
            "_id": "$products.name",
            "totalQuantity": {"$sum": "$products.quantity"},
            "totalRevenue": {
                "$sum": {
                    "$multiply": ["$products.quantity", "$products.price"]
                }
            }
        }
    },
    {"$sort": {"totalQuantity": -1}}
]

print("\nПродані продукти за вересень 2024:")
for item in orders.aggregate(pipeline1):
    print(f"  - {item['_id']}: {item['totalQuantity']} шт, виручка: {item['totalRevenue']} грн")

# Підрахунок загальної суми всіх замовлень конкретного клієнта / # дивитись в файлi pipeline.md детальне пояснення !!!
pipeline2 = [
    {"$match": {"customer.email": "ivan@example.com"}},
    {
        "$group": {
            "_id": "$customer.email",
            "customerName": {"$first": "$customer.name"},
            "totalOrders": {"$sum": 1},
            "totalSpent": {"$sum": "$totalAmount"},
            "avgOrderAmount": {"$avg": "$totalAmount"}
        }
    }
]

print("\nСтатистика клієнта ivan@example.com:")
for stat in orders.aggregate(pipeline2):
    print(f"  Ім'я: {stat['customerName']}")
    print(f"  Всього замовлень: {stat['totalOrders']}")
    print(f"  Загальна сума: {stat['totalSpent']} грн")
    print(f"  Середня сума замовлення: {stat['avgOrderAmount']:.2f} грн")

print("\nСТВОРЕННЯ ІНДЕКСІВ:")

# Створити індекс для поля category
products.create_index([("category", ASCENDING)])
print("Створено індекс для category")

# Створити текстовий індекс для пошуку
products.create_index([("name", "text"), ("description", "text")])
print("Створено текстовий індекс для name та description")

# всі індекси
print("\nІндекси колекції products:")
for index in products.list_indexes():
    print(f"  - {index['name']}: {index.get('key', {})}")

# Приклад використання текстового пошуку
print("\nТекстовий пошук 'бездротові':")
for product in products.find({"$text": {"$search": "бездротові"}}):
    print(f"  - {product['name']}: {product['description']}")

# Клієнти з найбільшою кількістю замовлень
pipeline_top_customers = [
    {
        "$group": {
            "_id": "$customer.email",
            "customerName": {"$first": "$customer.name"},
            "orderCount": {"$sum": 1},
            "totalSpent": {"$sum": "$totalAmount"}
        }
    },
    {"$sort": {"orderCount": -1}},
    {"$limit": 10}
]

client.close()

print(f"""
│ Операція                │ NoSQL (MongoDB)                           
├─────────────────────────┼──────────────────────────────
│ SELECT/FIND             │  {mongo_read_time*1000:>7.2f} мс         
│ UPDATE                  │  {mongo_update_time*1000:>7.2f} мс        
│ DELETE                  │  {mongo_delete_time*1000:>7.2f} мс        
└─────────────────────────┴──────────────────────────────
""")