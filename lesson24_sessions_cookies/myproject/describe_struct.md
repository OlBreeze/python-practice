# Структура Django проекту

```
myproject/                          # Коренева директорія проекту
│
├── myproject/                      # Головна директорія налаштувань
│   ├── __init__.py                # Ініціалізація Celery
│   ├── settings.py                # Налаштування Django
│   ├── urls.py                    # Головні URL маршрути
│   ├── wsgi.py                    # WSGI конфігурація
│   ├── asgi.py                    # ASGI конфігурація
│   └── celery.py                  # Конфігурація Celery
│
├── myapp/                          # Основний додаток
│   ├── __init__.py
│   ├── admin.py                   # Налаштування адмін-панелі
│   ├── apps.py                    # Конфігурація додатку
│   ├── models.py                  # Моделі (Author, Book, Review)
│   ├── views.py                   # Представлення (views)
│   ├── urls.py                    # URL маршрути додатку
│   ├── tasks.py                   # Celery завдання
│   ├── middleware.py              # Власні middleware
│   ├── tests.py                   # Тести
│   │
│   ├── migrations/                # Міграції бази даних
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   ├── management/                # Власні команди manage.py
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_db.py    # Команда заповнення БД
│   │
│   ├── templates/                 # HTML шаблони
│   │   ├── base.html             # Базовий шаблон
│   │   ├── login.html            # Форма входу
│   │   ├── welcome.html          # Сторінка привітання
│   │   ├── books_list.html       # Список книг
│   │   ├── books_cached.html     # Кешований список
│   │   ├── statistics.html       # Статистика
│   │   └── popular_authors.html  # Популярні автори
│   │
│   └── static/                    # Статичні файли (CSS, JS, зображення)
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── main.js
│       └── images/
│
├── data/                          # Директорія для даних
│   └── books.csv                 # CSV файл для імпорту
│
├── media/                         # Завантажені файли користувачів
│
├── static/                        # Зібрані статичні файли (collectstatic)
│
├── logs/                          # Логи
│   ├── django.log
│   └── celery.log
│
├── venv/                          # Віртуальне середовище (не додавати в git)
│
├── manage.py                      # Django CLI
├── requirements.txt               # Python залежності
├── .env                          # Змінні оточення (не додавати в git)
├── .gitignore                    # Git ignore файл
├── README.md                     # Документація проекту
└── db.sqlite3                    # База даних SQLite (не додавати в git)
```

## Детальний опис файлів:

### 📁 myproject/ (налаштування)

**`__init__.py`**
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```

**`celery.py`**
```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

**`urls.py`**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

### 📁 myapp/ (основний додаток)

**`admin.py`**
```python
from django.contrib import admin
from .models import Author, Book, Review

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_year', 'created_at']
    list_filter = ['published_year', 'author']
    search_fields = ['title']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
```

### 📁 data/

**`books.csv`**
```csv
title,author,year
Кобзар,Тарас Шевченко,1840
Лісова пісня,Леся Українка,1911
Захар Беркут,Іван Франко,1883
Тіні забутих предків,Михайло Коцюбинський,1911
Повія,Панас Мирний,1883
```

### 📄 Конфігураційні файли

**`.gitignore`**
```
# Python
*.py[cod]
*$py.class
__pycache__/
*.so
.Python
venv/
env/

# Django
*.log
db.sqlite3
/media
/static
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

**`.env`**
```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## Команди для створення структури:

```bash
# Створити проект
django-admin startproject myproject
cd myproject

# Створити додаток
python manage.py startapp myapp

# Створити директорії
mkdir -p myapp/templates
mkdir -p myapp/static/{css,js,images}
mkdir -p myapp/management/commands
mkdir -p data
mkdir -p media
mkdir -p logs

# Створити порожні файли
touch myapp/middleware.py
touch myapp/tasks.py
touch myapp/management/__init__.py
touch myapp/management/commands/__init__.py
touch myapp/management/commands/populate_db.py
touch myproject/celery.py
touch .env
touch .gitignore
touch data/books.csv

# Застосувати міграції
python manage.py makemigrations
python manage.py migrate

# Створити суперюзера
python manage.py createsuperuser

# Заповнити БД
python manage.py populate_db

# Запустити сервер
python manage.py runserver
```

## Запуск всіх компонентів:

**Термінал 1 - Django:**
```bash
python manage.py runserver
```

**Термінал 2 - Redis:**
```bash
redis-server
```

**Термінал 3 - Celery Worker:**
```bash
celery -A myproject worker -l info
```

**Термінал 4 - Celery Beat (опціонально, для періодичних завдань):**
```bash
celery -A myproject beat -l info
```

## Корисні команди:

```bash
# Створити нові міграції
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Відкрити Django shell
python manage.py shell

# Зібрати статичні файли
python manage.py collectstatic

# Створити дамп бази даних
python manage.py dumpdata > backup.json

# Завантажити дамп
python manage.py loaddata backup.json

# Очистити кеш
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```