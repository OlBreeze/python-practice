# Django Ninja: Современный подход к созданию API

## Содержание
1. [Введение](#введение)
2. [Базовые концепции REST API](#базовые-концепции-rest-api)
3. [Django Ninja vs Django REST Framework](#django-ninja-vs-django-rest-framework)
4. [Установка и настройка](#установка-и-настройка)
5. [Создание моделей и схем](#создание-моделей-и-схем)
6. [CRUD операции](#crud-операции)
7. [Документация Swagger](#документация-swagger)
8. [Практические примеры](#практические-примеры)

---

## Введение

**Django Ninja** — современный фреймворк для создания API в Django, построенный на основе FastAPI и Pydantic. Он предоставляет высокую производительность, автоматическую валидацию данных и интерактивную документацию.

### Ключевые преимущества:
- 🚀 **Высокая производительность** благодаря асинхронной архитектуре
- ✅ **Автоматическая валидация** через Pydantic
- 📚 **Интерактивная документация** Swagger из коробки
- 🎯 **Современный синтаксис** с type hints и аннотациями
- 🔄 **Простая интеграция** с существующими Django проектами

---

## Базовые концепции REST API

### Что такое REST?

**REST** (Representational State Transfer) — архитектурный стиль для создания распределенных гипермедиа-систем.

**API** (Application Programming Interface) — это набор правил, протоколов и инструментов, который позволяет разным программам и сервисам взаимодействовать друг с другом и обмениваться данными. По сути, это «посредник» или «мост», который даёт одной программе возможность запрашивать функции или данные у другой, не вдаваясь в детали её внутренней работы

#### Основные принципы REST:

1. **Ресурсы** — любая информация, доступная через URI
   - Пользователи: `/api/users/`
   - Конкретный пользователь: `/api/users/5/`
   - Продукты: `/api/products/`

2. **HTTP методы**:
   - `GET` — получение ресурса
   - `POST` — создание нового ресурса
   - `PUT` — полное обновление ресурса
   - `PATCH` — частичное обновление ресурса
   - `DELETE` — удаление ресурса

3. **Stateless** — каждый запрос содержит всю необходимую информацию
4. **Единый интерфейс** — стандартизированные методы взаимодействия

### CRUD операции

**CRUD** — Create, Read, Update, Delete:
- **C**reate → POST
- **R**ead → GET (список и детали)
- **U**pdate → PUT/PATCH
- **D**elete → DELETE

---

## Django Ninja vs Django REST Framework

| Характеристика | Django Ninja | Django REST Framework |
|---------------|--------------|----------------------|
| **Производительность** | Высокая (FastAPI + Pydantic) | Средняя |
| **Валидация** | Pydantic (type hints) | Serializers |
| **Документация** | Автоматическая (Swagger) | Требует настройки |
| **Асинхронность** | Встроенная поддержка | Ограниченная |
| **Сложность** | Проще для новых API | Больше абстракций |
| **Синтаксис** | Современный Python | Классический Django |

---

## Установка и настройка

### Шаг 1: Создание проекта

```bash
# Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка Django и Django Ninja
pip install django
pip install django-ninja

# Создание проекта
django-admin startproject myproject
cd myproject

# Создание приложения
python manage.py startapp tasks
```

### Шаг 2: Настройка settings.py

```python
# myproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja',
    # Ваши приложения
    'tasks',
]

# Настройки базы данных (по умолчанию SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Шаг 3: Настройка URLs

```python
# myproject/urls.py

from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from tasks.api import router as tasks_router

# Создание экземпляра API
api = NinjaAPI(title="To-Do List API")

# Регистрация маршрутов
api.add_router("/tasks", tasks_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),  # Все API endpoints под /api/
]
```

---

## Создание моделей и схем

### Модель Django

```python
# tasks/models.py

from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    completed = models.BooleanField(default=False, verbose_name="Завершено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

### Схемы Pydantic

```python
# tasks/schemas.py

from ninja import Schema
from datetime import datetime
from typing import Optional

# Схема для входных данных (создание)
class TaskIn(Schema):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Схема для выходных данных (ответ)
class TaskOut(Schema):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    
    class Config:
        # Включает работу с ORM моделями Django
        orm_mode = True
```

### Миграции

```bash
# Создание миграций
python manage.py makemigrations

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser
```

---

## CRUD операции

### Полный пример API endpoints

```python
# tasks/api.py

from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List, Optional
from .models import Task
from .schemas import TaskIn, TaskOut

router = Router()

# CREATE - Создание задачи
@router.post("/", response=TaskOut)
def create_task(request, data: TaskIn):
    """
    Создание новой задачи
    """
    task = Task.objects.create(**data.dict())
    return task

# READ - Получение списка задач
@router.get("/", response=List[TaskOut])
def list_tasks(request, completed: Optional[bool] = None):
    """
    Получение списка всех задач с опциональной фильтрацией
    """
    tasks = Task.objects.all()
    
    # Фильтрация по статусу выполнения
    if completed is not None:
        tasks = tasks.filter(completed=completed)
    
    return tasks

# READ - Получение конкретной задачи
@router.get("/{task_id}", response=TaskOut)
def get_task(request, task_id: int):
    """
    Получение задачи по ID
    """
    task = get_object_or_404(Task, id=task_id)
    return task

# UPDATE - Обновление задачи (PUT)
@router.put("/{task_id}", response=TaskOut)
def update_task(request, task_id: int, data: TaskIn):
    """
    Полное обновление задачи
    """
    task = get_object_or_404(Task, id=task_id)
    
    # Обновление полей
    for attr, value in data.dict().items():
        if value is not None:
            setattr(task, attr, value)
    
    task.save()
    return task

# UPDATE - Частичное обновление (PATCH)
@router.patch("/{task_id}", response=TaskOut)
def partial_update_task(request, task_id: int, data: TaskIn):
    """
    Частичное обновление задачи
    """
    task = get_object_or_404(Task, id=task_id)
    
    # Обновляем только переданные поля
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(task, attr, value)
    
    task.save()
    return task

# DELETE - Удаление задачи
@router.delete("/{task_id}")
def delete_task(request, task_id: int):
    """
    Удаление задачи
    """
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return {"success": True}
```

### Bulk операции

```python
# Массовое создание задач
@router.post("/bulk", response=List[TaskOut])
def bulk_create_tasks(request, data: List[TaskIn]):
    """
    Массовое создание задач
    """
    tasks = [Task(**item.dict()) for item in data]
    Task.objects.bulk_create(tasks)
    return tasks
```

---

## Документация Swagger

### Автоматическая документация

После запуска сервера документация доступна по адресу:
- **Swagger UI**: `http://127.0.0.1:8000/api/docs`
- **ReDoc**: `http://127.0.0.1:8000/api/redoc`

### Запуск сервера

```bash
python manage.py runserver
```

### Особенности Swagger в Django Ninja:

1. **Интерактивное тестирование** — можно выполнять запросы прямо из браузера
2. **Автоматическая валидация** — показывает обязательные поля
3. **Примеры данных** — генерирует примеры JSON
4. **Документация методов** — отображает docstrings функций

---

## Практические примеры

### Пример 1: Интернет-магазин

```python
# shop/models.py

from django.db import models
from decimal import Decimal

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Цена"
    )
    in_stock = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

```python
# shop/schemas.py

from ninja import Schema
from datetime import datetime
from typing import Optional
from decimal import Decimal

class ItemIn(Schema):
    name: str
    description: Optional[str] = None
    price: Decimal
    in_stock: bool = True

class ItemOut(Schema):
    id: int
    name: str
    description: Optional[str]
    price: Decimal
    in_stock: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ItemUpdate(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    in_stock: Optional[bool] = None
```

```python
# shop/api.py

from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List, Optional
from .models import Item
from .schemas import ItemIn, ItemOut, ItemUpdate

router = Router()

@router.post("/", response=ItemOut)
def create_item(request, data: ItemIn):
    """Создание нового товара"""
    item = Item.objects.create(**data.dict())
    return item

@router.get("/", response=List[ItemOut])
def list_items(request, 
               name: Optional[str] = None,
               in_stock: Optional[bool] = None,
               min_price: Optional[float] = None,
               max_price: Optional[float] = None):
    """
    Получение списка товаров с фильтрацией:
    - name: поиск по названию
    - in_stock: фильтр по наличию
    - min_price: минимальная цена
    - max_price: максимальная цена
    """
    items = Item.objects.all()
    
    if name:
        items = items.filter(name__icontains=name)
    
    if in_stock is not None:
        items = items.filter(in_stock=in_stock)
    
    if min_price is not None:
        items = items.filter(price__gte=min_price)
    
    if max_price is not None:
        items = items.filter(price__lte=max_price)
    
    return items

@router.get("/{item_id}", response=ItemOut)
def get_item(request, item_id: int):
    """Получение товара по ID"""
    item = get_object_or_404(Item, id=item_id)
    return item

@router.put("/{item_id}", response=ItemOut)
def update_item(request, item_id: int, data: ItemUpdate):
    """Обновление товара"""
    item = get_object_or_404(Item, id=item_id)
    
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(item, attr, value)
    
    item.save()
    return item

@router.delete("/{item_id}")
def delete_item(request, item_id: int):
    """Удаление товара"""
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return {"success": True, "message": "Товар успешно удален"}

@router.post("/bulk", response=List[ItemOut])
def bulk_create_items(request, data: List[ItemIn]):
    """Массовое создание товаров"""
    items = [Item(**item.dict()) for item in data]
    Item.objects.bulk_create(items)
    return items
```

### Пример 2: Тестирование с Postman

#### Создание товара (POST)
```json
POST http://127.0.0.1:8000/api/items/

Body (JSON):
{
    "name": "Ноутбук Dell XPS 15",
    "description": "Мощный ноутбук для разработки",
    "price": 1299.99,
    "in_stock": true
}

Response (201 Created):
{
    "id": 1,
    "name": "Ноутбук Dell XPS 15",
    "description": "Мощный ноутбук для разработки",
    "price": "1299.99",
    "in_stock": true,
    "created_at": "2025-11-19T20:30:00Z",
    "updated_at": "2025-11-19T20:30:00Z"
}
```

#### Получение списка (GET)
```json
GET http://127.0.0.1:8000/api/items/?in_stock=true&min_price=1000

Response (200 OK):
[
    {
        "id": 1,
        "name": "Ноутбук Dell XPS 15",
        "description": "Мощный ноутбук для разработки",
        "price": "1299.99",
        "in_stock": true,
        "created_at": "2025-11-19T20:30:00Z",
        "updated_at": "2025-11-19T20:30:00Z"
    }
]
```

#### Обновление товара (PUT)
```json
PUT http://127.0.0.1:8000/api/items/1/

Body (JSON):
{
    "name": "Ноутбук Dell XPS 15 (Обновлено)",
    "price": 1199.99
}

Response (200 OK):
{
    "id": 1,
    "name": "Ноутбук Dell XPS 15 (Обновлено)",
    "description": "Мощный ноутбук для разработки",
    "price": "1199.99",
    "in_stock": true,
    "created_at": "2025-11-19T20:30:00Z",
    "updated_at": "2025-11-19T20:35:00Z"
}
```

#### Удаление товара (DELETE)
```json
DELETE http://127.0.0.1:8000/api/items/1/

Response (204 No Content):
{
    "success": true,
    "message": "Товар успешно удален"
}
```

### Пример 3: Массовое создание

```json
POST http://127.0.0.1:8000/api/items/bulk

Body (JSON):
[
    {
        "name": "iPhone 15 Pro",
        "description": "Флагманский смартфон",
        "price": 999.99,
        "in_stock": true
    },
    {
        "name": "MacBook Pro 16",
        "description": "Профессиональный ноутбук",
        "price": 2499.99,
        "in_stock": true
    },
    {
        "name": "AirPods Pro",
        "description": "Беспроводные наушники",
        "price": 249.99,
        "in_stock": false
    }
]
```

---

## Дополнительные возможности

### Аутентификация

```python
# auth.py

from ninja.security import HttpBearer

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # Простая проверка токена
        if token == "supersecrettoken":
            return token
        return None

# Использование в API
@router.get("/protected", auth=AuthBearer())
def protected_endpoint(request):
    return {"message": "Доступ разрешен"}
```

### Пагинация

```python
from ninja.pagination import paginate, PageNumberPagination

@router.get("/", response=List[ItemOut])
@paginate(PageNumberPagination, page_size=10)
def list_items(request):
    return Item.objects.all()
```

### Обработка ошибок

```python
from ninja import Router
from ninja.errors import HttpError

@router.get("/{item_id}")
def get_item(request, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        return item
    except Item.DoesNotExist:
        raise HttpError(404, "Товар не найден")
```

---

## Резюме

### Основные выводы:

1. **Django Ninja** — современная альтернатива DRF с лучшей производительностью
2. **Pydantic схемы** обеспечивают автоматическую валидацию данных
3. **Swagger** генерируется автоматически без дополнительной настройки
4. **Type hints** делают код более читаемым и безопасным
5. **Простая интеграция** с существующими Django проектами

### Когда использовать Django Ninja:

✅ Новые API проекты  
✅ Когда важна производительность  
✅ Нужна автоматическая документация  
✅ Работа с современным Python синтаксисом  
✅ Асинхронные операции

### Полезные ресурсы:

- [Официальная документация Django Ninja](https://django-ninja.rest-framework.com/)
- [Pydantic документация](https://docs.pydantic.dev/)
- [Swagger/OpenAPI спецификация](https://swagger.io/specification/)

---

**Успехов в разработке API! 🚀**

---
Давайте я перепроверю лекцию на предмет точности содержания и определений, используя актуальную информацию.  
Проанализировав лекцию и актуальную информацию из открытых источников, могу подтвердить следующее:

## ✅ Что правильно в лекции:

1. **Django Ninja** - действительно построен на основе FastAPI и Pydantic ✅
2. **Pydantic** - это библиотека для валидации данных ✅
3. **Swagger UI** генерируется автоматически ✅
4. **Высокая производительность** благодаря Pydantic ✅
5. **Type hints** и современный синтаксис ✅
6. **Асинхронность** - встроенная поддержка ✅

## ⚠️ Что требует уточнения:

### 1. **Неточность о "построен на базе FastAPI"**

В лекции сказано:
> "побудований він на базі fast API і Pidentic"

**Уточнение**: Django Ninja **вдохновлен** FastAPI, но НЕ построен на его базе. Это независимый фреймворк, который использует похожие концепции (Pydantic, type hints, автоматическую документацию), но работает поверх Django, а не FastAPI.

Django Ninja - это веб-фреймворк для создания API с Django и Python 3.6+ type hints, основанный на открытых стандартах OpenAPI и JSON Schema.

### 2. **Продуктивность через асинхронность**

В лекции говорится о высокой производительности за счет асинхронности. 

**Уточнение**: Основной прирост производительности идет от **Pydantic** (ядро написано на Rust), а не только от асинхронности. Ядро валидации Pydantic написано на Rust, что делает его одной из самых быстрых библиотек валидации данных для Python.

### 3. **Не упомянута важная деталь**

Django Ninja требует **Python 3.7+** (не 3.6+ как было раньше) и поддерживает Django версии 3.1 - 5.2.

## 📝 Рекомендации по исправлению:

Вместо:
```
побудований він на базі fast API і Pidentic
```

Правильнее:
```
вдохновлений Fast API та використовує Pydantic для валідації
```

