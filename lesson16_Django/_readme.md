# Конспект лекції: Введення в Django

## 1. Повторення: Веб-скрейпінг

### Beautiful Soup
**Beautiful Soup** - бібліотека для парсингу та аналізу HTML та XML файлів.

**Можливості:**
- Витягування тексту з веб-сторінок
- Пошук за тегами, атрибутами, текстом
- Збір даних для аналізу
- Наповнення баз даних

### Регулярні вирази (Regex)
Допомагають шукати інформацію за шаблоном (паттерном). Дуже гнучкий інструмент для пошуку та фільтрування тексту.

## 2. Основи веб-розробки

### Компоненти веб-застосунку

**Складові:**
1. **Серверна частина (Backend)**
   - Бізнес-логіка
   - База даних
   - API

2. **Клієнтська частина (Frontend)**
   - Інтерфейс користувача
   - Відображення даних

### Архітектурний патерн MVC

**MVC (Model-View-Controller)**

```
┌─────────┐
│  Model  │ ← База даних, бізнес-логіка
└────┬────┘
     │
┌────┴────────┐
│ Controller  │ ← Обробка запитів
└────┬────────┘
     │
┌────┴────┐
│  View   │ ← Відображення для користувача
└─────────┘
```

**Компоненти:**
- **Model** - робота з базами даних
- **View** - те, що бачить користувач
- **Controller** - зв'язує Model і View, обробляє запити

## 3. Django Framework

### Що таке Django?

> **Django** - високорівневий веб-фреймворк на Python, який сприяє швидкій розробці та підтримує чисту архітектуру коду.

### Історія
- **Перший реліз:** 2005 рік
- **Розробка почалась:** ~2003 рік
- **Поточна версія:** Django 5.2 (бета 6-ї версії)
- **Вік фреймворку:** 20+ років

### Чому Django?

#### ✅ Переваги

**1. All-inclusive (все з коробки)**
- Вбудована адмін-панель
- ORM для роботи з БД
- Система форм
- Система шаблонів
- Аутентифікація користувачів

**2. Швидка розробка**
- Готові компоненти
- Не потрібно писати з нуля
- Швидке прототипування (MVP)

**3. Безпека**
- Захист від SQL-ін'єкцій
- Захист від XSS-атак
- CSRF-токени
- Вбудовані механізми безпеки

**4. Масштабованість**
- Підходить для малих проектів
- Підходить для великих Enterprise-проектів
- Модульна архітектура

**5. Велика спільнота**
- Багато документації
- Велика кількість пакетів
- Багато вакансій

#### ⚠️ Особливості (недоліки)

**1. Жорстка структура**
- ➕ Добре для великих проектів
- ➖ Надмірно для простих застосунків

**2. Прив'язка до HTTP**
- Працює з методами HTTP (навіть при використанні HTTPS)
- Історичні причини (розробка почалась у 2003)

**3. Важкий для простих проектів**
- Багато вбудованих компонентів
- Альтернатива: Flask (легший фреймворк)

### Порівняння фреймворків Python

| Фреймворк | Тип | Особливості |
|-----------|-----|-------------|
| **Django** | Синхронний | Жорстка структура, все з коробки |
| **Flask** | Синхронний | Легкий, гнучкий, мінімалістичний |
| **FastAPI** | Асинхронний | Швидкий, сучасний, REST API |

### Django REST Framework (DRF)

Розширення для Django для побудови REST API:
- Серіалізація даних
- Автентифікація/авторизація
- Документація API
- Throttling (обмеження запитів)

### Django Ninja

Асинхронне розширення для Django:
- Швидша робота
- Асинхронні запити
- Альтернатива Fast API всередині Django

## 4. Патерн MTV у Django

### Від MVC до MTV

Django використовує модифікацію MVC:

| MVC | Django (MTV) |
|-----|--------------|
| Model | Model (моделі) |
| View | Template (шаблони) |
| Controller | View (представлення) |

**MTV (Model-Template-View)**

```
Model ─────┐
           ├──> View ──> Template
URLs ──────┘
```

## 5. Встановлення та налаштування

### Вимоги

- **Python:** версія 3.8 або вище
- **Віртуальне середовище:** рекомендовано
- **IDE:** PyCharm Pro, VS Code

### Встановлення Django

```bash
# Створення віртуального середовища
python -m venv venv

# Активація (Windows)
venv\Scripts\activate

# Активація (Linux/Mac)
source venv/bin/activate

# Встановлення Django
pip install django

# Перевірка версії
django-admin --version
```

### Створення проекту

```bash
# Створення проекту
django-admin startproject myproject

# Перехід у директорію
cd myproject

# Запуск сервера
python manage.py runserver
```

**Результат:** Сервер запуститься на `http://127.0.0.1:8000/`

## 6. Структура Django-проекту

### Файлова структура

```
myproject/
├── manage.py              # Головний файл керування
├── myproject/             # Пакет проекту
│   ├── __init__.py       # Ініціалізація пакету
│   ├── settings.py       # Налаштування проекту
│   ├── urls.py           # Маршрутизація проекту
│   ├── asgi.py           # ASGI-конфігурація
│   └── wsgi.py           # WSGI-конфігурація
```

### Основні файли

#### `manage.py`
Головний файл для керування проектом (запуск сервера, міграції, тощо)

#### `settings.py` - Налаштування проекту

**Основні параметри:**

```python
# Базова директорія проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретний ключ (ВАЖЛИВО: не публікуйте!)
SECRET_KEY = 'django-insecure-...'

# Режим налагодження
DEBUG = True  # False на продакшні!

# Дозволені хости
ALLOWED_HOSTS = []  # ['example.com'] на продакшні

# Встановлені застосунки
INSTALLED_APPS = [
    'django.contrib.admin',      # Адмін-панель
    'django.contrib.auth',       # Аутентифікація
    'django.contrib.contenttypes',
    'django.contrib.sessions',   # Сесії
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Тут додаються власні застосунки
]

# Middleware (проміжне ПЗ)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF-захист
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основний файл маршрутизації
ROOT_URLCONF = 'myproject.urls'

# База даних (за замовчуванням SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Мова та часова зона
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
```

**Важливі налаштування:**

| Параметр | Розробка | Продакшн |
|----------|----------|----------|
| `DEBUG` | `True` | `False` |
| `SECRET_KEY` | У коді | Змінна оточення |
| `ALLOWED_HOSTS` | `[]` | `['domain.com']` |

#### `urls.py` - Маршрутизація

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),  # Адмін-панель
]
```

## 7. Створення застосунків (Apps)

### Різниця між проектом та застосунком

**Проект** - вся веб-платформа
**Застосунок** - модуль з конкретною функціональністю

```
Проект (1)
    ├── Застосунок 1 (blog)
    ├── Застосунок 2 (shop)
    └── Застосунок 3 (users)
```

**Модульність:**
- Один застосунок може входити в різні проекти
- Один проект може містити багато застосунків
- Можливість повторного використання коду

### Створення застосунку

```bash
# Створення застосунку
python manage.py startapp lesson1

# Структура застосунку
lesson1/
├── __init__.py
├── admin.py        # Налаштування адмін-панелі
├── apps.py         # Конфігурація застосунку
├── models.py       # Моделі (БД)
├── tests.py        # Автотести
├── views.py        # Представлення (логіка)
└── migrations/     # Міграції БД
```

### Реєстрація застосунку

**ОБОВ'ЯЗКОВО** додати в `settings.py`:

```python
INSTALLED_APPS = [
    # ... Django apps
    'lesson1',  # Ваш застосунок
]
```

## 8. Маршрутизація (Routing)

### Як працює запит-відповідь

```
1. Client ──(Request)──> 2. URLs ──> 3. View ──> 4. Response
                              │
                              └──> Models (БД)
                              └──> Templates (HTML)
```

**Етапи:**
1. Клієнт формує **Request**
2. Django шукає відповідний маршрут в **URLs**
3. Викликається **View** (функція/клас)
4. View може звертатися до **Models** (БД)
5. View може використовувати **Templates** (HTML)
6. Повертається **Response** клієнту

### Базова маршрутизація

#### URLs проекту (`myproject/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lesson1/', include('lesson1.urls')),  # Підключення URLs застосунку
]
```

#### URLs застосунку (`lesson1/urls.py`)

**ВАЖЛИВО:** Цей файл потрібно створити вручну!

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # lesson1/
    path('about/', views.about, name='about'),  # lesson1/about/
]
```

### Views (Представлення)

#### Функціональні представлення (Function-Based Views)

```python
# lesson1/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello from Lesson 1!")

def about(request):
    return HttpResponse("About page")
```

**Структура:**
```python
def view_name(request):
    # Логіка обробки
    return HttpResponse("Response")
```

#### Класові представлення (Class-Based Views)

```python
from django.views import View
from django.http import HttpResponse

class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from Class View!")
```

## 9. Динамічна маршрутизація

### Статичні vs Динамічні маршрути

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    # Статичний маршрут
    path('about/', views.about),
    
    # Динамічний маршрут (path)
    path('users/<int:user_id>/', views.user_detail),
    path('articles/<slug:slug>/', views.article_detail),
    
    # Динамічний маршрут (regex)
    re_path(r'^users/(?P<user_id>\d+)/$', views.user_detail),
]
```

### Path-конвертери

| Конвертер | Опис | Приклад |
|-----------|------|---------|
| `<int:id>` | Ціле число | `/users/123/` |
| `<str:name>` | Рядок (без слешів) | `/profile/john/` |
| `<slug:slug>` | Slug (a-z, 0-9, -, _) | `/posts/my-first-post/` |
| `<uuid:id>` | UUID | `/item/550e8400-e29b.../` |
| `<path:path>` | Будь-який шлях | `/files/docs/readme.txt` |

### Приклади динамічних Views

```python
# views.py
from django.http import HttpResponse

# З параметром user_id
def user_detail(request, user_id):
    return HttpResponse(f"User ID: {user_id}")

# З параметром slug
def article_detail(request, slug):
    return HttpResponse(f"Article slug: {slug}")
```

### Регулярні вирази в маршрутах

```python
from django.urls import re_path

urlpatterns = [
    # Початок та кінець шаблону
    re_path(r'^about/$', views.about),
    #       ^       $
    #    початок  кінець
    
    # Slug: літери, цифри, дефіс (1+ раз)
    re_path(r'^articles/(?P<slug>[\w-]+)/$', views.article_detail),
    
    # ID: тільки цифри (1+ раз)
    re_path(r'^users/(?P<user_id>\d+)/$', views.user_detail),
]
```

**Символи regex:**
- `^` - початок рядка
- `$` - кінець рядка (обов'язково!)
- `\d` - цифра
- `\w` - літера або цифра
- `+` - один або більше
- `*` - нуль або більше
- `?P<name>` - іменована група

**Приклад:**
```
# Маршрут
r'^articles/(?P<slug>[\w-]+)/$'

# Відповідає:
/articles/my-first-post/
/articles/python-tutorial/

# Не відповідає:
/articles/my-first-post/edit/  # Є щось після слешу
/articles/  # Немає slug
```

## 10. Практичний приклад

### Повний приклад простого блогу

#### 1. Створення проекту та застосунку

```bash
django-admin startproject myblog
cd myblog
python manage.py startapp blog
```

#### 2. Реєстрація (`settings.py`)

```python
INSTALLED_APPS = [
    # ...
    'blog',
]
```

#### 3. URLs проекту (`myblog/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Корінь сайту
]
```

#### 4. URLs застосунку (`blog/urls.py`)

```python
from django.urls import path, re_path
from . import views

urlpatterns = [
    # Головна сторінка
    path('', views.index, name='home'),
    
    # Про нас
    path('about/', views.about, name='about'),
    
    # Користувачі (динамічно)
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    
    # Статті (regex)
    re_path(r'^articles/(?P<slug>[\w-]+)/$', views.article_detail, name='article'),
]
```

#### 5. Views (`blog/views.py`)

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Головна сторінка блогу")

def about(request):
    return HttpResponse("Про наш блог")

def user_detail(request, user_id):
    return HttpResponse(f"Профіль користувача #{user_id}")

def article_detail(request, slug):
    return HttpResponse(f"Стаття: {slug}")
```

#### 6. Запуск

```bash
python manage.py runserver
```

**Тестування:**
- `http://127.0.0.1:8000/` → "Головна сторінка блогу"
- `http://127.0.0.1:8000/about/` → "Про наш блог"
- `http://127.0.0.1:8000/users/123/` → "Профіль користувача #123"
- `http://127.0.0.1:8000/articles/my-post/` → "Стаття: my-post"

## 11. Налагодження (Debug)

### DEBUG режим

```python
# settings.py
DEBUG = True  # Розробка
DEBUG = False  # Продакшн
```

**Коли `DEBUG = True`:**
✅ Детальні повідомлення про помилки
✅ Traceback у браузері
✅ Список маршрутів при 404

**Коли `DEBUG = False`:**
❌ Користувачі не бачать деталі помилок
✅ Тільки загальні сторінки помилок (404, 500)

### Типові помилки

#### 1. Застосунок не зареєстрований

```python
# Помилка: ModuleNotFoundError

# Рішення: додати в INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'your_app',
]
```

#### 2. URL не знайдено (404)

```
Page not found (404)
Request URL: http://127.0.0.1:8000/lesson1/
```

**Причини:**
- Не створено `urls.py` у застосунку
- Не додано `include()` у проекті
- Помилка в шаблоні URL

#### 3. View не існує

```python
# Помилка: AttributeError: module 'app.views' has no attribute 'index'

# Рішення: створити функцію у views.py
def index(request):
    return HttpResponse("...")
```

### Автоматичне перезавантаження

Django автоматично перезавантажує сервер при змінах у коді.

**Коли потрібне ручне перезавантаження:**
- Зміни в налаштуваннях
- Додавання нових файлів
- Міграції БД

```bash
# Зупинити: Ctrl+C
# Запустити знову
python manage.py runserver
```

## 12. Корисні команди Django

```bash
# Створення проекту
django-admin startproject project_name

# Створення застосунку
python manage.py startapp app_name

# Запуск сервера
python manage.py runserver

# Запуск на іншому порту
python manage.py runserver 8080

# Міграції (пізніше)
python manage.py makemigrations
python manage.py migrate

# Створення суперкористувача (адмін)
python manage.py createsuperuser

# Shell для експериментів
python manage.py shell

# Перевірка налаштувань
python manage.py check
```

## 13. Найкращі практики

### Структура проекту

```
myproject/
├── venv/                  # Віртуальне середовище (не в Git!)
├── myproject/             # Налаштування проекту
│   ├── settings.py
│   └── urls.py
├── app1/                  # Застосунок 1
│   ├── urls.py
│   └── views.py
├── app2/                  # Застосунок 2
├── manage.py
└── .gitignore             # Виключення для Git
```

### `.gitignore` для Django

```
# Віртуальне середовище
venv/
env/

# База даних
*.sqlite3
db.sqlite3

# Python
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
*.swp

# Налаштування
local_settings.py
.env
```

### Безпека

**❌ НІКОЛИ не публікуйте:**
```python
SECRET_KEY = 'django-insecure-your-secret-key'
```

**✅ Використовуйте змінні оточення:**
```python
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
```

### Організація URLs

```python
# Проект: urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('shop/', include('shop.urls')),
    path('users/', include('users.urls')),
]

# Застосунок: blog/urls.py
urlpatterns = [
    path('', views.post_list),           # /blog/
    path('<int:id>/', views.post_detail), # /blog/123/
]
```

## 14. Наступні кроки

**Що вивчати далі:**
1. **Models** - робота з базами даних через ORM
2. **Templates** - динамічні HTML-шаблони
3. **Forms** - обробка форм
4. **Admin** - налаштування адмін-панелі
5. **Authentication** - реєстрація та авторизація
6. **Static files** - CSS, JavaScript, зображення
7. **Deployment** - розгортання на сервері

## Домашнє завдання

### Завдання 1: Базовий проект
1. Створити проект `mysite`
2. Створити застосунок `pages`
3. Додати 3-4 маршрути з різними сторінками
4. Використати як `path()`, так і `re_path()`

### Завдання 2: Динамічні маршрути
1. Створити маршрут `/users/<int:id>/`
2. Створити маршрут `/articles/<slug:slug>/`
3. View повинні показувати отримані параметри

### Завдання 3: Regex
1. Створити маршрут через `re_path()` для статей
2. Шаблон повинен дозволяти літери, цифри та дефіс
3. Обов'язково використати `^` та `$`

## Корисні посилання

- **Офіційна документація:** https://docs.djangoproject.com/
- **Django Girls Tutorial:** https://tutorial.djangogirls.org/
- **Real Python Django:** https://realpython.com/tutorials/django/
- **Django Packages:** https://djangopackages.org/

---

**Ключові висновки:**
- Django - потужний фреймворк з великою спільнотою
- MTV патерн замість MVC
- Модульна архітектура (проект + застосунки)
- Маршрутизація через `urls.py`
- Логіка у `views.py`
- Для продакшну: `DEBUG=False`, змінні оточення для секретів