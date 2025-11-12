# Лекция: Кастомизация в Django

## Введение

Django Framework предоставляет множество готовых решений "из коробки", но для специфических задач часто требуется кастомизация различных компонентов. Эта лекция охватывает основные аспекты кастомизации Django-приложений.

---

## 1. Кастомизация моделей

### 1.1 Добавление пользовательских методов

Методы модели используются для повторяющейся логики:

```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    
    def price_after_discount(self):
        """Вычисление цены со скидкой"""
        discounted_price = self.price * (1 - self.discount_percent / 100)
        return f"{discounted_price:.2f}"
    
    def __str__(self):
        return f"{self.name} - {self.price_after_discount()}"
```

**Совет:** Используйте декоратор `@property` для обращения к методу как к атрибуту (без скобок).

#### 📘 Что происходит

Ты видишь модель Django `Product`, которая описывает товар в базе данных:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
```

То есть в таблице будут храниться:

* `name` — имя товара,
* `price` — цена,
* `discount_percent` — процент скидки.

---

#### 🧠 Что делает метод `price_after_discount`

Метод `price_after_discount()` — это **пользовательский метод модели**, который выполняет вычисление:

```python
def price_after_discount(self):
    discounted_price = self.price * (1 - self.discount_percent / 100)
    return f"{discounted_price:.2f}"
```

Он **возвращает цену со скидкой** — например:

* если цена = `100`,
* скидка = `20`,
* то `price_after_discount()` вернёт `"80.00"`.

Метод `price_after_discount()` (или свойство с `@property`) — это **чисто Python-логика**, которая существует **внутри Django-приложения**, а **не в самой базе данных**.

То есть:

* В таблице `product` будут только **поля** (`name`, `price`, `discount_percent`).
* А метод `price_after_discount` — это **вычисляемое свойство**, которое Django выполняет **в памяти** после того, как данные уже получены из базы.

---

#### 🧩 Как использовать

**1️⃣ В Python-коде:**

```python
product = Product.objects.get(id=1)
print(product.price_after_discount())  # вызов метода
```
Результат будет, например:

```
80.00
```

---

#### 💡 Совет про `@property`

Автор рекомендует использовать **декоратор `@property`**, чтобы обращаться к методу **как к обычному атрибуту**, без круглых скобок:

```python
class Product(models.Model):
    ...
    @property
    def price_after_discount(self):
        discounted_price = self.price * (1 - self.discount_percent / 100)
        return f"{discounted_price:.2f}"
```
Теперь можно писать просто:

```python
product = Product.objects.get(id=1)
print(product.price)               # 1000
print(product.discount_percent)    # 10
print(product.price_after_discount)  # 900.00 (вычисляется в Python) # без ()
```
---

#### 🎯 Зачем это нужно

* чтобы **избежать дублирования кода** — не считать скидку вручную в каждом месте;
* чтобы **инкапсулировать бизнес-логику** в самой модели (удобно и читаемо);
* можно использовать и в шаблонах Django:

```django
{{ product.price_after_discount }}
```
---

#### ⚙️ Если нужно хранить результат в БД

Если ты хочешь, чтобы **цена со скидкой реально хранилась в таблице**,
тогда нужно добавить **отдельное поле** и обновлять его, например, в `save()`:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.discounted_price = self.price * (1 - self.discount_percent / 100)
        super().save(*args, **kwargs)
```

Теперь `discounted_price` реально сохранится в базе.

---

### 1.2 Кастомные менеджеры и QuerySet

Менеджеры — это интерфейс для взаимодействия с базой данных.

```python
# Создание кастомного QuerySet
class ProductQuerySet(models.QuerySet):
    def expensive(self, price):
        """Фильтр дорогих товаров"""
        return self.filter(price__gt=price)
    
    def discounted(self):
        """Фильтр товаров со скидкой"""
        return self.filter(discount_percent__gt=0)

# Создание кастомного менеджера
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def expensive(self, price):
        return self.get_queryset().expensive(price)

# Использование в модели
class Product(models.Model):
    # ... поля модели ...
    
    objects = ProductManager()  # Переопределение стандартного менеджера
```

**Использование в представлениях:**

```python
# Получить все дорогие товары
expensive_products = Product.objects.expensive(100)
```

---

### 1.3 Кастомные поля модели

Создание специальных полей для хранения данных нестандартного формата:  

В Django у моделей есть стандартные поля:
CharField, IntegerField, DateTimeField, JSONField, и т.д.

Но иногда нужно хранить нестандартные данные,
например — Python-словарь, список, координаты, массив и т.п.

В таких случаях можно создать своё поле, унаследовав его от одного из базовых полей (в примере — models.TextField)
и добавить собственную логику преобразования данных между Python и базой данных.

```python
import json
from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError

class SimpleJSONField(models.TextField):
    description = "JSON field"
    
    def from_db_value(self, value, expression, connection): # Вызывается, когда Django достаёт значение из базы данных.
        # Если там хранится строка "{\"a\": 1}", она превращается в словарь {"a": 1}.
        if value is None:
            return value
        return json.loads(value)
    
    def to_python(self, value):
        """
         Преобразует значение в Python-объект,
                например при валидации формы или перед сохранением.

                Если значение уже словарь — возвращает как есть.
                Если это строка — пытается распарсить json.loads.
                Если формат некорректный — вызывает ValidationError.
        """
        if value is None or isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            raise ValidationError("Invalid JSON")
    
    def get_prep_value(self, value): # Перед сохранением в базу — делает обратное:
                            # превращает Python-объект (словарь) обратно в строку JSON.
        if value is None:
            return None
        return json.dumps(value)
```
 #### 🧩Что делает этот пример  
```python
class SimpleJSONField(models.TextField):
    description = "JSON field"
```
Это собственное поле, которое **хранит данные в виде текста в базе**,
но в **Python выглядит как словарь (dict)**.


#### 🧠 Пример использования:

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    data = SimpleJSONField()
```

Теперь можно:

```python
p = Product(name="Phone", data={"color": "black", "weight": 150})
p.save()  # в базе сохранится текст '{"color": "black", "weight": 150}'

# а при чтении из базы Django вернёт словарь:
p = Product.objects.get(name="Phone")
print(p.data["color"])  # black
```

---

#### ⚠️ Важно знать

* Django уже имеет **встроенное поле `JSONField`** (начиная с версии 3.1+),
  которое делает **всё то же самое**, но безопаснее и оптимальнее.
* Такой код нужен только если ты работаешь со **старыми версиями Django**
  или хочешь **особое поведение**, например —
  автоматическую валидацию структуры JSON, хранение только части данных и т.д.

---

## 2. Кастомизация форм

### 2.1 Кастомные валидаторы

```python
from django.core.exceptions import ValidationError

def validate_even(value):
    """Валидатор для проверки четных чисел"""
    if value % 2 != 0:
        raise ValidationError(f'{value} не является четным числом')

# Использование в форме
from django import forms

class NumberForm(forms.Form):
    even_number = forms.IntegerField(validators=[validate_even])
```

### 2.2 Переопределение метода clean()

```python
class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        
        return cleaned_data
```

### 2.3 Кастомные виджеты

```python
from django.forms import widgets

class FancyTextInput(widgets.TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'fancy-input form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

# Использование
class MyForm(forms.Form):
    name = forms.CharField(widget=FancyTextInput())
```

---

## 3. Кастомизация Admin-панели

### 🧩3.1 Регистрация моделей

```python
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percent', 'price_after_discount']
    list_filter = ['discount_percent']
    search_fields = ['name']
```
#### 🔍 Что делает этот код:

* **`@admin.register(Product)`** — регистрирует модель `Product` в админке.
  (То же самое, что `admin.site.register(Product, ProductAdmin)`.)
* **`class ProductAdmin(admin.ModelAdmin)`** — создаёт *настройки отображения* для этой модели в админке.

#### 🖥️ Что увидишь в админке:

| name  | price | discount_percent | price_after_discount |
| ----- | ----- | ---------------- | -------------------- |
| Phone | 1000  | 10               | 900                  |

* `list_display` — какие колонки показывать в списке товаров.
  Ты можешь даже добавить туда **методы модели**, например `price_after_discount()`.
* `list_filter` — фильтр справа, чтобы можно было отфильтровать по скидке.
* `search_fields` — строка поиска по имени.

👉 Таким образом, админка превращается из "сырой таблицы" в удобную панель управления.

### ⚙️3.2 Кастомные действия (actions)

```python
class ProductAdmin(admin.ModelAdmin):
    actions = ['make_free']
    
    def make_free(self, request, queryset):
        """Установить цену = 0"""
        queryset.update(price=0)
    
    make_free.short_description = "Сделать товары бесплатными"
```
#### 🔍 Что происходит:

* `actions` — список действий, которые можно выбрать и применить к выделенным записям в админке.
* `make_free` — это твоё собственное действие.

#### 🖱️ Как работает:

1. В админке ты выделяешь несколько товаров галочками.
2. В выпадающем списке выбираешь **“Сделать товары бесплатными”**.
3. Django вызывает метод `make_free`, который:

   ```python
   queryset.update(price=0)
   ```

   — устанавливает цену `0` для всех выбранных товаров.

💡 Такие кастомные actions часто используют для массового изменения полей, подтверждения заказов, активации пользователей и т.п.

### 🔗3.3 Inline модели

```python
class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]
```
#### 🔍 Что это:

"Инлайны" позволяют **редактировать связанные объекты прямо внутри другой модели**.

#### 🧠 Пример:

Если у тебя есть `Category` → `Product` (связь `ForeignKey`),
то в админке, открыв категорию, ты увидишь таблицу товаров этой категории прямо на странице категории.

📊 Пример в админке:

**Category: Смартфоны**

| name    | price | discount |
| ------- | ----- | -------- |
| iPhone  | 1000  | 10%      |
| Samsung | 800   | 5%       |

(это и есть `TabularInline` — табличная форма, `extra=1` означает "показать одну пустую строку для добавления нового продукта").

### 🎯3.4 Кастомные фильтры

```python
from django.contrib.admin import SimpleListFilter

class DiscountFilter(SimpleListFilter):
    title = 'скидка'
    parameter_name = 'discount'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Со скидкой'),
            ('no', 'Без скидки'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(discount_percent__gt=0)
        if self.value() == 'no':
            return queryset.filter(discount_percent=0)
        return queryset

class ProductAdmin(admin.ModelAdmin):
    list_filter = [DiscountFilter]
```
#### 🔍 Что делает:

Это — **пользовательский фильтр** (в правой панели админки).

Теперь можно выбирать:

* **Со скидкой** → покажет все товары, где `discount_percent > 0`.
* **Без скидки** → покажет, где `discount_percent = 0`.

---

### 🧭 В итоге

| Возможность        | Что делает                               |
| ------------------ | ---------------------------------------- |
| `@admin.register`  | Регистрирует модель в админке            |
| `list_display`     | Показывает нужные колонки                |
| `list_filter`      | Добавляет фильтры справа                 |
| `search_fields`    | Включает поиск                           |
| `actions`          | Добавляет кнопки массовых действий       |
| `Inline`           | Позволяет редактировать связанные модели |
| `SimpleListFilter` | Создаёт кастомный фильтр                 |

---

## 4. Кастомизация шаблонов

### 4.1 Кастомные теги

Создайте структуру: `app_name/templatetags/custom_extras.py`

```python
from django import template

register = template.Library()

@register.simple_tag
def multiply(a, b):
    """Умножение двух чисел"""
    return a * b
```

**Использование в шаблоне:**

```django
{% load custom_extras %}
{% multiply 3 4 %}  {# Выведет: 12 #}
```

### 4.2 Кастомные фильтры

```python
@register.filter
def currency(value):
    """Форматирование в валюту"""
    return f"${value:.2f}"
```

**Использование:**

```django
{{ product.price|currency }}  {# Выведет: $19.99 #}
```

### 4.3 Контекстные процессоры

Создайте файл `context_processors.py`:

```python
def site_settings(request):
    """Добавление переменных во все шаблоны"""
    return {
        'site_name': 'My Shop',
        'support_email': 'support@example.com',
        'current_year': 2025
    }
```

#### Регистрация в settings.py:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... другие процессоры ...
                'myapp.context_processors.site_settings',
            ],
        },
    },
]
```

#### Использование в шаблоне:

```django
<footer>
    {{ site_name }} © {{ current_year }}
    Контакты: {{ support_email }}
</footer>
```

---

## 5. Кастомизация представлений (Views)

### 5.1 Миксины (Mixins)

```python
from django.views.generic import ListView

class ExpensiveMixin:
    """Миксин для фильтрации дорогих товаров"""
    max_price = 100
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(price__gte=self.max_price)

class ExpensiveProductView(ExpensiveMixin, ListView):
    model = Product
    template_name = 'expensive_list.html'
```

---

## 6. Middleware (Промежуточное ПО)

### 6.1 Создание кастомного middleware

Создайте файл `middleware.py`:

```python
import time

class RequestTimingMiddleware:
    """Измерение времени обработки запроса"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Код выполняется перед обработкой запроса
        request.start_time = time.time()
        
        response = self.get_response(request)
        
        # Код выполняется после обработки запроса
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            print(f"Request to {request.path} took {duration:.3f} seconds")
        
        return response
```

**Регистрация в settings.py:**

```python
MIDDLEWARE = [
    # ... другие middleware ...
    'myapp.middleware.RequestTimingMiddleware',
]
```

---

## 7. Кастомизация модели пользователя

### 7.1 Создание кастомной модели User

```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Расширенная модель пользователя"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    # Указываем поле для входа
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Регистрация в settings.py:**

```python
AUTH_USER_MODEL = 'myapp.CustomUser'
```

### 7.2 Кастомный менеджер пользователей

```python
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Использование в модели
class CustomUser(AbstractUser):
    # ... поля ...
    objects = CustomUserManager()
```

---

## Практические задания

1. **Создать кастомный фильтр** для шаблонов (например, форматирование даты)
2. **Создать кастомный тег** для шаблонов (например, вывод текущего времени)
3. **Создать контекстный процессор** (например, информация о сайте)
4. **Применить все три** в одном шаблоне

---

## Ключевые выводы

✅ **Django очень гибкий** — можно кастомизировать практически все компоненты

✅ **Используйте готовые решения** — начинайте с базовых возможностей Django

✅ **Кастомизируйте при необходимости** — не переусложняйте без реальной потребности

✅ **Следуйте принципу DRY** — выносите повторяющуюся логику в методы, миксины и менеджеры

✅ **Документируйте код** — кастомные решения должны быть понятны другим разработчикам

---

## Полезные ссылки

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Custom Template Tags](https://docs.djangoproject.com/en/stable/howto/custom-template-tags/)
- [Django Custom Model Fields](https://docs.djangoproject.com/en/stable/howto/custom-model-fields/)
- [Django Middleware](https://docs.djangoproject.com/en/stable/topics/http/middleware/)