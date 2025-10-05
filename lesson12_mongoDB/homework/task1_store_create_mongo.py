# Створіть базу даних для зберігання інформації про онлайн-магазин.
# Створіть колекцію products, яка містить дані про продукти
# (назва, ціна, категорія, кількість на складі).
# Створіть колекцію orders, яка містить інформацію про замовлення
# (номер замовлення, клієнт, список продуктів із кількістю, загальна сума).
"""
Онлайн-магазин
"""
from datetime import datetime, time

from pymongo import MongoClient

client = MongoClient(host="localhost", port=27017)

# База Store
db = client.Store


# Колекції products і orders
products = db.products
orders = db.orders

# Очистимо колекції
# Видаляє ВСЮ колекцію (колекція зникає повністю)
# products.drop()
# orders.drop()

# Видаляє всі документи, але колекція залишається
products.delete_many({})
orders.delete_many({})

# Видаляє всі документи з певною умовою
# products.delete_many({"stock": 0})

# 2. CRUD ОПЕРАЦІЇ - CREATE
# Додавання продуктів
start_time = time.time()
product_docs = [
    {
        "name": "Ноутбук Lenovo IdeaPad",
        "price": 25000,
        "category": "Електроніка",
        "stock": 15,
        "description": "15.6 дюймів, 8GB RAM, SSD 512GB"
    },
    {
        "name": "Смартфон Samsung Galaxy S23",
        "price": 30000,
        "category": "Електроніка",
        "stock": 25,
        "description": "128GB, 5G"
    },
    {
        "name": "Навушники Sony WH-1000XM5",
        "price": 12000,
        "category": "Аксесуари",
        "stock": 40,
        "description": "Бездротові, шумозаглушення"
    },
    {
        "name": "Клавіатура Logitech MX Keys",
        "price": 3500,
        "category": "Аксесуари",
        "stock": 30,
        "description": "Механічна, підсвітка"
    },
    {
        "name": "Монітор Dell 27\"",
        "price": 8500,
        "category": "Електроніка",
        "stock": 10,
        "description": "4K, IPS панель"
    },
{
    "name": "Ноутбук Lenovo IdeaPad",
    "price": 23000,
    "category": "Електроніка",
    "stock": 0,
    "description": "18.6 дюймів, 8GB RAM, SSD 512GB"
}
]
product_ids = products.insert_many(product_docs).inserted_ids

# Додавання замовлень
order_docs = [
    {
        "orderNumber": "ORD-001",
        "customer": {
            "name": "Іван Петренко",
            "email": "ivan@example.com",
            "phone": "+380501234567"
        },
        "products": [
            {"product_id": product_ids[0], "quantity": 1, "price": 25000},  # Ноутбук
            {"product_id": product_ids[2], "quantity": 1, "price": 12000}   # Навушники
        ],
        "totalAmount": 37000,
        "orderDate": datetime(2024, 9, 15),
        "status": "Доставлено"
    },
    {
        "orderNumber": "ORD-002",
        "customer": {
            "name": "Марія Коваленко",
            "email": "maria@example.com",
            "phone": "+380502345678"
        },
        "products": [
            {"product_id": product_ids[1], "quantity": 2, "price": 30000}  # Смартфон
        ],
        "totalAmount": 60000,
        "orderDate": datetime(2024, 9, 20),
        "status": "В обробці"
    },
    {
        "orderNumber": "ORD-003",
        "customer": {
            "name": "Олександр Шевченко",
            "email": "alex@example.com",
            "phone": "+380503456789"
        },
        "products": [
            {"product_id": product_ids[4], "quantity": 1, "price": 8500},  # Монітор
            {"product_id": product_ids[3], "quantity": 1, "price": 3500}   # Клавіатура
        ],
        "totalAmount": 12000,
        "orderDate": datetime(2024, 10, 1),
        "status": "Відправлено"
    },
    {
        "orderNumber": "ORD-004",
        "customer": {
            "name": "Наталія Бондаренко",
            "email": "natalia@example.com",
            "phone": "+380504567890"
        },
        "products": [
            {"product_id": product_ids[1], "quantity": 1, "price": 30000},  # Смартфон
            {"product_id": product_ids[2], "quantity": 2, "price": 12000}   # Навушники x2
        ],
        "totalAmount": 54000,
        "orderDate": datetime(2024, 10, 3),
        "status": "В обробці"
    },
    {
        "orderNumber": "ORD-005",
        "customer": {
            "name": "Дмитро Ковальчук",
            "email": "dmytro@example.com",
            "phone": "+380505678901"
        },
        "products": [
            {"product_id": product_ids[0], "quantity": 1, "price": 25000},  # Ноутбук
            {"product_id": product_ids[3], "quantity": 1, "price": 3500},   # Клавіатура
            {"product_id": product_ids[4], "quantity": 1, "price": 8500}    # Монітор
        ],
        "totalAmount": 37000,
        "orderDate": datetime(2024, 10, 4),
        "status": "Відправлено"
    }
]

order_ids = orders.insert_many(order_docs)
mongo_insert_time = time.time() - start_time
print(f"Час виконання INSERT: {mongo_insert_time*1000:.2f} мс")
# --------------------------------------------
# Перевіримо результат
print("\nProducts:")
for product in products.find():
    print(product)

print("\nOrders:")
for order in orders.find():
    print(order)

print(f" - Додано {len(product_ids)} продуктів")
print(f" - Додано {len(order_ids.inserted_ids)} замовлень")