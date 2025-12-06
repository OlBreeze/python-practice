django-admin startproject task_manager  
python manage.py startapp main
 
python manage.py makemigrations  
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

pip install django-ninja-jwt
pip install django-ninja-extra

pip install Django channels channels-redis redis

---
 git add .   
 git commit -m "Lesson24/homework"   
 git push -u origin main  
---

### выгрузить зависимости проекта Python
pip freeze > requirements.txt

### установить зависимости из этого файла
pip install -r requirements.txt

### Запуск проекта на порту
 uvicorn app.main:app --reload --port 8002
---
#### Django Debug Toolbar
pip install django-debug-toolbar

---
"""
# Створення міграцій
python manage.py makemigrations

# Застосування міграцій
python manage.py migrate

# Створення суперкористувача
python manage.py createsuperuser

# Збір статичних файлів
python manage.py collectstatic

# Запуск сервера розробки
python manage.py runserver

# Перегляд метрик
python manage.py show_metrics

# Запуск тестів
python manage.py test blog
"""
## асинхронная база на фастАПИ
pip install aiosqlite sqlalchemy[asyncio]


# Стандартный запуск FastAPI (порт 8000)
uvicorn main:app --reload

# На кастомном порту
uvicorn main:app --reload --port 8002



## 🧩 1. Что такое DRF

**Django REST Framework (DRF)** — это **дополнение** к Django, которое помогает создавать **API** (интерфейсы для обмена
данными между системами).

> То есть: DRF — не «встроенная» часть Django, а **отдельная библиотека**, которую ты **устанавливаешь через pip** (
`pip install djangorestframework`) и подключаешь в проект.

Она помогает:

* сериализовать (преобразовывать) объекты моделей Django в JSON (и обратно),
* обрабатывать запросы типа `GET`, `POST`, `PUT`, `DELETE` через API,
* предоставлять готовые классы представлений (`APIView`, `ViewSet`),
* управлять правами доступа, пагинацией, фильтрацией и т.д.

---

## 📚 2. Пример структуры приложения «Библиотека»

Допустим, у тебя проект называется `library_project`, а приложение — `books`.

```
library_project/
│
├── library_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── books/
│   ├── models.py        # модели (например, Book, Author)
│   ├── views.py         # обычные Django вьюхи для HTML-страниц
│   ├── urls.py          # маршруты приложения
│   ├── forms.py         # формы для HTML
│   ├── templates/       # шаблоны для отображения страниц
│   ├── admin.py         # регистрация моделей в админке
│   ├── serializers.py   # (DRF) сериализаторы для API
│   ├── api_views.py     # (DRF) вьюхи для API
│   └── api_urls.py      # (DRF) маршруты для API
│
└── manage.py
```

---

## ⚙️ 3. Состав приложения: «всё сразу»

| Компонент                 | Для чего                                | Пример                                    |
|---------------------------|-----------------------------------------|-------------------------------------------|
| **models.py**             | связь с базой данных                    | `Book`, `Author`                          |
| **admin.py**              | админ-панель Django                     | управление книгами                        |
| **forms.py**              | формы для HTML-страниц                  | добавление книги вручную                  |
| **views.py + templates/** | обычные веб-страницы                    | список книг, страница книги               |
| **serializers.py**        | преобразование моделей в JSON (для API) | `BookSerializer`                          |
| **api\_views.py**         | обработка API-запросов (DRF)            | список книг через `APIView` или `ViewSet` |
| **api\_urls.py**          | маршруты API                            | `/api/books/`, `/api/books/1/`            |

---

## 🔁 4. Пример — API для модели Book

```python
# books/models.py
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published = models.DateField()

    def __str__(self):
        return self.title
```

```python
# books/serializers.py
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

```python
# books/api_views.py
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

```python
# books/api_urls.py
from rest_framework.routers import DefaultRouter
from .api_views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = router.urls
```

```python
# library_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),  # обычные страницы
    path('api/', include('books.api_urls')),  # API
]
```

Теперь:

* `/books/` → обычная HTML-страница (через Django templates),
* `/api/books/` → REST API (JSON).

---

## 💡 5. Вывод

| Задача              | Где реализуется                                        |
|---------------------|--------------------------------------------------------|
| Хранение данных     | `models.py`                                            |
| Отображение страниц | `views.py` + `templates/`                              |
| Администрирование   | `admin.py`                                             |
| Работа с API        | `DRF`: `serializers.py`, `api_views.py`, `api_urls.py` |

---