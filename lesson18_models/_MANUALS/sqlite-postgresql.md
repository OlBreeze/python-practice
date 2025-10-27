## 🐘 Підключення PostgreSQL до Django проєкту

---

## 📋 Покрокова інструкція

### Крок 1️⃣: Встановити PostgreSQL

**Windows:**
1. Завантажити: https://www.postgresql.org/download/windows/
2. Запустити інсталятор
3. Запам'ятати **пароль для postgres**
4. Порт за замовчуванням: **5432**

**Або через chocolatey:**
```bash
choco install postgresql
```

---

### Крок 2️⃣: Встановити драйвер psycopg2

```bash
# У віртуальному середовищі проєкту
pip install psycopg2-binary

# АБО (якщо перший не працює)
pip install psycopg2
```

Додати до `requirements.txt`:
```txt
Django==5.1.3
psycopg2-binary==2.9.9
```

---

### Крок 3️⃣: Створити базу даних PostgreSQL

**Через pgAdmin** (графічний інтерфейс):
1. Відкрити pgAdmin
2. Правою кнопкою на **Databases** → **Create** → **Database**
3. Назва: `bulletin_board_db`
4. Owner: `postgres`
5. Save

**Або через командний рядок:**
```bash
# Увійти в PostgreSQL
psql -U postgres

# Створити БД
CREATE DATABASE bulletin_board_db;

# Створити користувача (опціонально)
CREATE USER board_user WITH PASSWORD 'your_password';

# Надати права
GRANT ALL PRIVILEGES ON DATABASE bulletin_board_db TO board_user;

# Вийти
\q
```

---

### Крок 4️⃣: Оновити `settings.py`

#### ❌ Було (SQLite):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### ✅ Стало (PostgreSQL):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bulletin_board_db',           # Назва БД
        'USER': 'postgres',                    # Користувач
        'PASSWORD': 'your_password',           # Пароль
        'HOST': 'localhost',                   # Або '127.0.0.1'
        'PORT': '5432',                        # Порт PostgreSQL
    }
}
```

---

### Крок 5️⃣: Застосувати міграції

```bash
# Перевірити підключення
python manage.py check

# Застосувати міграції
python manage.py migrate

# Створити суперкористувача
python manage.py createsuperuser
```

---

### Крок 6️⃣: Заповнити тестовими даними

```bash
# Запустити populate скрипт
python populate_db.py

# АБО
python manage.py shell
>>> from board.models import *
>>> # Створити тестові дані вручну
```

---

## 🔒 Крок 7️⃣: Винести секрети в .env (ВАЖЛИВО!)

### Встановити python-dotenv:
```bash
pip install python-dotenv
```

### Створити файл `.env`:
```env
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=bulletin_board_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### Оновити `settings.py`:
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Завантажити .env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретний ключ з .env
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-key')

# Debug режим
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# База даних
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'bulletin_board_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Додати `.env` до `.gitignore`:
```gitignore
# .gitignore
.env
db.sqlite3
__pycache__/
*.pyc
*.pyo
```

---

## 📊 Порівняння SQLite vs PostgreSQL

| Характеристика | SQLite | PostgreSQL |
|----------------|--------|------------|
| Тип | Файл | Сервер |
| Продуктивність | Добре для розробки | Краще для продакшену |
| Concurrent writes | Обмежено | Відмінно |
| Дані | 1 файл | Окремий сервер |
| Backup | Скопіювати файл | pg_dump |
| Складність | Просто | Складніше |

---

## 🔄 Міграція даних з SQLite → PostgreSQL

### Спосіб 1: Через dumpdata/loaddata

```bash
# 1. Експорт даних зі SQLite
python manage.py dumpdata > data_backup.json

# 2. Змінити settings.py на PostgreSQL

# 3. Застосувати міграції
python manage.py migrate

# 4. Імпортувати дані
python manage.py loaddata data_backup.json
```

### Спосіб 2: Написати скрипт міграції

```python
# migrate_to_postgres.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')
django.setup()

from board.models import *
from django.contrib.auth.models import User

# Експортувати дані зі старої БД
# Імпортувати в нову БД
```

---

## 🧪 Перевірка підключення

```bash
python manage.py shell
```

```python
from django.db import connection

# Перевірити підключення
with connection.cursor() as cursor:
    cursor.execute("SELECT version();")
    row = cursor.fetchone()
    print(row)

# Має показати версію PostgreSQL
# Наприклад: ('PostgreSQL 15.3 ...',)
```

---

## 📝 Чек-лист міграції на PostgreSQL

- [ ] 1. Встановити PostgreSQL
- [ ] 2. `pip install psycopg2-binary python-dotenv`
- [ ] 3. Створити БД: `CREATE DATABASE bulletin_board_db;`
- [ ] 4. Створити `.env` файл
- [ ] 5. Оновити `settings.py`
- [ ] 6. Експорт даних: `python manage.py dumpdata > backup.json`
- [ ] 7. Застосувати міграції: `python manage.py migrate`
- [ ] 8. Імпорт даних: `python manage.py loaddata backup.json`
- [ ] 9. Створити суперюзера: `python manage.py createsuperuser`
- [ ] 10. Тестувати: `python manage.py runserver`

---

## ⚠️ Можливі проблеми та рішення

### Проблема 1: `psycopg2` не встановлюється

```bash
# Спробувати binary версію
pip install psycopg2-binary

# Або встановити Visual C++ Build Tools (Windows)
```

### Проблема 2: Не може підключитися до PostgreSQL

```python
# Перевірити чи запущений PostgreSQL
# Windows: Відкрити Services → PostgreSQL

# Перевірити порт
netstat -an | findstr 5432
```

### Проблема 3: Помилка автентифікації

```bash
# Перевірити пароль
psql -U postgres -d bulletin_board_db

# Змінити пароль
ALTER USER postgres PASSWORD 'new_password';
```

---
