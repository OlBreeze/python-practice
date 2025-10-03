import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Таблица продуктов
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL
                )''')
conn.commit()

# Таблица клиентов
cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL
                )''')
conn.commit()

# Таблица заказов
cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )''')
conn.commit()

conn.close()