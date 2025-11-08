`test_nested_serializers.py` тестує 
**вкладені серіалізатори** (Завдання 3) - коли один серіалізатор містить інший серіалізатор всередині.## 🎯 Коротко: `test_nested_serializers.py` тестує **Завдання 3**

### Що таке вкладений серіалізатор?

**Звичайний серіалізатор:**
```json
{
  "title": "Завдання",
  "user": 1  ← Тільки ID існуючого користувача
}
```

**Вкладений серіалізатор:**
```json
{
  "title": "Завдання",
  "user": {  ← Повні дані користувача
    "username": "john",
    "email": "john@example.com"
  }
}
```

### Що тестується:

1. ✅ **Створення** завдання з новим користувачем одночасно
2. ❌ **Валідація** даних користувача (пустий username, невалідний email)
3. ❌ **Помилки** при відсутності даних користувача
4. ✅ **Читання** завдання з повними даними користувача
5. ❌ **Валідація дат** у вкладеному серіалізаторі

### Переваги вкладених серіалізаторів:

- 🚀 Створити кілька об'єктів одним запитом
- 📦 Отримати всі дані без додаткових запитів
- 🎯 Зручніше для клієнта API

---

## 🔍 Що тестує файл

`test_nested_serializers.py` тестує **вкладені серіалізатори**.

> **Вкладений серіалізатор** — це коли один серіалізатор містить інший як поле.

📘 **Приклад:**

* Кожне завдання (`Task`) належить користувачеві (`User`)
* Ми хочемо створити **завдання разом із користувачем**
* Дані користувача передаються всередині даних завдання

---

## 🆚 Звичайний vs Вкладений серіалізатор

```python
from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import Task
```

### 🧱 Звичайний серіалізатор

```python
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'user']
```

**Приклад використання:**

```python
data = {
    'title': 'Завдання',
    'description': 'Опис',
    'due_date': '2025-12-31',
    'user': 1  # ← Тільки ID користувача
}

serializer = TaskSerializer(data=data)
serializer.save()
```

---

### 🧩 Вкладений серіалізатор

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TaskWithUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # ← Вкладений серіалізатор!

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        task = Task.objects.create(user=user, **validated_data)
        return task
```

**Приклад використання:**

```python
data = {
    'title': 'Завдання',
    'description': 'Опис',
    'due_date': '2025-12-31',
    'user': {
        'username': 'john_doe',
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    }
}

serializer = TaskWithUserSerializer(data=data)
serializer.save()
# Створить і користувача, і завдання одночасно!
```

---

## ⚖️ Різниця між звичайним і вкладеним

| Серіалізатор               | Вхідні дані       | Вихідні дані      | Особливості                       |
| -------------------------- | ----------------- | ----------------- | --------------------------------- |
| **TaskSerializer**         | `"user": 1`       | `"user": 1`       | ❌ Користувач має існувати         |
| **TaskWithUserSerializer** | `"user": { ... }` | `"user": { ... }` | ✅ Створює користувача автоматично |

---

## 🧠 Що тестує `test_nested_serializers.py`

### 🏗️ OOP підхід (`TestTaskWithUserSerializerOOP`)

| № | Тест                                               | Результат               |
| - | -------------------------------------------------- | ----------------------- |
| 1 | `test_nested_serializer_valid_with_correct_data()` | ✅ Валідні вкладені дані |
| 2 | `test_nested_serializer_invalid_empty_username()`  | ❌ Пустий username       |
| 3 | `test_nested_serializer_missing_user_username()`   | ❌ Відсутній username    |
| 4 | `test_nested_serializer_invalid_email()`           | ❌ Невалідний email      |
| 5 | `test_nested_serializer_missing_user_data()`       | ❌ Відсутній об’єкт user |
| 6 | `test_nested_serializer_create_with_user()`        | ✅ Створення user+task   |
| 7 | `test_nested_serializer_read_existing_task()`      | ✅ Читання даних         |
| 8 | `test_nested_serializer_past_date_validation()`    | ❌ Минуле значення дати  |

---

### ⚙️ Функціональний підхід

| № | Тест                                                      | Результат                    |
| - | --------------------------------------------------------- | ---------------------------- |
| 1 | `test_nested_serializer_valid_functional()`               | ✅ Створення user+task        |
| 2 | `test_nested_serializer_invalid_user_fields_functional()` | ❌ Невалідні поля користувача |
| 3 | `test_nested_serializer_missing_user_data_functional()`   | ❌ Відсутні дані user         |
| 4 | `test_nested_serializer_missing_user_fields_functional()` | ❌ Пропущені поля             |
| 5 | `test_nested_serializer_full_workflow_functional()`       | ✅ Повний робочий цикл        |

---

## 🧪 Приклад тестів

```python
import pytest
from datetime import date, timedelta
from django.contrib.auth.models import User
from main.serializers import TaskWithUserSerializer
```

### ✅ Валідний приклад

```python
@pytest.mark.django_db
def test_nested_example():
    data = {
        'title': 'Завдання з користувачем',
        'description': 'Опис завдання',
        'due_date': str(date.today() + timedelta(days=7)),
        'user': {
            'username': 'nesteduser',
            'email': 'nested@example.com',
            'first_name': 'Тест',
            'last_name': 'Користувач'
        }
    }

    serializer = TaskWithUserSerializer(data=data)
    assert serializer.is_valid(), f"Помилки: {serializer.errors}"

    task = serializer.save()

    assert task.title == 'Завдання з користувачем'
    assert task.user.username == 'nesteduser'
    assert User.objects.filter(username='nesteduser').exists()
```

---

### ❌ Невалідний користувач

```python
@pytest.mark.django_db
def test_nested_invalid_user():
    data = {
        'title': 'Завдання',
        'description': 'Опис',
        'due_date': str(date.today() + timedelta(days=7)),
        'user': {
            'username': 'testuser',
            'email': 'not-an-email',
            'first_name': 'Тест'
        }
    }

    serializer = TaskWithUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'user' in serializer.errors
```

---

## 🌐 Приклад API-запиту

### `POST /api/tasks/`

**Request:**

```json
{
  "title": "Розробити новий функціонал",
  "description": "Додати можливість експорту звітів",
  "due_date": "2025-12-31",
  "user": {
    "username": "developer",
    "email": "dev@company.com",
    "first_name": "Іван",
    "last_name": "Петренко"
  }
}
```

**Response (201 Created):**

```json
{
  "id": 42,
  "title": "Розробити новий функціонал",
  "description": "Додати можливість експорту звітів",
  "due_date": "2025-12-31",
  "user": {
    "id": 15,
    "username": "developer",
    "email": "dev@company.com",
    "first_name": "Іван",
    "last_name": "Петренко"
  }
}
```

✅ Одним запитом створено і користувача, і завдання!

---

## 💡 Коли використовувати вкладені серіалізатори

✅ Використовуйте, якщо:

* Потрібно створювати кілька пов’язаних об’єктів одночасно
* При читанні потрібні повні дані об’єктів
* Хочете спростити API для клієнтів

❌ Не використовуйте, якщо:

* Об’єкти вже існують (достатньо ID)
* Дані часто повторюються
* Є складна бізнес-логіка (краще окремі ендпоїнти)

---

## 📚 Інші приклади

### 📝 Блог з коментарями

```python
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'comments']
```

---

### 🛒 Замовлення з товарами

```python
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'items', 'total']
```

---

### 👤 Профіль користувача з адресою

```python
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'country', 'zip_code']


class UserProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'avatar', 'address']
```

---

## ✅ Підсумок

`test_nested_serializers.py` перевіряє:

* ✅ Створення завдання разом із новим користувачем
* ✅ Валідацію вкладених полів користувача
* ❌ Обробку невалідних даних
* ✅ Коректне читання повних даних користувача
* ✅ Валідацію дат

**Навіщо це потрібно:**

* 🔍 Вкладені серіалізатори складніші у валідації
* ⚙️ Помилки можуть бути як у Task, так і у User
* 🧠 Важливо перевірити, що створюються обидва об’єкти
* 🌐 Для зручності API-клієнтів

---
