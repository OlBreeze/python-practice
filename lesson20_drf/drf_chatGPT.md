
**DRF (Django REST Framework)** — это мощная библиотека для Django, которая облегчает создание **RESTful API**.
Она расширяет возможности стандартного Django и позволяет быстро и удобно создавать бэкенды для веб-и мобильных приложений.

---

## 🔹 Что такое REST API

**REST (Representational State Transfer)** — это архитектурный стиль взаимодействия клиент–сервер, основанный на:

* HTTP-методах (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`);
* использовании URL для обозначения ресурсов (например, `/api/books/1/`);
* передаче данных в формате JSON.

---

## 🔹 Основные возможности Django REST Framework

| Возможность                      | Описание                                               |
| -------------------------------- | ------------------------------------------------------ |
| **Сериализация данных**          | Преобразует Django-модели в JSON и обратно.            |
| **ViewSets и Generic Views**     | Упрощают написание CRUD-операций.                      |
| **Аутентификация и авторизация** | Поддерживает токены, JWT, OAuth2 и др.                 |
| **Права доступа (Permissions)**  | Позволяют ограничивать доступ к API.                   |
| **Пагинация**                    | Делит большие наборы данных на страницы.               |
| **Фильтрация и поиск**           | Простая интеграция с `django-filter` и `SearchFilter`. |
| **Browsable API**                | Красивый и удобный веб-интерфейс для тестирования API. |

---

## 🔹 Пример: CRUD для модели книги

**models.py**

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return self.title
```

**serializers.py**

```python
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
```

**views.py**

```python
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

**urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

Теперь можно обращаться к:

* `GET /api/books/` — список книг
* `POST /api/books/` — добавить книгу
* `GET /api/books/1/` — получить книгу
* `PUT /api/books/1/` — обновить книгу
* `DELETE /api/books/1/` — удалить книгу

---

## 🔹 Пример интерфейса DRF

Когда ты откроешь `http://127.0.0.1:8000/api/books/`, DRF покажет удобный браузерный интерфейс:

* формы для отправки запросов;
* список доступных эндпоинтов;
* JSON-ответы прямо в браузере.

---

## 🔹 Когда использовать DRF

Используй Django REST Framework, когда:

* тебе нужно API для SPA (React, Vue, Angular);
* создаёшь мобильное приложение с сервером на Django;
* хочешь гибкую систему авторизации и прав доступа;
* важно быстро построить надёжный и масштабируемый бэкенд.

---

## 🔐 Часть 1. JWT-аутентификация

**JWT (JSON Web Token)** — это способ безопасной авторизации без сохранения сессий на сервере.
Пользователь логинится → получает токен → прикрепляет его к каждому запросу.

---

### 🔸 Установка

```bash
pip install djangorestframework-simplejwt
```

---

### 🔸 Настройка в `settings.py`

```python
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'myapp',  # твое приложение
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

---

### 🔸 Настройка URL для токенов

В `urls.py`:

```python
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновление токена
    path('api/', include('myapp.urls')),
]
```

---

### 🔸 Как это работает

1. Пользователь отправляет `POST` на `/api/token/`:

   ```json
   {
     "username": "olga",
     "password": "12345"
   }
   ```

2. В ответ получает:

   ```json
   {
     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
   }
   ```

3. Теперь любой защищённый запрос нужно делать с заголовком:

   ```
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...
   ```

---

### 🔸 Ограничим доступ к книгам только для авторизованных пользователей

В `views.py`:

```python
from rest_framework import viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
```

Теперь:

* если пользователь не авторизован → `401 Unauthorized`;
* если авторизован → может выполнять CRUD-операции.

---

## 🔍 Часть 2. Фильтрация по полям

Часто нужно искать книги, например, по автору или году.
Для этого удобно использовать `django-filter`.

---

### 🔸 Установка

```bash
pip install django-filter
```

---

### 🔸 Настройка в `settings.py`

```python
INSTALLED_APPS += ['django_filters']

REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = (
    'django_filters.rest_framework.DjangoFilterBackend',
)
```

---

### 🔸 Настройка фильтров в `views.py`

```python
from django_filters.rest_framework import DjangoFilterBackend

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'year']
```

---

### 🔸 Пример запроса

```
GET /api/books/?author=Orwell
GET /api/books/?year=2024
```

Можно комбинировать:

```
GET /api/books/?author=Orwell&year=2024
```

---
