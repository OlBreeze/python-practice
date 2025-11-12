
# Лекция: Кастомизация в Django

## Введение в кастомизацию

### Почему важна кастомизация?
- Готовые решения Django не покрывают все случаи использования
- Возможность адаптировать фреймворк под специфические требования проекта
- Создание повторно используемых компонентов

## Кастомизация моделей

### Добавление методов к моделям

```python
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def price_after_discount(self):
        return self.price * (1 - self.discount_percent / 100)
```

**Преимущества:**
- Повторное использование логики
- Чистый и читаемый код
- Инкапсуляция бизнес-логики

### Кастомные менеджеры моделей

```python
class ProductQuerySet(models.QuerySet):
    def expensive(self, min_price=100):
        return self.filter(price__gte=min_price)
    
    def discounted(self):
        return self.filter(discount_percent__gt=0)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)
    
    def expensive(self, min_price=100):
        return self.get_queryset().expensive(min_price)

class Product(models.Model):
    # поля модели
    objects = ProductManager()
```

**Использование:**
```python
expensive_products = Product.objects.expensive(150)
discounted_products = Product.objects.discounted()
```

### Кастомные поля

```python
import json
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SimpleJSONField(models.JSONField):
    description = _("Custom JSON field")
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)
    
    def to_python(self, value):
        if value is None or isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except (TypeError, ValueError):
            raise ValidationError(_("Invalid JSON"))
    
    def get_prep_value(self, value):
        if value is None:
            return None
        return json.dumps(value)
```

## Кастомизация форм

### Кастомные валидаторы

```python
from django import forms
from django.core.exceptions import ValidationError

def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('Число должно быть четным')

class NumberForm(forms.Form):
    even_number = forms.IntegerField(validators=[validate_even])
```

### Кастомная валидация нескольких полей

```python
class RegistrationForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise ValidationError('Пароли не совпадают')
        
        return cleaned_data
```

### Кастомные виджеты

```python
class FancyTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})
        kwargs['attrs'].update({'class': 'fancy-input'})
        super().__init__(*args, **kwargs)

class CustomForm(forms.Form):
    name = forms.CharField(widget=FancyTextInput)
```

## Кастомизация админ-панели

### Базовая кастомизация ModelAdmin

```python
from django.contrib import admin

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_percent', 'price_after_discount']
    list_filter = ['discount_percent']
    search_fields = ['name']
    
    actions = ['make_free']
    
    def make_free(self, request, queryset):
        queryset.update(price=0)
    make_free.short_description = "Сделать продукты бесплатными"
```

### Кастомные фильтры

```python
class DiscountFilter(admin.SimpleListFilter):
    title = 'Скидка'
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
```

## Кастомизация шаблонов

### Кастомные теги шаблонов

**Создание структуры:**
```
myapp/
    templatetags/
        __init__.py
        custom_tags.py
```

**Реализация тега:**
```python
from django import template

register = template.Library()

@register.simple_tag
def multiply(x, y):
    return x * y

@register.filter
def currency(value):
    return f"${value:.2f}"
```

**Использование в шаблоне:**
```html
{% load custom_tags %}

{% multiply 3 4 %} {# Результат: 12 #}
{{ product.price|currency }} {# Результат: $35.00 #}
```

### Контекстные процессоры

```python
# context_processors.py
def site_settings(request):
    return {
        'site_name': 'My Shop',
        'support_email': 'support@myshop.com',
        'copyright_year': 2025
    }
```

**Регистрация в settings.py:**
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                # стандартные процессоры
                'myapp.context_processors.site_settings',
            ],
        },
    },
]
```

## Кастомизация представлений

### Миксины для CBV

```python
class ExpensiveMixin:
    price = 100
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(price__gte=self.price)

class ExpensiveProductView(ExpensiveMixin, ListView):
    model = Product
    template_name = 'expensive_list.html'
```

## Middleware

### Кастомный middleware

```python
import time
from django.utils.deprecation import MiddlewareMixin

class TimingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            print(f"Request took {duration:.3f} seconds")
        return response
```

**Регистрация в settings.py:**
```python
MIDDLEWARE = [
    # другой middleware
    'myapp.middleware.TimingMiddleware',
]
```

## Кастомизация пользовательской модели

### Кастомная модель пользователя

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Настройка в settings.py:**
```python
AUTH_USER_MODEL = 'myapp.CustomUser'
```

### Кастомный менеджер пользователей

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
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
```

## Кастомизация форм аутентификации

```python
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
```

## Заключение

### Ключевые моменты:
1. **Гибкость Django** - практически каждый компонент можно кастомизировать
2. **Повторное использование** - создавайте переиспользуемые компоненты
3. **Чистота кода** - кастомизация помогает поддерживать код чистым и организованным
4. **Адаптивность** - возможность адаптировать фреймворк под конкретные нужды проекта

### Что можно кастомизировать:
- Модели (поля, менеджеры, методы)
- Формы (валидаторы, виджеты)
- Админ-панель
- Шаблоны (теги, фильтры)
- Представления (миксины)
- Middleware
- Модель пользователя
- Формы аутентификации

Кастомизация - это мощный инструмент, который делает Django одним из самых гибких и адаптируемых фреймворков для веб-разработки.
