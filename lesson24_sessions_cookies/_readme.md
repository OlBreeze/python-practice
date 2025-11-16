# Оптимизация и работа с сессиями в Django

## 1. Кастомизация в Django

### Основные возможности кастомизации:
- Шаблоны (templates)
- Модели (models)
- Template tags (кастомные теги)
- Фильтры
- Декораторы
- Middleware

### Зачем нужна кастомизация?
- Сделать интерфейс более гибким и функциональным
- Добавить свою логику там, где это необходимо
- Закрыть пробелы в безопасности

### Middleware
**Назначение:** Предотвращение утечки данных и махинаций, дополнительный слой безопасности.

**Создание кастомного middleware:**
1. Создать модуль `middlewares.py`
2. Написать код middleware
3. Активировать через `settings.py`

---

## 2. Django ORM (Object-Relational Mapping)

### Что даёт ORM?
- Замена SQL-синтаксиса на Python-код
- Работа с моделями
- Использование в шаблонах
- Работа с формами
- Универсальность для разных СУБД (PostgreSQL, MySQL, SQLite)
- Мощный инструмент миграций

### Выбор базы данных
В `settings.py` можно указать тип БД:
- SQLite (по умолчанию)
- PostgreSQL
- MySQL
- NoSQL

**Важно:** Код остаётся одинаковым для любой БД!

---

## 3. Сессии и Cookies

### Что такое сессии?
**Сессия** — способ хранения данных на сервере, привязанных к конкретному пользователю.

- Браузер хранит только Session ID
- Данные хранятся на сервере (в БД, файлах или кеше)

### Что такое Cookies?
**Cookies** — небольшие фрагменты данных, которые браузер хранит локально.

### Сравнение Sessions и Cookies

| Параметр | Cookies | Sessions |
|----------|---------|----------|
| **Хранение** | У клиента (браузер) | На сервере |
| **Безопасность** | Низкая | Высокая |
| **Размер** | До 4 KB | Неограничен |
| **Доступ JS** | Да (если не HttpOnly) | Нет |

### Использование
**Cookies:**
- Сохранение настроек
- Цветовые темы
- Языки

**Sessions:**
- Корзины покупок
- Авторизация
- Профили пользователей
- Данные профиля

---

## 4. Работа с сессиями в Django

### Как работают сессии?

1. Пользователь открывает сайт
2. Сервер создаёт сессию и возвращает Cookie с Session ID
3. При следующих запросах браузер отправляет Cookie
4. Сервер извлекает сессию из памяти

### Встроенная система сессий Django

**Настройка в `settings.py`:**
```python
INSTALLED_APPS = [
    ...
    'django.contrib.sessions',
    ...
]

MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    ...
]
```

### API для работы с сессиями
```python
# Простой API
request.session

# Прозрачная работа с cookies
# Поддержка разных бэкендов
```

---

## 5. Настройка хранения сессий

### Вариант 1: База данных (по умолчанию)
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
```

### Вариант 2: Файлы
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = BASE_DIR / 'sessions'  # или '/tmp/django_sessions'
```

### Вариант 3: Кеш (самый быстрый)
```python
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
    'default': {
        # настройки кеша
    }
}
```

---

## 6. Работа с Cookies в Django

### Установка Cookie
```python
def set_cookie(request):
    response = HttpResponse()
    response.set_cookie('username', 'test_user', max_age=3600)  # 3600 сек = 1 час
    return response
```

### Чтение Cookie
```python
def get_cookie(request):
    username = request.cookies.get('username', 'guest')
    return HttpResponse(f'Hello {username}')
```

### Удаление Cookie
```python
def delete_cookie(request):
    response = HttpResponse()
    response.delete_cookie('username')
    return response
```

### Работа с корзиной
```python
def add_to_cart(request):
    request.session['cart'] = {
        'item_1': ...,
        'item_2': ...,
        'item_3': ...,
    }
    return HttpResponse('Added to cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    return HttpResponse(str(cart))
```

---

## 7. Безопасность

### CSRF Protection
**CSRF (Cross-Site Request Forgery)** — атака, позволяющая злоумышленнику заставить авторизованного пользователя выполнить нежелательные действия.

**Защита в Django:**
- CSRF protection включён по умолчанию
- Использование `{% csrf_token %}` в формах

### Настройки безопасности в `settings.py`
```python
# Время жизни сессии (в секундах)
SESSION_COOKIE_AGE = 86400  # 1 день

# Сессия истекает при закрытии браузера
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Безопасные cookies
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
```

### XSS атаки
**XSS (Cross-Site Scripting)** — позволяет внедрять вредоносный код (JavaScript).

**Риски при работе с Cookies:**
- Легко использовать в XSS атаках
- Ограничение ~4 KB
- Видимы пользователю
- Политика GDPR

---

## 8. Оптимизация сессий и cookies

### Оптимизация сессий
1. **Не хранить большие данные в сессии** — хранить только идентификаторы
2. **Не хранить большие списки** — они занимают много памяти
3. **Использовать кеш для часто изменяемых данных**
4. **Сжатие данных** — использовать JSON при работе с API

### Оптимизация Cookies
1. Минимизировать размер cookie
2. Уменьшать lifetime
3. Избегать конфиденциальных данных

---

## 9. Оптимизация работы с Django ORM

### Базовая модель
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

### Базовые запросы
```python
# Выборка с фильтрацией и сортировкой
products = Product.objects.filter(price__gte=100).order_by('-price')
```

### Агрегация и аннотация

**Агрегация** — группировка и обобщение данных
**Аннотация** — добавление вычисляемых полей

```python
from django.db.models import Avg, Count

# Агрегация: средняя цена
result = Product.objects.aggregate(avg_price=Avg('price'))

# Аннотация: добавление вычисляемого поля
products = Product.objects.annotate(total_sales=Count('sales'))
```

---

## 10. Проблема N+1 и её решение

### Что такое проблема N+1?
При работе с связанными таблицами (ForeignKey, ManyToMany) происходит:
1. Один запрос для получения основных объектов
2. N дополнительных запросов для связанных объектов

### Решение: prefetch_related и select_related

**select_related** — для связей One-to-One и ForeignKey (Many-to-One)
```python
# Плохо: N+1 запросов
products = Product.objects.all()
for product in products:
    print(product.category.name)  # Запрос для каждого продукта!

# Хорошо: 1 запрос с JOIN
products = Product.objects.select_related('category')
```

**prefetch_related** — для ManyToMany и обратных ForeignKey
```python
# Плохо
categories = Category.objects.all()
for category in categories:
    products = category.product_set.all()  # Запрос для каждой категории!

# Хорошо
categories = Category.objects.prefetch_related('product_set')
```
`select_related` и `prefetch_related` — это два ключевых инструмента в Django ORM, которые помогают оптимизировать работу с базой данных и избегать проблемы N+1 запросов. Они оба уменьшают количество SQL-запросов, но делают это по-разному.

---

# 🔵 **select_related**

Используется для **жадной загрузки** (*JOIN*) связанных объектов **по связи ForeignKey или OneToOne**.

## ✔ Как работает

Django делает **JOIN** и получает данные связанных моделей **в одном SQL-запросе**.

## ✔ Когда использовать

* ForeignKey
* OneToOne

## ✔ Пример

```python
# Модель Book имеет ForeignKey на Author
books = Book.objects.select_related('author')

for b in books:
    print(b.author.name)
```

### SQL

Будет примерно так:

```sql
SELECT * FROM book
JOIN author ON book.author_id = author.id;
```

## ✔ Плюсы

* один SQL-запрос вместо N+1
* очень быстро

## ✔ Минусы

* работает **ТОЛЬКО** для FK и OneToOne
* приносит много данных, даже если они не нужны

---

# 🟢 **prefetch_related**

Используется для **отложенной загрузки** через *два запроса* — один для основной модели, второй для связанных объектов. Django объединяет результат уже в Python.

## ✔ Как работает

* Делает два (или больше) SQL-запроса
* Подтягивает связанные объекты отдельным запросом
* Django сопоставляет их в памяти

## ✔ Когда использовать

* ManyToMany
* reverse ForeignKey (`related_name`)
* Сложные связи
* Кастомные кверисеты

## ✔ Пример

```python
# Author имеет ManyToMany к Tag
authors = Author.objects.prefetch_related('tags')

for a in authors:
    print(a.tags.all())
```

### SQL

1. `SELECT * FROM author`
2. `SELECT * FROM tag JOIN author_tag ...`

## ✔ Плюсы

* работает с любыми типами связей
* можно настраивать через Prefetch
* гибче чем select_related

## ✔ Минусы

* минимум два запроса
* больше работы в Python

---

# 🆚 Краткое сравнение

| Характеристика     | select_related                    | prefetch_related                  |
| ------------------ | ---------------------------------- | ---------------------------------- |
| Тип связи          | FK, OneToOne                       | Любые, чаще M2M и reverse          |
| SQL                | JOIN — один запрос                 | 2+ отдельных запроса               |
| Скорость           | Быстро                             | Быстро, но медленнее JOIN          |
| Обработка          | SQL                                | Python                             |
| Когда использовать | "один-к-одному", "многие-к-одному" | "многие-ко-многим", обратные связи |

---

# 🧠 Как выбрать?

* Если связь **одна запись → одна запись** → **select_related**
* Если связь **много записей** → **prefetch_related**
* Если не уверен → обычно **prefetch_related**, т.к. безопаснее


---

## 11. Сложные запросы

### Класс Q для комбинированных условий
```python
from django.db.models import Q

products = Product.objects.filter(
    Q(price__lt=100) | Q(name__icontains='smartphone')
)
```

### Класс F для работы с полями
```python
from django.db.models import F

# Обновить цену на 10%
Product.objects.update(price=F('price') * 1.1)
```

### Raw SQL запросы
```python
products = Product.objects.raw(
    'SELECT * FROM myapp_product WHERE price > %s',
    [100]
)
```

### Использование только нужных полей
```python
# Выбрать только определённые поля
products = Product.objects.filter(price__gt=100).only('name', 'price')

# Исключить ненужные поля
products = Product.objects.defer('description')
```

---

## 12. Системы рекомендаций

Современное направление, основанное на анализе:
- Поведения пользователя
- Времени на странице
- Просмотренных товаров
- Категорий интересов

**Этапы:**
1. Сбор информации (cookies, sessions)
2. Анализ данных
3. Формирование рекомендаций

---

## 13. Request и Response

**Request** — запрос от клиента к серверу
**Response** — ответ от сервера клиенту

Между ними происходит обмен пакетами данных.

---

## 14. Практические примеры

### Счётчик посещений
```python
def visit_counter(request):
    visits = request.COOKIES.get('visits', 0)
    visits = int(visits) + 1
    
    response = HttpResponse(f'Visits: {visits}')
    response.set_cookie('visits', visits)
    return response
```

### Корзина покупок
```python
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return HttpResponse('Added to cart')

def view_cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'cart.html', {'products': products})

def clear_cart(request):
    request.session.flush()
    return HttpResponse('Cart cleared')
```

### Топ-10 товаров
```python
def top_products(request):
    top = Product.objects.order_by('-sales')[:10]
    return render(request, 'top.html', {'products': top})
```

---

## 15. Рекомендации по оптимизации

1. **Использовать только нужные поля** — `only()`, `defer()`
2. **Избегать проблемы N+1** — `select_related()`, `prefetch_related()`
3. **Использовать агрегацию** — вместо Python-циклов
4. **Кешировать часто используемые данные**
5. **Использовать explain() для анализа запросов**
6. **Работать с индексацией и транзакциями**

---

---

## 16. Дополнительные техники оптимизации (расширенный материал)

### Django Debug Toolbar
Незаменимый инструмент для выявления проблем производительности:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    ...
]

INTERNAL_IPS = ['127.0.0.1']
```

**Что показывает:**
- Количество SQL-запросов
- Время выполнения каждого запроса
- Дублирующиеся запросы
- Использование кеша
- Загрузку шаблонов

### Database Indexing
Индексы критически важны для производительности:

```python
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)  # Простой индекс
    sku = models.CharField(max_length=50, unique=True)  # Уникальный индекс
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Составной индекс
        indexes = [
            models.Index(fields=['price', 'created_at']),
            models.Index(fields=['-created_at']),  # Для сортировки DESC
        ]
```

**Когда создавать индексы:**
- Поля для фильтрации (WHERE)
- Поля для сортировки (ORDER BY)
- Внешние ключи (обычно создаются автоматически)
- Поля для поиска (LIKE)

**Когда НЕ создавать:**
- Таблицы с частыми INSERT/UPDATE
- Маленькие таблицы (<1000 строк)
- Поля с низкой уникальностью (boolean)

### Bulk операции
Избегайте циклов с сохранением в БД:

```python
# ❌ Плохо: N запросов
for i in range(1000):
    Product.objects.create(name=f'Product {i}', price=100)

# ✅ Хорошо: 1 запрос
products = [Product(name=f'Product {i}', price=100) for i in range(1000)]
Product.objects.bulk_create(products, batch_size=100)

# Bulk update
products = Product.objects.filter(category='electronics')
products.update(price=F('price') * 1.1)  # 1 запрос вместо N

# Bulk delete
Product.objects.filter(price__lt=10).delete()
```

### Пагинация
Обязательна для больших списков:

```python
from django.core.paginator import Paginator

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    paginator = Paginator(products, 25)  # 25 товаров на страницу
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products.html', {'page_obj': page_obj})
```

```html
<!-- В шаблоне -->
{% for product in page_obj %}
    {{ product.name }}
{% endfor %}

<!-- Навигация -->
<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Назад</a>
    {% endif %}
    
    Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Вперёд</a>
    {% endif %}
</div>
```

---

## 17. Кеширование в Django

### Уровни кеширования

**1. Per-Site кеш (весь сайт):**
```python
# settings.py
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # Первым
    ...
    'django.middleware.cache.FetchFromCacheMiddleware',  # Последним
]

CACHE_MIDDLEWARE_SECONDS = 600  # 10 минут
```

**2. Per-View кеш (отдельные view):**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 минут
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
```

**3. Template Fragment кеш (части шаблона):**
```html
{% load cache %}

{% cache 500 sidebar %}
    <!-- Этот блок кешируется на 500 секунд -->
    <div class="sidebar">
        {% for category in categories %}
            <a href="{{ category.url }}">{{ category.name }}</a>
        {% endfor %}
    </div>
{% endcache %}
```

**4. Low-Level кеш (ручное управление):**
```python
from django.core.cache import cache

# Установить значение
cache.set('my_key', 'my_value', 300)  # 300 секунд

# Получить значение
value = cache.get('my_key', 'default_value')

# Удалить
cache.delete('my_key')

# Получить или установить
def get_expensive_data():
    return Product.objects.aggregate(
        total=Count('id'),
        avg_price=Avg('price')
    )

data = cache.get_or_set('stats', get_expensive_data, 3600)
```

### Настройка Redis для кеша
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myproject',
        'TIMEOUT': 300,
    }
}
```

---

## 18. Безопасность: расширенные практики

### Content Security Policy (CSP)
```python
# settings.py
MIDDLEWARE = [
    ...
    'csp.middleware.CSPMiddleware',
]

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'https://cdn.example.com')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
```

### Защита от брутфорса
```python
from django.core.cache import cache
from django.http import HttpResponseForbidden

def login_view(request):
    ip = request.META.get('REMOTE_ADDR')
    attempts_key = f'login_attempts_{ip}'
    
    attempts = cache.get(attempts_key, 0)
    
    if attempts >= 5:
        return HttpResponseForbidden('Слишком много попыток. Попробуйте через час.')
    
    # Логика авторизации
    if not user_authenticated:
        cache.set(attempts_key, attempts + 1, 3600)  # 1 час
    else:
        cache.delete(attempts_key)
```

### Безопасные настройки для production
```python
# settings.py для production

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (заставляет браузер использовать HTTPS)
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Другие настройки безопасности
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Безопасность cookies
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'
```

---

## 19. Мониторинг и профилирование

### Django Silk (профилирование)
```python
# settings.py
INSTALLED_APPS = [
    ...
    'silk',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    ...
]
```

Доступно на `/silk/` — показывает:
- Все HTTP запросы
- SQL запросы для каждого request
- Время выполнения
- Графики и статистику

### Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'django_warnings.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {  # SQL запросы
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

### Использование в коде
```python
import logging

logger = logging.getLogger(__name__)

def my_view(request):
    logger.info(f'User {request.user} accessed my_view')
    
    try:
        # Код
        pass
    except Exception as e:
        logger.error(f'Error in my_view: {str(e)}', exc_info=True)
```

---

## 20. Тестирование производительности

### Использование django-test-plus
```python
from django.test import TestCase
from django.test.utils import override_settings

class ProductQueryTests(TestCase):
    def setUp(self):
        # Создать тестовые данные
        for i in range(100):
            Product.objects.create(name=f'Product {i}', price=100)
    
    def test_query_count(self):
        """Проверить количество запросов"""
        with self.assertNumQueries(1):  # Ожидаем 1 запрос
            list(Product.objects.all())
    
    def test_prefetch_related(self):
        """Тест prefetch_related"""
        with self.assertNumQueries(2):  # 1 для категорий + 1 для продуктов
            categories = Category.objects.prefetch_related('products')
            for cat in categories:
                list(cat.products.all())
```

### Нагрузочное тестирование с Locust
```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)  # Выполняется в 3 раза чаще
    def view_products(self):
        self.client.get("/products/")
    
    @task(1)
    def view_product_detail(self):
        self.client.get("/products/1/")
    
    @task(2)
    def add_to_cart(self):
        self.client.post("/cart/add/", {"product_id": 1})
```

Запуск: `locust -f locustfile.py`

---

## 21. Чек-лист оптимизации Django проекта

### Database
- [ ] Индексы на часто используемых полях
- [ ] `select_related()` для ForeignKey
- [ ] `prefetch_related()` для ManyToMany
- [ ] `only()` / `defer()` для больших таблиц
- [ ] Bulk операции вместо циклов
- [ ] Пагинация для списков
- [ ] Агрегация на уровне БД, а не Python

### Кеширование
- [ ] Redis/Memcached настроен
- [ ] Кеш для дорогих запросов
- [ ] Template fragment кеш
- [ ] Per-view кеш где возможно
- [ ] Invalidation стратегия (очистка устаревшего кеша)

### Безопасность
- [ ] DEBUG = False в production
- [ ] ALLOWED_HOSTS настроен
- [ ] HTTPS редирект включён
- [ ] Secure cookies (Secure, HttpOnly, SameSite)
- [ ] CSP заголовки
- [ ] Rate limiting для API
- [ ] Регулярные обновления зависимостей

### Статика и медиа
- [ ] Whitenoise или CDN для статики
- [ ] Сжатие изображений
- [ ] Lazy loading изображений
- [ ] Минификация CSS/JS
- [ ] Gzip compression

### Мониторинг
- [ ] Логирование настроено
- [ ] Sentry для отслеживания ошибок
- [ ] Метрики производительности
- [ ] Алерты на критические проблемы

---

## 22. Типичные ошибки и как их избежать

### ❌ Ошибка 1: Запросы в цикле
```python
# Плохо
for product in Product.objects.all():
    print(product.category.name)  # N+1 запросов!

# Хорошо
for product in Product.objects.select_related('category'):
    print(product.category.name)  # 1 запрос
```

### ❌ Ошибка 2: Загрузка всех данных в память
```python
# Плохо
products = Product.objects.all()  # Загружает ВСЁ
for product in products:
    process(product)

# Хорошо
products = Product.objects.all().iterator(chunk_size=100)  # По частям
for product in products:
    process(product)
```

### ❌ Ошибка 3: Неэффективная проверка существования
```python
# Плохо
if Product.objects.filter(sku='ABC123').count() > 0:
    pass

# Хорошо
if Product.objects.filter(sku='ABC123').exists():
    pass
```

### ❌ Ошибка 4: Использование len() вместо count()
```python
# Плохо: загружает все объекты в память
total = len(Product.objects.all())

# Хорошо: SQL COUNT запрос
total = Product.objects.count()
```

### ❌ Ошибка 5: Хранение файлов в БД
```python
# Плохо
class Document(models.Model):
    content = models.BinaryField()  # НЕ хранить файлы в БД!

# Хорошо
class Document(models.Model):
    file = models.FileField(upload_to='documents/')  # Файловая система или S3
```

---

## Заключение

Сегодня мы изучили:
- Работу с cookies и sessions
- Безопасность (CSRF, XSS, CSP)
- Оптимизацию запросов к БД
- Решение проблемы N+1
- Агрегацию и аннотацию
- Сложные запросы с Q и F
- **Кеширование и его уровни**
- **Индексацию БД**
- **Bulk операции**
- **Мониторинг и профилирование**
- **Типичные ошибки**

### Полезные ресурсы
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Packages](https://djangopackages.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) (книга)
- [Django Performance](https://docs.djangoproject.com/en/stable/topics/performance/)
- [Query Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)

**Помните:** Преждевременная оптимизация — корень всех зол. Сначала профилируйте, потом оптимизируйте!

**Практика** — ключ к пониманию этих концепций! 🚀