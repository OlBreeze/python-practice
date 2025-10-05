# SQL vs NoSQL - Детальне порівняння

## 📊 Частина 2: Порівняння PostgreSQL і MongoDB

### 1. Модель даних

#### **PostgreSQL (SQL)**
```
Реляційна модель з жорсткою схемою:

customers              products              orders
├─ customer_id (PK)    ├─ product_id (PK)   ├─ order_id (PK)
├─ name                ├─ name              ├─ order_number
├─ email               ├─ price             ├─ customer_id (FK)
├─ phone               ├─ category          ├─ total_amount
└─ created_at          ├─ stock             ├─ status
                       └─ created_at        └─ order_date

order_items
├─ order_item_id (PK)
├─ order_id (FK)
├─ product_id (FK)
├─ quantity
└─ price
```

**Особливості:**
- Дані нормалізовані (розподілені по таблицях)
- Зв'язки через зовнішні ключі (Foreign Keys)
- Жорстка схема (потрібно ALTER TABLE для змін)
- ACID-транзакції з гарантіями

#### **MongoDB (NoSQL)**
```json
products колекція:
{
  "_id": ObjectId,
  "name": "Ноутбук Lenovo",
  "price": 25000,
  "category": "Електроніка",
  "stock": 15,
  "created_at": ISODate
}

orders колекція:
{
  "_id": ObjectId,
  "order_number": "ORD-2025-001",
  "customer": {
    "name": "Іван Петренко",
    "email": "ivan@example.com",
    "phone": "+380501234567"
  },
  "items": [
    {
      "product_id": ObjectId,
      "product_name": "Ноутбук Lenovo",
      "quantity": 1,
      "price": 25000
    }
  ],
  "total_amount": 27500,
  "status": "completed",
  "order_date": ISODate
}
```

**Особливості:**
- Денормалізовані дані (вбудовані документи)
- Гнучка схема (schema-less)
- Легко додавати нові поля
- Eventual consistency за замовчуванням

---

## 🔄 2. CRUD Операції - Порівняння

### **CREATE (Створення)**

#### PostgreSQL:
```sql
-- Потрібна транзакція для зв'язаних даних
BEGIN;
  INSERT INTO customers (name, email) 
  VALUES ('Іван', 'ivan@example.com') 
  RETURNING customer_id;
  
  INSERT INTO orders (order_number, customer_id, total_amount) 
  VALUES ('ORD-001', 1, 27500);
COMMIT;
```
**Переваги:** Атомарність, цілісність даних  
**Недоліки:** Складніше для складних структур

#### MongoDB:
```javascript
// Одна операція з вкладеними даними
db.orders.insertOne({
  order_number: 'ORD-001',
  customer: {
    name: 'Іван',
    email: 'ivan@example.com'
  },
  items: [...],
  total_amount: 27500
});
```
**Переваги:** Простота, природне представлення об'єктів  
**Недоліки:** Дублювання даних

---

### **READ (Читання)**

#### PostgreSQL:
```sql
-- Потрібні JOIN для зв'язаних даних
SELECT o.order_number, c.name, o.total_amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_date >= CURRENT_DATE - INTERVAL '30 days';
```
**Переваги:** Потужні JOIN, відсутність дублювання  
**Недоліки:** Повільніше при багатьох JOIN

#### MongoDB:
```javascript
// Всі дані в одному документі
db.orders.find({
  order_date: { $gte: new Date(Date.now() - 30*24*60*60*1000) }
});
```
**Переваги:** Швидкість (немає JOIN), простота  
**Недоліки:** Потенційно застарілі вбудовані дані

---

### **UPDATE (Оновлення)**

#### PostgreSQL:
```sql
-- Оновлення впливає на всі зв'язки
UPDATE products 
SET stock = stock - 1 
WHERE product_id = 1;

-- Автоматично відображається у всіх зв'язках
```
**Переваги:** Одне оновлення → скрізь актуально  
**Недоліки:** Потрібні додаткові запити для перевірки

#### MongoDB:
```javascript
// Потрібно оновити в кількох місцях
db.products.updateOne(
  { _id: productId },
  { $inc: { stock: -1 } }
);

// Також треба оновити в orders, якщо збережено
db.orders.updateMany(
  { 'items.product_id': productId },
  { $set: { 'items.$.price': newPrice } }
);
```
**Переваги:** Швидкість окремих оновлень  
**Недоліки:** Ризик неконсистентності

---

### **DELETE (Видалення)**

#### PostgreSQL:
```sql
-- Каскадне видалення або захист
DELETE FROM products WHERE product_id = 1;
-- Помилка, якщо є зв'язки без CASCADE
```
**Переваги:** Контроль цілісності  
**Недоліки:** Складніше видалити зв'язані дані

#### MongoDB:
```javascript
// Просте видалення
db.products.deleteOne({ _id: productId });
// Але залишаються посилання в orders!
```
**Переваги:** Швидкість  
**Недоліки:** "Сирітські" посилання

---

## 📈 3. Агрегація - Порівняння

### **Складний аналітичний запит**

#### PostgreSQL:
```sql
SELECT 
  c.name,
  COUNT(o.order_id) as total_orders,
  SUM(o.total_amount) as total_spent,
  AVG(o.total_amount) as avg_order,
  STRING_AGG(o.order_number, ', ') as orders
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= '2025-01-01'
GROUP BY c.customer_id, c.name
HAVING SUM(o.total_amount) > 10000
ORDER BY total_spent DESC;
```

**Переваги:**
- ✅ Стандартний SQL (легко зрозуміти)
- ✅ Потужні можливості GROUP BY, HAVING
- ✅ Оптимізація запитів планувальником
- ✅ Підтримка віконних функцій

**Недоліки:**
- ❌ Може бути повільним на великих JOIN
- ❌ Складність зростає з кількістю таблиць

#### MongoDB:
```javascript
db.orders.aggregate([
  { $match: { order_date: { $gte: new Date('2025-01-01') } } },
  { $group: {
      _id: '$customer.email',
      customer_name: { $first: '$customer.name' },
      total_orders: { $sum: 1 },
      total_spent: { $sum: '$total_amount' },
      avg_order: { $avg: '$total_amount' },
      orders: { $push: '$order_number' }
  }},
  { $match: { total_spent: { $gt: 10000 } } },
  { $sort: { total_spent: -1 } }
]);
```

**Переваги:**
- ✅ Працює з вбудованими документами
- ✅ Пайплайн зрозумілий покроково
- ✅ Відсутність JOIN (дані вже разом)
- ✅ Горизонтальне масштабування

**Недоліки:**
- ❌ Незвичний синтаксис
- ❌ Обмежені можливості vs SQL
- ❌ Ускладнення при зв'язках між колекціями

---

## ⚡ 4. Продуктивність

### **Швидкість читання**

| Операція | PostgreSQL | MongoDB | Переможець |
|----------|-----------|---------|------------|
| Простий SELECT | ~1ms | ~0.5ms | MongoDB |
| З 1 JOIN | ~3ms | ~0.5ms | MongoDB |
| З 3+ JOIN | ~15ms | ~0.5ms | MongoDB |
| Складна агрегація | ~20ms | ~25ms | PostgreSQL |
| Повнотекстовий пошук | ~10ms | ~15ms | PostgreSQL |

### **Швидкість запису**

| Операція | PostgreSQL | MongoDB | Переможець |
|----------|-----------|---------|------------|
| Один INSERT | ~2ms | ~1ms | MongoDB |
| Batch INSERT (1000) | ~50ms | ~30ms | MongoDB |
| UPDATE з транзакцією | ~5ms | ~2ms | MongoDB |
| Складний UPDATE | ~10ms | ~15ms | PostgreSQL |

---

## 🎯 5. Коли використовувати?

### **PostgreSQL (SQL) - Краще для:**

#### ✅ **Фінансові системи**
```sql
-- Критична важливість ACID-транзакцій
BEGIN;
  UPDATE accounts SET balance = balance - 1000 WHERE user_id = 1;
  UPDATE accounts SET balance = balance + 1000 WHERE user_id = 2;
  INSERT INTO transactions (from_user, to_user, amount) VALUES (1, 2, 1000);
COMMIT;
```
**Чому:** Атомарність, відсутність втрат даних

#### ✅ **Складні зв'язки**
- CRM системи (клієнти → контакти → угоди)
- ERP системи (замовлення → постачальники → склад)
- Соціальні мережі (користувачі → друзі → пости → коментарі)

#### ✅ **Звітність та аналітика**
```sql
-- Складні бізнес-запити
WITH monthly_sales AS (
  SELECT DATE_TRUNC('month', order_date) as month,
         SUM(total_amount) as revenue
  FROM orders
  GROUP BY month
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) as prev_month,
       revenue - LAG(revenue) OVER (ORDER BY month) as growth
FROM monthly_sales;
```

#### ✅ **Консистентність критична**
- Медичні записи
- Юридичні документи
- Інвентаризація

---

### **MongoDB (NoSQL) - Краще для:**

#### ✅ **Контент-менеджмент**
```javascript
// Гнучка структура для різних типів контенту
{
  type: 'blog_post',
  title: 'Заголовок',
  content: '...',
  author: { name: '...', bio: '...' },
  tags: ['tech', 'ai'],
  meta: { views: 1000, likes: 50 },
  // Легко додати нові поля
  featured_image: 'url',
  related_posts: [...]
}
```

#### ✅ **Real-time додатки**
- Чати (швидкі записи повідомлень)
- IoT сенсори (величезні обсяги даних)
- Ігрові сервери (стан гри)

#### ✅ **Каталоги продуктів**
```javascript
// Різні атрибути для різних товарів
{
  name: 'Ноутбук',
  specs: {
    cpu: 'Intel i7',
    ram: 16,
    screen: 15.6
  }
}
// vs
{
  name: 'Футболка',
  specs: {
    size: 'L',
    color: 'blue',
    material: 'cotton'
  }
}
```

#### ✅ **Прототипування**
- Швидка зміна структури даних
- Немає міграцій схеми
- Гнучкість у розробці

---

## 📊 6. Детальне порівняння характеристик

### **Цілісність даних**

| Аспект | PostgreSQL | MongoDB |
|--------|-----------|---------|
| ACID | ✅ Повна підтримка | ⚠️ Часткова (з v4.0) |
| Транзакції | ✅ Multi-table | ⚠️ Multi-document (з обмеженнями) |
| Referential integrity | ✅ Foreign Keys | ❌ Вручну |
| Constraints | ✅ NOT NULL, UNIQUE, CHECK | ⚠️ Обмежені |

### **Масштабування**

| Аспект | PostgreSQL | MongoDB |
|--------|-----------|---------|
| Вертикальне | ✅ Відмінно | ✅ Відмінно |
| Горизонтальне | ⚠️ Складно (sharding) | ✅ Вбудоване (sharding) |
| Реплікація | ✅ Master-Slave | ✅ Replica Sets |
| Auto-sharding | ❌ Потрібні додаткові інструменти | ✅ Вбудоване |

### **Гнучкість схеми**

| Аспект | PostgreSQL | MongoDB |
|--------|-----------|---------|
| Зміна структури | ❌ Потрібна міграція | ✅ Без міграцій |
| Нові поля | ❌ ALTER TABLE | ✅ Просто додати |
| Різні структури | ❌ Потрібні NULL | ✅ Природно |
| Вкладені об'єкти | ⚠️ JSON/JSONB | ✅ Нативно |

---

## 💡 7. Практичні рекомендації

### **Вибирайте PostgreSQL якщо:**

1. **Ваші дані мають чітку структуру** з багатьма зв'язками
2. **Критична цілісність даних** (фінанси, медицина)
3. **Потрібні складні JOIN** та аналітика
4. **Команда знає SQL** краще ніж NoSQL
5. **Дані рідко змінюють структуру**

### **Вибирайте MongoDB якщо:**

1. **Гнучка/невизначена структура** даних
2. **Потрібна висока швидкість** читання/запису
3. **Великі обсяги даних** з потребою шардингу
4. **Документо-орієнтована** модель природна
5. **Швидкий розвиток** з частими змінами схеми

### **Використовуйте обидва (Polyglot Persistence):**

```
Приклад архітектури:
├─ PostgreSQL
│  ├─ Транзакційні дані (замовлення, платежі)
│  └─ Користувачі та аутентифікація
│
├─ MongoDB
│  ├─ Каталог продуктів
│  ├─ Логи та події
│  └─ Кешування
│
└─ Redis
   ├─ Сесії
   └─ Real-time лічильники
```

---

## 📈 8. Підсумкова таблиця

| Критерій | PostgreSQL | MongoDB | Коментар |
|----------|-----------|---------|----------|
| **Простота використання** | ⭐⭐⭐ | ⭐⭐⭐⭐ | MongoDB простіший для початку |
| **Продуктивність (читання)** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | MongoDB швидший без JOIN |
| **Продуктивність (запис)** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | MongoDB трохи швидший |
| **Цілісність даних** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | PostgreSQL гарантує консистентність |
| **Складні запити** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | SQL потужніший для аналітики |
| **Масштабування** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | MongoDB легше масштабувати |
| **Гнучкість схеми** | ⭐⭐ | ⭐⭐⭐⭐⭐ | MongoDB не вимагає схеми |
| **Зрілість екосистеми** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | PostgreSQL старший та стабільніший |
| **Навчання/Документація** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Обидва мають чудову документацію |
| **Підтримка спільноти** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | PostgreSQL має більшу спільноту |

---

## 🎓 Висновок

**Немає універсального рішення!** Вибір залежить від:
- Типу даних та їх структури
- Вимог до консистентності
- Очікуваного навантаження
- Досвіду команди
- Бюджету на інфраструктуру

**Найкращий підхід:** використовувати правильний інструмент для кожного завдання (Polyglot Persistence).