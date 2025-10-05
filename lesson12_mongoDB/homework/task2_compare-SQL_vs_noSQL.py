"""
Порівняння SQL (SQLite) vs NoSQL (MongoDB)
Однакова модель даних: Онлайн-магазин
"""

import sqlite3
from pymongo import MongoClient
from datetime import datetime, timedelta
import time

print("ПОРІВНЯННЯ SQL (SQLite) vs NoSQL (MongoDB)")

# ============================================

print("1. SQLite (Реляційна база даних)")
print("-"*70)

# Підключення до SQLite
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# Створення таблиць
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
print("Таблиці SQL створено")

# ============================================
# SQL - CREATE (Insert)
# ============================================

print("\n CREATE операції (SQL)...")

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
    ("Іван Петренко", "ivan@41214example.com", "+380501234567"),
    ("Марія Коваленко", "maria@41124example.com", "+380502345678"),
    ("Олександр Шевченко", "alex@41214example.com", "+380503456789")
]

cursor.executemany('''
    INSERT INTO customers (name, email, phone)
    VALUES (?, ?, ?)
''', customers_sql)

# Додавання замовлень
cursor.execute('''
    INSERT INTO orders (order_number, customer_id, total_amount, order_date, status)
    VALUES ('Oц-001', 1, 37000, ?, 'Доставлено')
''', (datetime(2024, 9, 15),))
order1_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO order_items (order_id, product_id, quantity, price)
    VALUES (?, 1, 1, 25000), (?, 3, 1, 12000)
''', (order1_id, order1_id))

cursor.execute('''
    INSERT INTO orders (order_number, customer_id, total_amount, order_date, status)
    VALUES ('Oц-002', 2, 60000, ?, 'В обробці')
''', (datetime(2024, 9, 20),))
order2_id = cursor.lastrowid

cursor.execute('''
    INSERT INTO order_items (order_id, product_id, quantity, price)
    VALUES (?, 2, 2, 30000)
''', (order2_id,))

conn.commit()
print(f"SQL INSERT: {len(products_sql)} продуктів, {len(customers_sql)} клієнтів, 2 замовлення")
print(f"Час виконання INSERT: {sql_insert_time*1000:.2f} мс")

# SQL - READ (Select)
print("\nREAD операції (SQL)...")

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

print(f"Замовлення за останні 30 днів:")
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

# SQL - UPDATE
print("\nUPDATE операції (SQL)...")

start_time = time.time()
cursor.execute('''
    UPDATE products
    SET stock = stock - 2
    WHERE name = 'Ноутбук Lenovo IdeaPad'
''')
sql_update_time = time.time() - start_time

conn.commit()
print(f"Оновлено запас продукту")
print(f"Час виконання UPDATE: {sql_update_time*1000:.2f} мс")

# SQL - DELETE
print("\nDELETE операції (SQL)...")

start_time = time.time()
cursor.execute('DELETE FROM products WHERE stock = 0')
sql_delete_time = time.time() - start_time

conn.commit()
print(f"Видалено продукти без запасу")
print(f"Час виконання DELETE: {sql_delete_time*1000:.2f} мс")

# SQL - Агрегація
print("\nАГРЕГАЦІЯ (SQL)...")

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

print("\nТоп продуктів:")
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

print("\nСтатистика клієнта:")
for row in cursor.fetchall():
    print(f"  Ім'я: {row[0]}")
    print(f"  Email: {row[1]}")
    print(f"  Замовлень: {row[2]}")
    print(f"  Загальна сума: {row[3]} грн")
    print(f"  Середня сума: {row[4]:.2f} грн")

# SQL - Індекси
print("\nІНДЕКСИ (SQL)...")

cursor.execute('CREATE INDEX IF NOT EXISTS idx_product_category ON products(category)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_customer_email ON customers(email)')

conn.commit()
print("Створено індекси для category, order_date, email")

conn.close()

# ЧАСТИНА 2: MongoDB (NoSQL)
print("2. NoSQL - MongoDB - дивитись таск1")




print(f"""
│ Операція                │ SQL (SQLite)   
├─────────────────────────┼───────────────────────────
│ INSERT                  │ {sql_insert_time*1000:>7.2f} мс     
│ SELECT/FIND             │ {sql_read_time*1000:>7.2f} мс      
│ UPDATE                  │ {sql_update_time*1000:>7.2f} мс      
│ DELETE                  │ {sql_delete_time*1000:>7.2f} мс      
└─────────────────────────┴───────────────────────────
ВИСНОВОК  - SQL в мене швидше)
""")

