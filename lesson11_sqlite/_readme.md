# Лекция: Базы данных и SQL

## 1. Базовые концепции баз данных

### 1.1 Что такое база данных?
**База данных (БД)** — это организованная совокупность данных, которая позволяет:
- 📦 Хранить данные структурированно
- 🔄 Обрабатывать информацию
- 🔍 Получать быстрый доступ к данным

**Пример:** Таблица пользователей интернет-магазина с именами, email и возрастом.

### 1.2 Система управления базами данных (СУБД)
**СУБД** — это программное обеспечение для:
- Создания баз данных
- Управления данными
- Обеспечения безопасного доступа

**Примеры СУБД:** SQLite, PostgreSQL, MySQL, MongoDB

### 1.3 Типы баз данных

#### Реляционные БД
- ✅ Данные организованы в виде таблиц
- ✅ Стабильная структура
- ✅ Быстрый поиск информации
- ✅ Используются когда структура редко меняется

**Примеры:** SQLite, PostgreSQL, MySQL

#### Нереляционные БД (NoSQL)
- ✅ Гибкая структура данных
- ✅ Структура может часто меняться
- ✅ Подходят для стартапов и быстро развивающихся проектов

**Примеры:** MongoDB, Redis, Cassandra

---

## 2. Архитектура баз данных

### 2.1 SQLite — встроенная БД
- 📁 Хранится в одном файле
- 🚀 Не требует серверной части
- 💡 Идеальна для изучения и небольших проектов
- 🔧 Встроена в Python (модуль `sqlite3`)

### 2.2 Клиент-серверная модель
В полноценных СУБД:
- **Сервер** — хранит и обрабатывает данные
- **Клиент** — отправляет запросы к серверу
- **Запросы** — команды на языке SQL

---

## 3. Реляционная модель данных

### 3.1 Основные понятия

**Таблица** — основная структура для хранения данных
- Похожа на Excel таблицу
- Состоит из строк и столбцов

**Столбец (поле)** — характеристика объекта
- Например: `name`, `email`, `age`

**Строка (запись)** — конкретный объект
- Например: информация об одном пользователе

### 3.2 Типы данных в SQLite

| Тип | Описание | Пример |
|-----|----------|--------|
| `INTEGER` | Целые числа | 42, -10, 0 |
| `REAL` | Вещественные числа | 3.14, -0.5 |
| `TEXT` | Текстовые данные | "Иван", "email@test.com" |
| `BLOB` | Бинарные данные | Изображения, файлы |

### 3.3 Ключи

#### Primary Key (Первичный ключ)
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```
- 🔑 Уникальный идентификатор записи в таблице
- 🔢 Автоматически увеличивается при добавлении записей
- ⚠️ Не может повторяться

#### Foreign Key (Внешний ключ)
```sql
user_id INTEGER,
FOREIGN KEY (user_id) REFERENCES users(id)
```
- 🔗 Связывает таблицы между собой
- 📊 Создает отношения между данными

### 3.4 Ограничения (Constraints)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,           -- Обязательное поле
    email TEXT NOT NULL UNIQUE,   -- Уникальное значение
    age INTEGER
);
```

- `NOT NULL` — поле обязательно для заполнения
- `UNIQUE` — значение должно быть уникальным

---

## 4. Основы SQL

### 4.1 Группы команд SQL

#### DDL (Data Definition Language) — Определение структуры
- `CREATE` — создание таблиц
- `ALTER` — изменение структуры
- `DROP` — удаление таблиц

#### DML (Data Manipulation Language) — Манипуляция данными
- `INSERT` — вставка данных
- `UPDATE` — обновление данных
- `DELETE` — удаление данных

#### DQL (Data Query Language) — Запросы
- `SELECT` — выборка данных

### 4.2 Работа с SQLite в Python

#### Подключение к базе данных
```python
import sqlite3

# Создание подключения (файл создастся автоматически)
connection = sqlite3.connect('example.db')

# Создание курсора
cursor = connection.cursor()
```

#### Создание таблицы
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER
    )
''')

connection.commit()  # Фиксация изменений
```

#### Вставка данных
```python
# Один запись
cursor.execute('''
    INSERT INTO users (name, email, age)
    VALUES ('Иван', 'ivan@gmail.com', 25)
''')

# Множественная вставка
users_data = [
    ('Анна', 'anna@gmail.com', 22),
    ('Петр', 'petr@gmail.com', 30)
]
cursor.executemany('''
    INSERT INTO users (name, email, age)
    VALUES (?, ?, ?)
''', users_data)

connection.commit()
```

#### Выборка данных
```python
# Все записи
cursor.execute('SELECT * FROM users')
results = cursor.fetchall()
print(results)

# Одна запись
cursor.execute('SELECT * FROM users WHERE id = 1')
result = cursor.fetchone()
print(result)

# С условием
cursor.execute('SELECT name, age FROM users WHERE age > 25')
results = cursor.fetchall()
```

#### Закрытие соединения
```python
connection.close()

# Или использовать контекстный менеджер
with sqlite3.connect('example.db') as connection:
    cursor = connection.cursor()
    # Работа с базой данных
    # Автоматически закроется
```

### 4.3 Основные SQL команды

#### SELECT — Выборка данных
```sql
-- Все поля
SELECT * FROM users;

-- Конкретные поля
SELECT name, email FROM users;

-- С условием
SELECT * FROM users WHERE age > 18;

-- С сортировкой
SELECT * FROM users ORDER BY age DESC;

-- Ограничение количества
SELECT * FROM users LIMIT 5;

-- Пропуск первых записей
SELECT * FROM users LIMIT 5 OFFSET 3;
```

#### WHERE — Фильтрация
```sql
-- Точное совпадение
SELECT * FROM users WHERE name = 'Иван';

-- Поиск по шаблону
SELECT * FROM users WHERE name LIKE 'Ив%';

-- Несколько условий
SELECT * FROM users WHERE age > 18 AND age < 30;
```

#### UPDATE — Обновление
```sql
UPDATE users 
SET age = 26 
WHERE name = 'Иван';
```

#### DELETE — Удаление
```sql
DELETE FROM users WHERE id = 5;
```

### 4.4 Агрегатные функции

```sql
-- Количество записей
SELECT COUNT(*) FROM users;

-- Сумма
SELECT SUM(price) FROM products;

-- Среднее значение
SELECT AVG(age) FROM users;

-- Минимум и максимум
SELECT MIN(price), MAX(price) FROM products;

-- Группировка
SELECT age, COUNT(*) 
FROM users 
GROUP BY age;
```

### 4.5 JOIN — Объединение таблиц

```sql
-- INNER JOIN
SELECT customers.name, orders.order_id, products.product_name
FROM orders
JOIN customers ON orders.customer_id = customers.id
JOIN products ON orders.product_id = products.id;
```

---

## 5. Практический пример

### Создание базы данных магазина

```python
import sqlite3

# Подключение
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Таблица товаров
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER
    )
''')

# Таблица клиентов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
''')

# Таблица заказов
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id),
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
''')

# Добавление данных
cursor.execute("INSERT INTO products (name, price, quantity) VALUES ('Футболка', 15, 25)")
cursor.execute("INSERT INTO products (name, price, quantity) VALUES ('Штаны', 17, 20)")
cursor.execute("INSERT INTO customers (name, email) VALUES ('Иван', 'ivan@mail.com')")
cursor.execute("INSERT INTO customers (name, email) VALUES ('Анна', 'anna@mail.com')")
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (2, 1, 1)")
cursor.execute("INSERT INTO orders (customer_id, product_id, quantity) VALUES (1, 2, 2)")

conn.commit()

# Сложный запрос с JOIN
cursor.execute('''
    SELECT 
        orders.id AS order_id,
        customers.name AS customer_name,
        products.name AS product_name,
        orders.quantity,
        (products.price * orders.quantity) AS total_price
    FROM orders
    JOIN customers ON orders.customer_id = customers.id
    JOIN products ON orders.product_id = products.id
    ORDER BY orders.id
''')

results = cursor.fetchall()
for row in results:
    print(f"Заказ №{row[0]}: {row[1]} купил {row[2]} ({row[3]} шт.) на сумму {row[4]} руб.")

conn.close()
```

### Создание пользовательской агрегатной функции

```python
import sqlite3

class TotalRevenueAggregator:
    """Класс для подсчета общей выручки"""
    
    def __init__(self):
        self.total = 0
    
    def step(self, price, quantity):
        """Вызывается для каждой строки"""
        self.total += price * quantity
    
    def finalize(self):
        """Возвращает итоговый результат"""
        return self.total

# Регистрация функции
conn = sqlite3.connect('shop.db')
conn.create_aggregate("total_revenue", 2, TotalRevenueAggregator)

cursor = conn.cursor()
cursor.execute('''
    SELECT 
        products.id,
        products.name,
        total_revenue(products.price, orders.quantity) AS revenue
    FROM products
    JOIN orders ON products.id = orders.product_id
    GROUP BY products.id
''')

results = cursor.fetchall()
for row in results:
    print(f"Товар ID {row[0]}: {row[1]} - выручка {row[2]:.2f} руб.")

conn.close()
```

---

## 6. Частые ошибки и решения

### Проблема: UNIQUE constraint failed
```python
# Попытка добавить дубликат
# ОШИБКА: email уже существует

# Решение 1: INSERT OR IGNORE
cursor.execute('INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)', 
               ('Иван', 'ivan@mail.com'))

# Решение 2: INSERT OR REPLACE
cursor.execute('INSERT OR REPLACE INTO users (id, name, email) VALUES (?, ?, ?)', 
               (1, 'Иван', 'new_email@mail.com'))
```

### Не забывайте commit()
```python
cursor.execute('INSERT INTO users ...')
connection.commit()  # ❗ Без этого данные не сохранятся!
```

### Используйте параметризованные запросы
```python
# ❌ ПЛОХО (уязвимо для SQL-инъекций)
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# ✅ ХОРОШО
cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
```

---

## 7. Шпаргалка команд

### Основные операции
```sql
-- Создание таблицы
CREATE TABLE IF NOT EXISTS table_name (...)

-- Выборка
SELECT * FROM table_name WHERE condition

-- Вставка
INSERT INTO table_name (col1, col2) VALUES (val1, val2)

-- Обновление
UPDATE table_name SET col1 = val1 WHERE condition

-- Удаление
DELETE FROM table_name WHERE condition

-- Удаление таблицы
DROP TABLE IF EXISTS table_name
```

### Полезные операторы
```sql
LIKE       -- Поиск по шаблону: 'Ив%'
IN         -- Список значений: age IN (18, 20, 25)
BETWEEN    -- Диапазон: age BETWEEN 18 AND 30
IS NULL    -- Проверка на NULL
ORDER BY   -- Сортировка: ORDER BY age DESC
LIMIT      -- Ограничение: LIMIT 10
OFFSET     -- Пропуск записей: OFFSET 5
```

---

## 8. Практическое задание

### Задача: База данных университета

Создайте базу данных с тремя таблицами:

1. **students** — студенты
   - id, first_name, last_name, group_id

2. **groups** — группы
   - id, group_name, faculty

3. **grades** — оценки
   - id, student_id, subject, grade, grade_date

**Задания:**
1. Создайте все три таблицы с правильными связями
2. Добавьте 2-3 группы
3. Добавьте 5-7 студентов в разные группы
4. Добавьте оценки студентам
5. Напишите запрос для вывода рейтинга студентов по среднему баллу

---

## 9. Полезные ресурсы

- 📚 Документация SQLite: https://www.sqlite.org/docs.html
- 📚 Python sqlite3: https://docs.python.org/3/library/sqlite3.html
- 🔧 DB Browser for SQLite (визуальный инструмент)
- 💡 SQL Fiddle (онлайн практика)

---

## Ключевые выводы

✅ База данных — организованное хранилище данных  
✅ SQLite — простая встроенная БД для Python  
✅ Таблицы связываются через PRIMARY KEY и FOREIGN KEY  
✅ SQL имеет три группы команд: DDL, DML, DQL  
✅ Всегда используйте `commit()` для сохранения изменений  
✅ Закрывайте соединение или используйте контекстный менеджер  
✅ Агрегатные функции позволяют анализировать данные