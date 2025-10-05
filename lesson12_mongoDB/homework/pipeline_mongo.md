
Этот **агрегационный конвейер (pipeline)** — очень мощный инструмент MongoDB, который позволяет обрабатывать и анализировать данные прямо в базе, без Python-цикла.
Давай разберём пример **пошагово**, чтобы стало ясно, *как именно всё работает* 👇

---

## 🔹 Контекст

Коллекция `orders` содержит документы вроде этого:

```json
{
  "_id": 1,
  "orderDate": ISODate("2024-09-15"),
  "client": "Ольга Головаш",
  "products": [
    {"name": "Ноутбук", "quantity": 2, "price": 1500},
    {"name": "Мишка", "quantity": 1, "price": 25}
  ],
  "total": 3025
}
```

---

## 🔹 Конвейер (pipeline)

Ты передаёшь список шагов (`pipeline1`) в метод:

```python
db.orders.aggregate(pipeline1)
```

Каждый элемент списка — это **этап (stage)** обработки данных.

---

### 🔸 1. `$match`

```python
{
  "$match": {
    "orderDate": {
      "$gte": datetime(2024, 9, 1),
      "$lte": datetime(2024, 9, 30)
    }
  }
}
```

**Что делает:** фильтрует только заказы, сделанные **в сентябре 2024**.
➡️ В конвейер пойдут только такие документы.

**Аналогия:** это как `WHERE orderDate BETWEEN '2024-09-01' AND '2024-09-30'` в SQL.

---

### 🔸 2. `$unwind`

```python
{"$unwind": "$products"}
```

**Что делает:** разворачивает массив `products` — каждая позиция становится отдельным документом.

Пример:

```json
{
  "orderDate": "2024-09-15",
  "products": [
    {"name": "Ноутбук", "quantity": 2, "price": 1500},
    {"name": "Мишка", "quantity": 1, "price": 25}
  ]
}
```

⬇ после `$unwind` ⬇

```json
{ "orderDate": "2024-09-15", "products": {"name": "Ноутбук", "quantity": 2, "price": 1500} }
{ "orderDate": "2024-09-15", "products": {"name": "Мишка", "quantity": 1, "price": 25} }
```

**Зачем:** теперь можно считать статистику по каждому товару отдельно.

---

### 🔸 3. `$group`

```python
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
}
```

**Что делает:** группирует все товары по имени (`_id = "$products.name"`)
и считает:

* 🧮 `totalQuantity` — общее количество проданных единиц (`$sum`)
* 💰 `totalRevenue` — общую выручку, умножая количество × цену и суммируя все

---

### 🔸 4. `$sort`

```python
{"$sort": {"totalQuantity": -1}}
```

**Что делает:** сортирует результат по убыванию количества проданных товаров.

---

## 🔹 🔍 Пример результата:

После выполнения pipeline ты получишь примерно такое:

```json
[
  {"_id": "Ноутбук", "totalQuantity": 20, "totalRevenue": 30000},
  {"_id": "Мишка", "totalQuantity": 15, "totalRevenue": 375},
  {"_id": "Клавіатура", "totalQuantity": 8, "totalRevenue": 480}
]
```

---

## 🔹 Как выполнить в Python (`pymongo`)

```python
from datetime import datetime
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["shop"]

pipeline1 = [
    {"$match": {"orderDate": {"$gte": datetime(2024, 9, 1), "$lte": datetime(2024, 9, 30)}}},
    {"$unwind": "$products"},
    {"$group": {
        "_id": "$products.name",
        "totalQuantity": {"$sum": "$products.quantity"},
        "totalRevenue": {"$sum": {"$multiply": ["$products.quantity", "$products.price"]}}
    }},
    {"$sort": {"totalQuantity": -1}}
]

result = list(db.orders.aggregate(pipeline1))
for r in result:
    print(r)
```

---
