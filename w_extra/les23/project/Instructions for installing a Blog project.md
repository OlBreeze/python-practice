# 📦 Повна інструкція по встановленню Django Blog проекту

## 📂 Структура проекту

```
project/                          # Головна папка проекту
├── project/                      # Папка налаштувань
│   ├── __init__.py
│   ├── settings.py              # ← Артефакт "Файли конфігурації"
│   ├── urls.py                  # ← Артефакт "Файли конфігурації"
│   ├── wsgi.py
│   └── asgi.py
├── blog/                         # Додаток блогу
│   ├── __init__.py
│   ├── models.py                # ← Артефакт 1
│   ├── forms.py                 # ← Артефакт 2
│   ├── admin.py                 # ← Артефакт 3
│   ├── views.py                 # ← Артефакт 5
│   ├── api_views.py             # ← Артефакт 7
│   ├── serializers.py           # ← Артефакт 7
│   ├── urls.py                  # ← Артефакт "Файли конфігурації"
│   ├── api_urls.py              # ← Артефакт "Файли конфігурації"
│   ├── middleware.py            # ← Артефакт 5
│   ├── signals.py               # ← Артефакт 8
│   ├── queries.py               # ← Артефакт 8
│   ├── metrics.py               # ← Артефакт 9
│   ├── logging_config.py        # ← Артефакт 9
│   ├── context_processors.py    # ← Артефакт "Файли конфігурації"
│   ├── apps.py
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── blog_tags.py         # ← Артефакт 4
│   └── management/
│       └── commands/
│           └── show_metrics.py  # ← Артефакт 9
├── templates/                    # Шаблони
│   ├── base.html                # ← Шаблони
│   ├── blog/
│   │   ├── article_list.html
│   │   ├── article_detail.html
│   │   ├── article_form.html
│   │   ├── search_results.html
│   │   ├── tagged_articles.html
│   │   ├── user_articles.html
│   │   └── tags/
│   │       ├── article_card.html
│   │       ├── popular_tags.html
│   │       └── breadcrumbs.html
│   └── widgets/
│       └── tag_select.html
├── static/                       # Статичні файли
├── media/                        # Медіа файли
├── logs/                         # Логи
├── manage.py
└── requirements.txt              # ← Артефакт "Файли конфігурації"
```

## 🚀 Покрокове встановлення

### Крок 1: Створення проекту

```bash
# Створити головний проект
django-admin startproject project
cd project

# Створити додаток
python manage.py startapp blog

# Створити додаткові папки
mkdir templates
mkdir templates/blog
mkdir templates/blog/tags
mkdir templates/widgets
mkdir static
mkdir media
mkdir logs
```

### Крок 2: Встановлення залежностей

Створіть `requirements.txt`:
```txt
Django==4.2.7
djangorestframework==3.14.0
django-filter==23.3
django-cors-headers==4.3.0
psycopg2-binary==2.9.9
redis==5.0.1
django-redis==5.4.0
Pillow==10.1.0
python-dotenv==1.0.0
gunicorn==21.2.0
python-json-logger==2.0.7
drf-spectacular==0.27.0
```

Встановіть:
```bash
pip install -r requirements.txt
```

### Крок 3: Налаштування settings.py

Змініть `project/settings.py` (використайте артефакт "Файли конфігурації"), але **ВАЖЛИВО**:

```python
# В INSTALLED_APPS додайте
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_spectacular',  # ← Замість coreapi
    
    # Local
    'blog',
]

# Налаштування шаблонів
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← ВАЖЛИВО!
        'APP_DIRS': True,
        ...
    },
]

# Кастомна модель користувача
AUTH_USER_MODEL = 'blog.CustomUser'

# База даних (для початку SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Статичні файли
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медіа
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Крок 4: Налаштування URLs

**project/urls.py** (БЕЗ coreapi):
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('api/', include('blog.api_urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # API документація
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### Крок 5: Копіювання файлів з артефактів

Скопіюйте весь код з артефактів у відповідні файли:

1. **models.py** ← Артефакт 1
2. **forms.py** ← Артефакт 2
3. **admin.py** ← Артефакт 3
4. **templatetags/blog_tags.py** ← Артефакт 4
5. **views.py, middleware.py** ← Артефакт 5
6. **serializers.py, api_views.py** ← Артефакт 7
7. **signals.py, queries.py** ← Артефакт 8
8. **metrics.py, logging_config.py** ← Артефакт 9
9. **context_processors.py** ← З артефакту конфігурації
10. Всі **HTML шаблони** ← З артефактів шаблонів

### Крок 6: Налаштування signals

Створіть `blog/apps.py`:
```python
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    
    def ready(self):
        import blog.signals  # Імпорт сигналів
```

Переконайтеся що в `blog/__init__.py`:
```python
default_app_config = 'blog.apps.BlogConfig'
```

### Крок 7: Створення міграцій та БД

```bash
# Створити міграції
python manage.py makemigrations

# Застосувати міграції
python manage.py migrate

# Створити суперкористувача
python manage.py createsuperuser
```

### Крок 8: Створення тестових даних (опціонально)

```bash
python manage.py shell
```

В shell:
```python
from blog.models import Article, Tag, CustomUser

# Отримати суперкористувача
user = CustomUser.objects.first()

# Створити теги
tag1 = Tag.objects.create(name='Python')
tag2 = Tag.objects.create(name='Django')

# Створити статтю
article = Article.objects.create(
    title='Моя перша стаття',
    slug='moya-persha-stattya',
    author=user,
    content='Це тестова стаття з великим текстом. ' * 50,
    status='published'
)

# Додати теги
article.tags.add(tag1, tag2)

print("Дані створено!")
exit()
```

### Крок 9: Запуск сервера

```bash
python manage.py runserver
```

Перейдіть на:
- **http://127.0.0.1:8000/** - головна сторінка
- **http://127.0.0.1:8000/admin/** - адмінка
- **http://127.0.0.1:8000/api/** - API
- **http://127.0.0.1:8000/api/docs/** - документація API

## ✅ Перевірка роботи

### Тест 1: Веб-інтерфейс
- Відкрийте головну - повинен відображатися список статей
- Клікніть на статтю - деталі
- Увійдіть в адмінку - повинні бути всі моделі

### Тест 2: API
```bash
# Отримати статті
curl http://127.0.0.1:8000/api/articles/

# З фільтром
curl "http://127.0.0.1:8000/api/articles/?status=published&ordering=-views_count"
```

### Тест 3: Метрики
```bash
python manage.py show_metrics
```

## 🐛 Поширені помилки

### Помилка: "No module named 'blog'"
**Рішення**: Переконайтеся що `blog` додано в `INSTALLED_APPS`

### Помилка: "TemplateDoesNotExist"
**Рішення**: Перевірте що `DIRS = [BASE_DIR / 'templates']` в settings.py

### Помилка: "Table doesn't exist"
**Рішення**: Запустіть `python manage.py migrate`

### Помилка з coreapi
**Рішення**: Видаліть рядок з `include_docs_urls` або використайте `drf-spectacular`

## 📊 Тестування функціоналу

1. **Кастомні поля**: Створіть статтю - заголовок автоматично стане у верхньому регістрі
2. **Валідація**: Спробуйте створити статтю з коротким заголовком - повинна бути помилка
3. **Адмінка**: Відфільтруйте статті за популярністю
4. **API**: Протестуйте фільтри `/api/articles/?tag=python`
5. **Сигнали**: Створіть статтю - slug згенерується автоматично
6. **Метрики**: Подивіться метрики командою `show_metrics`

## 🎉 Готово!

Ваш Django проект з усіма 10 завданнями кастомізації готовий до роботи!