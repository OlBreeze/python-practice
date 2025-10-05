"""
Порівняння SQL (SQLite) vs NoSQL (MongoDB)
Однакова модель даних: Онлайн-магазин

Встановлення:
pip install pymongo
"""

import sqlite3
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import time

print("="*70)
print("ПОРІВНЯННЯ SQL (SQLite) vs NoSQL (MongoDB)")
print("="*70)

# ============================================
# ЧАСТИНА 1: SQLite (Реляційна БД)
# ============================================

print("\n" + "="*70)
print("1️⃣  SQL - SQLite (Реляційна база даних)")
print("="*70)

# Підключення до SQLite
conn = sqlite3.connect('online_shop.db')
cursor = conn.cursor()

# Створення таблиць з нормалізованою структурою
print("\n📋 Створення таблиць...")

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    customer_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    order_date DATETIME NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
''')

conn.commit()
print("✅ Таблиці створено")

# ============================================
# SQL - CREATE (Insert)
# ============================================

print("\n📝 CREATE операції (SQL)...")

# Додавання продуктів
products_sql = [
    ("Ноутбук Lenovo IdeaPad", 25000, "Електроніка", 15, "15.6 дюймів, 8GB RAM, SSD 512GB"),
    ("Смартфон Samsung Galaxy S23", 30000, "Електроніка", 25, "128GB, 5G"),
    ("Навушники Sony WH-1000XM5", 12000, "Аксесуари", 40, "Бездротові, шумозаглушення"),
    ("Клавіатура Logitech MX Keys", 3500, "Аксесуари", 30, "Механічна, підсвітка"),
    ("Монітор Dell 27\"", 8500, "Електроніка", 10, "4K, IPS панель")
]

start_time = time.time()
cursor.executemany('''
    INSERT INTO products (name, price, category, stock, description)
    VALUES (?, ?, ?, ?, ?)
''', products_sql)
sql_insert_time = time.time() - start_time

# Додавання клієнтів
customers_sql = [
    ("Іван Петренко", "ivan@example.com", "+380501234567"),
    ("Марія Коваленко", "maria@example.com", "+380502345678"),
    ("Олександр Шевченко", "alex@example.com", "+380503456789")
]

cursor.executemany('''
    INSERT INTO customers (name, email, phone)
    VALUES (?, ?, ?)
''', customers_sql)

# Додавання замовлень
cursor.execute('''
    INSERT INTO orders (order_number, customer_id, total_amount, order_date, status)
    VALUES ('ORD-001', 1, 37000, ?, 'Доставлено')
''', (datetime(2024, 9, 15),))
order1_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO order_items (order_id, product_id, quantity, price)
    VALUES (?, 1, 1, 25000), (?, 3, 1, 12000)
''', (order1_id, order1_id))

cursor.execute('''
    INSERT INTO orders (order_number, customer_id, total_amount, order_date, status)
    VALUES ('ORD-002', 2, 60000, ?, 'В обробці')
''', (datetime(2024, 9, 20),))
order2_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO order_items (order_id, product_id, quantity, price)
    VALUES (?, 2, 2, 30000)
''', (order2_id,))

conn.commit()
print(f"✅ SQL INSERT: {len(products_sql)} продуктів, {len(customers_sql)} клієнтів, 2 замовлення")
print(f"⏱️  Час виконання INSERT: {sql_insert_time*1000:.2f} мс")

# ============================================
# SQL - READ (Select)
# ============================================

print("\n📖 READ операції (SQL)...")

start_time = time.time()

# Замовлення за останні 30 днів
thirty_days_ago = datetime.now() - timedelta(days=30)
cursor.execute('''
    SELECT o.order_number, c.name, o.total_amount, o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    WHERE o.order_date >= ?
''', (thirty_days_ago,))

sql_read_time = time.time() - start_time

print(f"🔍 Замовлення за останні 30 днів:")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]} - {row[2]} грн ({row[3]})")
print(f"⏱️  Час виконання SELECT: {sql_read_time*1000:.2f} мс")

# Детальна інформація про замовлення
cursor.execute('''
    SELECT 
        o.order_number,
        c.name as customer_name,
        c.email,
        p.name as product_name,
        oi.quantity,
        oi.price,
        o.status
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN products p ON oi.product_id = p.id
    WHERE o.order_number = 'ORD-001'
''')

print(f"\n📦 Детальна інформація про замовлення ORD-001:")
for row in cursor.fetchall():
    print(f"  Клієнт: {row[1]} ({row[2]})")
    print(f"  Продукт: {row[3]} - {row[4]} шт × {row[5]} грн")
    print(f"  Статус: {row[6]}")

# ============================================
# SQL - UPDATE
# ============================================

print("\n✏️  UPDATE операції (SQL)...")

start_time = time.time()
cursor.execute('''
    UPDATE products
    SET stock = stock - 2
    WHERE name = 'Ноутбук Lenovo IdeaPad'
''')
sql_update_time = time.time() - start_time

conn.commit()
print(f"✅ Оновлено запас продукту")
print(f"⏱️  Час виконання UPDATE: {sql_update_time*1000:.2f} мс")

# ============================================
# SQL - DELETE
# ============================================

print("\n🗑️  DELETE операції (SQL)...")

start_time = time.time()
cursor.execute('DELETE FROM products WHERE stock = 0')
sql_delete_time = time.time() - start_time

conn.commit()
print(f"✅ Видалено продукти без запасу")
print(f"⏱️  Час виконання DELETE: {sql_delete_time*1000:.2f} мс")

# ============================================
# SQL - Агрегація
# ============================================

print("\n📊 АГРЕГАЦІЯ (SQL)...")

# Топ продуктів
cursor.execute('''
    SELECT 
        p.name,
        p.category,
        SUM(oi.quantity) as total_sold,
        SUM(oi.quantity * oi.price) as revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.id
    ORDER BY total_sold DESC
    LIMIT 5
''')

print("\n🏆 Топ продуктів:")
for row in cursor.fetchall():
    print(f"  - {row[0]} ({row[1]}): {row[2]} шт, виручка: {row[3]} грн")

# Статистика клієнта
cursor.execute('''
    SELECT 
        c.name,
        c.email,
        COUNT(o.id) as total_orders,
        SUM(o.total_amount) as total_spent,
        AVG(o.total_amount) as avg_order
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE c.email = 'ivan@example.com'
    GROUP BY c.id
''')

print("\n👤 Статистика клієнта:")
for row in cursor.fetchall():
    print(f"  Ім'я: {row[0]}")
    print(f"  Email: {row[1]}")
    print(f"  Замовлень: {row[2]}")
    print(f"  Загальна сума: {row[3]} грн")
    print(f"  Середня сума: {row[4]:.2f} грн")

# ============================================
# SQL - Індекси
# ============================================

print("\n🔍 ІНДЕКСИ (SQL)...")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_category ON products(category)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_email ON customers(email)')

conn.commit()
print("✅ Створено індекси для category, order_date, email")

conn.close()

# ============================================
# ЧАСТИНА 2: MongoDB (NoSQL)
# ============================================

print("\n" + "="*70)
print("2️⃣  NoSQL - MongoDB (Документо-орієнтована БД)")
print("="*70)

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['online_shop_nosql']

# Очистка колекцій
db.products.drop()
db.orders.drop()

print("\n📋 Створення колекцій...")
print("✅ Колекції створено (автоматично)")

# ============================================
# MongoDB - CREATE (Insert)
# ============================================

print("\n📝 CREATE операції (MongoDB)...")

products_mongo = [
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
    }
]

start_time = time.time()
product_ids = db.products.insert_many(products_mongo).inserted_ids
mongo_insert_time = time.time() - start_time

# Додавання замовлень (вбудована структура)
orders_mongo = [
    {
        "orderNumber": "ORD-001",
        "customer": {
            "name": "Іван Петренко",
            "email": "ivan@example.com",
            "phone": "+380501234567"
        },
        "products": [
            {"product_id": product_ids[0], "name": "Ноутбук Lenovo IdeaPad", "quantity": 1, "price": 25000},
            {"product_id": product_ids[2], "name": "Навушники Sony WH-1000XM5", "quantity": 1, "price": 12000}
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
            {"product_id": product_ids[1], "name": "Смартфон Samsung Galaxy S23", "quantity": 2, "price": 30000}
        ],
        "totalAmount": 60000,
        "orderDate": datetime(2024, 9, 20),
        "status": "В обробці"
    }
]

db.orders.insert_many(orders_mongo)

print(f"✅ MongoDB INSERT: {len(products_mongo)} продуктів, 2 замовлення")
print(f"⏱️  Час виконання INSERT: {mongo_insert_time*1000:.2f} мс")

# ============================================
# MongoDB - READ (Find)
# ============================================

print("\n📖 READ операції (MongoDB)...")

start_time = time.time()

thirty_days_ago = datetime.now() - timedelta(days=30)
recent_orders = db.orders.find({
    "orderDate": {"$gte": thirty_days_ago}
})

mongo_read_time = time.time() - start_time

print(f"🔍 Замовлення за останні 30 днів:")
for order in recent_orders:
    print(f"  - {order['orderNumber']}: {order['customer']['name']} - {order['totalAmount']} грн ({order['status']})")
print(f"⏱️  Час виконання FIND: {mongo_read_time*1000:.2f} мс")

# Детальна інформація (вже вбудована!)
order_detail = db.orders.find_one({"orderNumber": "ORD-001"})
print(f"\n📦 Детальна інформація про замовлення ORD-001:")
print(f"  Клієнт: {order_detail['customer']['name']} ({order_detail['customer']['email']})")
for p in order_detail['products']:
    print(f"  Продукт: {p['name']} - {p['quantity']} шт × {p['price']} грн")
print(f"  Статус: {order_detail['status']}")

# ============================================
# MongoDB - UPDATE
# ============================================

print("\n✏️  UPDATE операції (MongoDB)...")

start_time = time.time()
result = db.products.update_one(
    {"name": "Ноутбук Lenovo IdeaPad"},
    {"$inc": {"stock": -2}}
)
mongo_update_time = time.time() - start_time

print(f"✅ Оновлено запас продукту")
print(f"⏱️  Час виконання UPDATE: {mongo_update_time*1000:.2f} мс")

# ============================================
# MongoDB - DELETE
# ============================================

print("\n🗑️  DELETE операції (MongoDB)...")

start_time = time.time()
result = db.products.delete_many({"stock": 0})
mongo_delete_time = time.time() - start_time

print(f"✅ Видалено продукти без запасу")
print(f"⏱️  Час виконання DELETE: {mongo_delete_time*1000:.2f} мс")

# ============================================
# MongoDB - Агрегація
# ============================================

print("\n📊 АГРЕГАЦІЯ (MongoDB)...")

# Топ продуктів
pipeline = [
    {"$unwind": "$products"},
    {
        "$lookup": {
            "from": "products",
            "localField": "products.product_id",
            "foreignField": "_id",
            "as": "product_info"
        }
    },
    {"$unwind": "$product_info"},
    {
        "$group": {
            "_id": "$products.product_id",
            "name": {"$first": "$product_info.name"},
            "category": {"$first": "$product_info.category"},
            "totalSold": {"$sum": "$products.quantity"},
            "revenue": {"$sum": {"$multiply": ["$products.quantity", "$products.price"]}}
        }
    },
    {"$sort": {"totalSold": -1}},
    {"$limit": 5}
]

print("\n🏆 Топ продуктів:")
for item in db.orders.aggregate(pipeline):
    print(f"  - {item['name']} ({item['category']}): {item['totalSold']} шт, виручка: {item['revenue']} грн")

# Статистика клієнта
pipeline2 = [
    {"$match": {"customer.email": "ivan@example.com"}},
    {
        "$group": {
            "_id": "$customer.email",
            "name": {"$first": "$customer.name"},
            "totalOrders": {"$sum": 1},
            "totalSpent": {"$sum": "$totalAmount"},
            "avgOrder": {"$avg": "$totalAmount"}
        }
    }
]

print("\n👤 Статистика клієнта:")
for stat in db.orders.aggregate(pipeline2):
    print(f"  Ім'я: {stat['name']}")
    print(f"  Email: {stat['_id']}")
    print(f"  Замовлень: {stat['totalOrders']}")
    print(f"  Загальна сума: {stat['totalSpent']} грн")
    print(f"  Середня сума: {stat['avgOrder']:.2f} грн")

# ============================================
# MongoDB - Індекси
# ============================================

print("\n🔍 ІНДЕКСИ (MongoDB)...")

db.products.create_index([("category", 1)])
db.orders.create_index([("orderDate", -1)])
db.orders.create_index([("customer.email", 1)])

print("✅ Створено індекси для category, orderDate, customer.email")

client.close()

# ============================================
# ПОРІВНЯЛЬНИЙ АНАЛІЗ
# ============================================

print("\n" + "="*70)
print("📊 ПОРІВНЯЛЬНИЙ АНАЛІЗ SQL vs NoSQL")
print("="*70)

print(f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    ПРОДУКТИВНІСТЬ ОПЕРАЦІЙ                          │
├─────────────────────────┬─────────────────┬─────────────────────────┤
│ Операція                │ SQL (SQLite)    │ NoSQL (MongoDB)         │
├─────────────────────────┼─────────────────┼─────────────────────────┤
│ INSERT                  │ {sql_insert_time*1000:>7.2f} мс      │ {mongo_insert_time*1000:>7.2f} мс            │
│ SELECT/FIND             │ {sql_read_time*1000:>7.2f} мс      │ {mongo_read_time*1000:>7.2f} мс            │
│ UPDATE                  │ {sql_update_time*1000:>7.2f} мс      │ {mongo_update_time*1000:>7.2f} мс            │
│ DELETE                  │ {sql_delete_time*1000:>7.2f} мс      │ {mongo_delete_time*1000:>7.2f} мс            │
└─────────────────────────┴─────────────────┴─────────────────────────┘
""")

print("""
┌─────────────────────────────────────────────────────────────────────┐
│                   ПЕРЕВАГИ ТА НЕДОЛІКИ                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ✅ SQL (SQLite) - ПЕРЕВАГИ:                                         │
│                                                                     │
│  1. ACID транзакції - гарантована консистентність даних            │
│  2. Нормалізація - немає дублювання даних                          │
│  3. Строга типізація - захист від помилок                          │
│  4. Складні JOIN запити - легко зв'язувати таблиці                 │
│  5. Стандартизація - SQL підтримується скрізь                      │
│  6. Схема даних - чітка структура                                  │
│  7. Зрілість - перевірені роками технології                        │
│                                                                     │
│ ❌ SQL (SQLite) - НЕДОЛІКИ:                                         │
│                                                                     │
│  1. Жорстка схема - важко змінювати структуру                      │
│  2. Вертикальне масштабування - складно розподілити навантаження   │
│  3. JOIN операції - можуть бути повільними                         │
│  4. Складність міграцій - зміна схеми вимагає зусиль               │
│  5. Обмежена гнучкість - всі записи мають однакову структуру       │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ ✅ NoSQL (MongoDB) - ПЕРЕВАГИ:                                      │
│                                                                     │
│  1. Гнучка схема - можна зберігати різні структури                 │
│  2. Горизонтальне масштабування - легко додавати сервери           │
│  3. Вбудовані документи - немає потреби в JOIN                     │
│  4. Швидкість читання - денормалізовані дані                       │
│  5. JSON формат - природно для веб-додатків                        │
│  6. Агрегація - потужний pipeline для аналітики                    │
│  7. Швидка розробка - не потрібно проектувати схему заздалегідь    │
│                                                                     │
│ ❌ NoSQL (MongoDB) - НЕДОЛІКИ:                                      │
│                                                                     │
│  1. Дублювання даних - може бути багато копій                      │
│  2. Складність оновлень - треба оновлювати в кількох місцях        │
│  3. Немає JOIN - складніше зв'язувати дані                         │
│  4. Менша консистентність - eventual consistency                   │
│  5. Розмір даних - денормалізація збільшує обсяг                   │
│  6. Складність транзакцій - не всі операції атомарні               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│              КОЛИ ВИКОРИСТОВУВАТИ SQL vs NoSQL                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 🎯 ВИКОРИСТОВУЙТЕ SQL, ЯКЩО:                                        │
│                                                                     │
│  • Потрібні ACID транзакції (банки, фінанси)                       │
│  • Складні зв'язки між даними (ERP, CRM системи)                   │
│  • Чітка структура даних (інвентаризація, бухгалтерія)             │
│  • Важлива консистентність (медичні системи)                       │
│  • Багато JOIN запитів (аналітика)                                 │
│  • Невеликі/середні обсяги даних                                   │
│                                                                     │
│ Приклади: Банківські системи, ERP, CRM, E-commerce з інвентарем    │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ 🎯 ВИКОРИСТОВУЙТЕ NoSQL, ЯКЩО:                                      │
│                                                                     │
│  • Дані часто змінюють структуру (стартапи, прототипи)             │
│  • Потрібне горизонтальне масштабування (великі навантаження)      │
│  • Вбудовані документи природні для моделі (блоги, соцмережі)      │
│  • Швидкість читання критична (каталоги, контент)                  │
│  • Працюєте з великими даними (логи, IoT)                          │
│  • Гнучкість важливіша за консистентність                          │
│                                                                     │
│ Приклади: Соціальні мережі, блоги, IoT, логування, каталоги товарів│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    ГІБРИДНИЙ ПІДХІД                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ Часто найкращим рішенням є використання ОБОХ:                      │
│                                                                     │
│  • SQL для критичних даних (транзакції, користувачі)               │
│  • NoSQL для масштабованих частин (логи, кеш, сесії)               │
│                                                                     │
│ Приклад: E-commerce                                                 │
│  → SQL: Замовлення, платежі, інвентар                              │
│  → NoSQL: Каталог товарів, відгуки, рекомендації                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

print("\n" + "="*70)
print("✅ Порівняння завершено!")
print("="*70)