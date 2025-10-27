## 🔑 Що таке суперкористувач (superuser)?

**Суперкористувач** - це адміністратор з **повними правами**:
- ✅ Доступ до адмін-панелі `/admin/`
- ✅ Може додавати/редагувати/видаляти будь-які дані
- ✅ Може керувати іншими користувачами
- ✅ Має всі дозволи (permissions)

---

## 🎯 Варіанти створення суперкористувача

### ✅ Варіант 1: Команда `createsuperuser` (РЕКОМЕНДОВАНО)

```bash
python manage.py createsuperuser
```

**Інтерактивний процес:**
```
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

**Плюси:**
- ✅ Найбезпечніший спосіб
- ✅ Пароль автоматично хешується
- ✅ Перевірка на помилки

---

### ✅ Варіант 2: Через Python shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Створення суперкористувача
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123'
)

print(f"Суперкористувач {admin.username} створений!")
```

---

### ✅ Варіант 3: Через скрипт

Створіть файл `create_admin.py`:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')
django.setup()

from django.contrib.auth.models import User

# Перевірка чи існує
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("✅ Суперкористувач створений!")
else:
    print("⚠️ Суперкористувач вже існує")
```

Запуск:
```bash
python create_admin.py
```

---
## 👥 Різниця між типами користувачів

### 1. **Звичайний користувач**
```python
user = User.objects.create_user(
    username='ivan',
    password='pass123'
)
```
- ❌ Немає доступу до `/admin/`
- ✅ Може використовувати сайт
- `is_staff = False`
- `is_superuser = False`

### 2. **Staff користувач** (персонал)
```python
user = User.objects.create_user(
    username='manager',
    password='pass123'
)
user.is_staff = True
user.save()
```
- ✅ Доступ до `/admin/`
- ⚠️ Обмежені права (тільки те, що дозволено)
- `is_staff = True`
- `is_superuser = False`

### 3. **Суперкористувач**
```python
admin = User.objects.create_superuser(
    username='admin',
    password='admin123'
)
```
- ✅ Повний доступ до `/admin/`
- ✅ Всі права
- ✅ Може все
- `is_staff = True`
- `is_superuser = True`
- `is_active = True`

---

## 📊 Таблиця порівняння

| Характеристика          | User  | Staff | Superuser |
|-------------------------|-------|-------|-----------|
| Доступ до сайту         | ✅     | ✅     | ✅         |
| Доступ до /admin/       | ❌     | ✅     | ✅         |
| Може додавати дані      | ❌     | ⚠️    | ✅         |
| Може видаляти дані      | ❌     | ⚠️    | ✅         |
| Керування користувачами | ❌     | ❌     | ✅         |
| `is_staff`              | False | True  | True      |
| `is_superuser`          | False | False | True      |

---

## 🔐 Перевірка прав користувача

```python
from django.contrib.auth.models import User

user = User.objects.get(username='admin')

# Перевірки
print(f"Username: {user.username}")
print(f"Email: {user.email}")
print(f"Is staff: {user.is_staff}")          # True
print(f"Is superuser: {user.is_superuser}") # True
print(f"Is active: {user.is_active}")       # True

# Перевірка конкретного дозволу
if user.has_perm('board.add_ad'):
    print("Може додавати оголошення")

# Перевірка чи суперкористувач
if user.is_superuser:
    print("Це адміністратор з повними правами!")
```

---

## 🛠️ Практичні команди

### Створити нового суперкористувача
```bash
python manage.py createsuperuser
```

### Зробити існуючого користувача суперкористувачем
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User

user = User.objects.get(username='ivan')
user.is_superuser = True
user.is_staff = True
user.save()

print(f"{user.username} тепер суперкористувач!")
```

### Змінити пароль суперкористувача
```bash
python manage.py changepassword admin
```

### Скинути пароль через shell
```python
from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('new_password123')
user.save()
```

---
## 🚨 Важливі моменти

### ⚠️ Безпека в продакшені

```python
# ❌ НЕ РОБІТЬ ТАК на реальному сайті:
password='admin123'  # Занадто простий!

# ✅ РОБІТЬ ТАК:
password='Kj9$mN2p!Qw8@Lx5'  # Складний пароль
```

### ⚠️ Змінні оточення
```python
# settings.py (для продакшену)
import os

ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
```

### ⚠️ Не комітьте паролі в Git
```python
# .gitignore
.env
secrets.py
```

---
## ✅ Підсумок

**Відповіді на ваші питання:**

2. **Які є варіанти?**
   - ✅ `python manage.py createsuperuser` (найкращий)
   - ✅ Через Python shell
   - ✅ Через скрипт
   - ✅ Програмно в коді

**Запускайте сервер і заходьте в адмінку!** 🚀  
http://127.0.0.1:8000/admin/