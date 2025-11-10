# Лекция: Формы в Django

## 1. Введение в формы Django

### 1.1 Что такое формы?

**Формы в Django** — это мощный инструмент для взаимодействия пользователя с веб-приложением.

```
┌─────────────┐
│ Пользователь│
└──────┬──────┘
       │ Ввод данных
       ↓
┌─────────────┐
│   Форма     │
│  (валидация)│
└──────┬──────┘
       │ Чистые данные
       ↓
┌─────────────┐
│ База данных │
└─────────────┘
```

### 1.2 Роль форм в веб-приложениях

**Формы выполняют функции посредника:**
- 🔄 Сбор данных от пользователя
- ✅ Валидация введённых данных
- 💾 Сохранение в базу данных
- 🛡️ Защита от атак (XSS, CSRF)

### 1.3 Зачем использовать формы Django?

#### Упрощение создания интерфейсов

```python
# ❌ Без форм Django (вручную)
<input type="text" name="username" required>
<input type="email" name="email" required>
# Валидация на стороне клиента и сервера

# ✅ С формами Django
{{ form.as_p }}
# Автоматическая генерация полей + валидация
```

#### Валидация данных

```python
# Автоматическая проверка:
- Обязательные поля (required)
- Корректность email
- Длина строки (max_length)
- Числовые диапазоны
- Пользовательские правила
```

#### Безопасность

```python
# Встроенная защита от:
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- SQL Injection
```

---

## 2. Основы работы с формами

### 2.1 Два подхода к созданию форм

Django предоставляет два основных подхода:

| Подход | Использование | Гибкость | Код |
|--------|---------------|----------|-----|
| `forms.Form` | Ручное создание | ✅ Высокая | Больше кода |
| `forms.ModelForm` | На основе модели | ⚡ Быстрая разработка | Меньше кода |

### 2.2 Создание файла forms.py

```python
# myapp/forms.py
from django import forms
from .models import Product

# Теперь готовы создавать формы!
```

---

## 3. Использование forms.Form

### 3.1 Базовый пример

```python
# myapp/forms.py
from django import forms


class ContactForm(forms.Form):
    """Форма обратной связи"""
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        required=True
    )
    email = forms.EmailField(
        label='Электронная почта',
        required=True
    )
    message = forms.CharField(
        widget=forms.Textarea,
        label='Сообщение',
        required=True
    )
```

### 3.2 Типы полей форм

```python
from django import forms


class ExampleForm(forms.Form):
    # Текстовые поля
    username = forms.CharField(max_length=50)
    
    # Email
    email = forms.EmailField()
    
    # Числа
    age = forms.IntegerField(min_value=18, max_value=120)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    
    # Дата и время
    birth_date = forms.DateField()
    appointment = forms.DateTimeField()
    
    # Логические
    agree = forms.BooleanField(required=True)
    
    # Выбор из списка
    CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java')
    ]
    language = forms.ChoiceField(choices=CHOICES)
    
    # Множественный выбор
    interests = forms.MultipleChoiceField(choices=CHOICES)
    
    # Файлы
    document = forms.FileField()
    photo = forms.ImageField()  # Требует Pillow
    
    # URL
    website = forms.URLField()
    
    # Пароль
    password = forms.CharField(widget=forms.PasswordInput())
```

### 3.3 Параметры полей

```python
class ProductForm(forms.Form):
    name = forms.CharField(
        label="Название товара",       # Метка поля
        max_length=100,                 # Максимальная длина
        required=True,                  # Обязательное поле (по умолчанию)
        help_text="Введите название",   # Подсказка
        initial="Новый товар",          # Начальное значение
        disabled=False,                 # Заблокировано/нет
        widget=forms.TextInput(attrs={  # Настройка виджета
            'class': 'form-control',
            'placeholder': 'Название'
        })
    )
    
    price = forms.DecimalField(
        label="Цена",
        max_digits=10,
        decimal_places=2,
        min_value=0,                    # Минимальное значение
        max_value=999999.99,            # Максимальное значение
        required=True
    )
    
    description = forms.CharField(
        label="Описание",
        required=False,                  # Необязательное поле
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 50
        })
    )
```

---

## 4. Использование forms.ModelForm

### 4.1 Автоматическое создание формы

**ModelForm** автоматически создаёт форму на основе модели.

```python
# myapp/models.py
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    in_stock = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
```

```python
# myapp/forms.py
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Форма на основе модели Product"""
    
    class Meta:
        model = Product
        fields = '__all__'  # Все поля модели
        # или
        # fields = ['name', 'price', 'description']  # Конкретные поля
        # или
        # exclude = ['in_stock']  # Исключить поля
```

### 4.2 Настройка Meta класса

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
        
        # Пользовательские метки
        labels = {
            'name': 'Название товара',
            'price': 'Цена (руб.)',
            'description': 'Описание товара'
        }
        
        # Подсказки
        help_texts = {
            'name': 'Введите название товара',
            'price': 'Цена в рублях'
        }
        
        # Сообщения об ошибках
        error_messages = {
            'name': {
                'required': 'Название обязательно для заполнения',
                'max_length': 'Название слишком длинное'
            }
        }
        
        # Виджеты
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            })
        }
```

### 4.3 Переопределение полей

```python
class ProductForm(forms.ModelForm):
    # Переопределение поля модели
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название'
        })
    )
    
    # Добавление нового поля (не из модели)
    confirm_price = forms.DecimalField(
        label="Подтверждение цены",
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
    
    def clean(self):
        """Валидация всей формы"""
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        confirm_price = cleaned_data.get('confirm_price')
        
        if price and confirm_price:
            if price != confirm_price:
                raise forms.ValidationError(
                    "Цены не совпадают!"
                )
        
        return cleaned_data
```

---

## 5. Валидация данных

### 5.1 Встроенная валидация

```python
class UserForm(forms.Form):
    username = forms.CharField(
        min_length=3,           # Минимум 3 символа
        max_length=20,          # Максимум 20 символов
        required=True           # Обязательное поле
    )
    
    email = forms.EmailField()  # Автоматическая проверка email
    
    age = forms.IntegerField(
        min_value=18,           # Минимум 18
        max_value=120           # Максимум 120
    )
```

### 5.2 Валидация отдельного поля (clean_<field>)

```python
class ContactForm(forms.Form):
    email = forms.EmailField()
    
    def clean_email(self):
        """Валидация поля email"""
        email = self.cleaned_data['email']
        
        # Проверка домена
        if not email.endswith('@example.com'):
            raise forms.ValidationError(
                'Используйте email с доменом @example.com'
            )
        
        return email
```

```python
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    
    def clean_username(self):
        """Проверка уникальности username"""
        username = self.cleaned_data['username']
        
        # Проверка существования в БД
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        
        # Запрет спецсимволов
        if not username.isalnum():
            raise forms.ValidationError(
                'Имя пользователя может содержать только буквы и цифры'
            )
        
        return username
```

### 5.3 Валидация всей формы (clean)

```python
class RegistrationForm(forms.Form):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput()
    )
    
    def clean(self):
        """Валидация нескольких полей"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    'Пароли не совпадают!'
                )
            
            # Проверка сложности пароля
            if len(password1) < 8:
                raise forms.ValidationError(
                    'Пароль должен содержать минимум 8 символов'
                )
        
        return cleaned_data
```

### 5.4 Пользовательские валидаторы

```python
from django.core.exceptions import ValidationError


def validate_even(value):
    """Валидатор для проверки чётности"""
    if value % 2 != 0:
        raise ValidationError(
            f'{value} не является чётным числом'
        )


def validate_phone(value):
    """Валидатор номера телефона"""
    import re
    pattern = r'^\+?\d{10,15}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Введите корректный номер телефона'
        )


class NumberForm(forms.Form):
    number = forms.IntegerField(
        validators=[validate_even]  # Применение валидатора
    )
    
    phone = forms.CharField(
        max_length=15,
        validators=[validate_phone]
    )
```

---

## 6. Обработка форм в views

### 6.1 Базовая обработка (Function-Based View)

```python
# myapp/views.py
from django.shortcuts import render, redirect
from .forms import ContactForm


def contact_view(request):
    """Обработка формы обратной связи"""
    
    if request.method == "POST":
        # Форма отправлена
        form = ContactForm(request.POST)
        
        if form.is_valid():
            # Данные валидны
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Обработка данных (отправка email, сохранение и т.д.)
            print(f"Получено сообщение от {name} ({email}): {message}")
            
            # Редирект после успешной отправки
            return redirect('success_page')
    else:
        # GET запрос - показать пустую форму
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
```

### 6.2 Обработка ModelForm

```python
from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product


def product_create(request):
    """Создание нового товара"""
    
    if request.method == "POST":
        form = ProductForm(request.POST)
        
        if form.is_valid():
            # Автоматическое сохранение в БД
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form})


def product_edit(request, pk):
    """Редактирование товара"""
    product = Product.objects.get(pk=pk)
    
    if request.method == "POST":
        # Привязка формы к существующему объекту
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {'form': form})
```

### 6.3 Обработка forms.Form с сохранением в БД

```python
from .forms import SimpleForm
from .models import Product


def simple_view(request):
    """Обработка обычной формы с сохранением в БД"""
    
    if request.method == "POST":
        form = SimpleForm(request.POST)
        
        if form.is_valid():
            # Ручное извлечение данных
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            
            # Создание объекта модели
            Product.objects.create(
                name=name,
                # ... другие поля
            )
            
            return redirect('success')
    else:
        form = SimpleForm()
    
    return render(request, 'simple_form.html', {'form': form})
```

### 6.4 Class-Based View (CBV)

```python
from django.views.generic import CreateView, UpdateView
from .models import Product
from .forms import ProductForm


class ProductCreateView(CreateView):
    """Создание товара через CBV"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = '/products/'


class ProductUpdateView(UpdateView):
    """Редактирование товара через CBV"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = '/products/'
```

---

## 7. Отображение форм в шаблонах

### 7.1 Простое отображение

```html
<!-- templates/contact.html -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Отправить</button>
</form>
```

**Методы отображения:**

```html
<!-- Как параграфы (<p>) -->
{{ form.as_p }}

<!-- Как таблица (<table>) -->
{{ form.as_table }}

<!-- Как список (<ul>) -->
{{ form.as_ul }}
```

### 7.2 Ручное отображение полей

```html
<form method="post">
    {% csrf_token %}
    
    <!-- Перебор всех полей -->
    {% for field in form %}
        <div class="form-group">
            {{ field.label_tag }}
            {{ field }}
            
            {% if field.help_text %}
                <small>{{ field.help_text }}</small>
            {% endif %}
            
            {% if field.errors %}
                <div class="error">
                    {{ field.errors }}
                </div>
            {% endif %}
        </div>
    {% endfor %}
    
    <button type="submit">Отправить</button>
</form>
```

### 7.3 Полный контроль над отображением

```html
<form method="post" class="needs-validation">
    {% csrf_token %}
    
    <!-- Конкретное поле -->
    <div class="mb-3">
        <label for="{{ form.name.id_for_label }}" class="form-label">
            {{ form.name.label }}
        </label>
        <input 
            type="text" 
            name="{{ form.name.name }}" 
            class="form-control {% if form.name.errors %}is-invalid{% endif %}"
            id="{{ form.name.id_for_label }}"
            value="{{ form.name.value|default:'' }}"
        >
        {% if form.name.errors %}
            <div class="invalid-feedback">
                {{ form.name.errors.0 }}
            </div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">Отправить</button>
</form>
```

### 7.4 Bootstrap стилизация

```html
<!-- templates/product_form.html -->
{% load crispy_forms_tags %}  <!-- Если используете django-crispy-forms -->

<div class="container mt-5">
    <h2>Добавить товар</h2>
    
    <form method="post" class="needs-validation" novalidate>
        {% csrf_token %}
        
        <div class="mb-3">
            <label for="{{ form.name.id_for_label }}" class="form-label">
                {{ form.name.label }}
            </label>
            {{ form.name|add_class:"form-control" }}
            {% if form.name.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.name.errors.0 }}
                </div>
            {% endif %}
        </div>
        
        <div class="mb-3">
            <label for="{{ form.price.id_for_label }}" class="form-label">
                {{ form.price.label }}
            </label>
            {{ form.price|add_class:"form-control" }}
        </div>
        
        <button type="submit" class="btn btn-primary">Сохранить</button>
        <a href="{% url 'product_list' %}" class="btn btn-secondary">Отмена</a>
    </form>
</div>
```

---

## 8. Виджеты (Widgets)

### 8.1 Что такое виджеты?

**Widget** — это представление HTML-элемента формы.

```python
# Пример: одно поле, разные виджеты
password = forms.CharField(widget=forms.PasswordInput())  # <input type="password">
comment = forms.CharField(widget=forms.Textarea())         # <textarea>
```

### 8.2 Встроенные виджеты

```python
from django import forms


class ExampleForm(forms.Form):
    # Текстовое поле
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя'
        })
    )
    
    # Textarea
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 50
        })
    )
    
    # Пароль
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    
    # Email
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Дата
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # Checkbox
    agree = forms.BooleanField(
        widget=forms.CheckboxInput()
    )
    
    # Radio buttons
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect()
    )
    
    # Select dropdown
    country = forms.ChoiceField(
        choices=[('ru', 'Россия'), ('ua', 'Украина')],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    # Скрытое поле
    user_id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
```

### 8.3 Пользовательский виджет

```python
from django.forms.widgets import Widget
from django.utils.safestring import mark_safe


class CustomTextarea(Widget):
    """Кастомный виджет textarea"""
    
    def render(self, name, value, attrs=None, renderer=None):
        """Отрисовка виджета"""
        if value is None:
            value = ''
        
        html = f'''
            <textarea 
                name="{name}" 
                style="border: 2px solid blue; border-radius: 5px;"
                rows="5"
            >{value}</textarea>
        '''
        return mark_safe(html)


class CustomForm(forms.Form):
    message = forms.CharField(widget=CustomTextarea())
```

---

## 9. Расширенные возможности

### 9.1 FileField и ImageField

```python
# myapp/models.py
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
```

```python
# myapp/forms.py
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
```

```python
# myapp/views.py
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)  # ⚠️ request.FILES!
        
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentForm()
    
    return render(request, 'upload.html', {'form': form})
```

```html
<!-- templates/upload.html -->
<form method="post" enctype="multipart/form-data">  <!-- ⚠️ enctype! -->
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Загрузить</button>
</form>
```

**Настройка в settings.py:**

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Установка Pillow (для ImageField):**

```bash
pip install Pillow
```

### 9.2 Inline Formsets

**Inline Formsets** позволяют редактировать связанные модели вместе.

```python
# myapp/models.py
class Order(models.Model):
    customer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
```

```python
# myapp/forms.py
from django.forms import inlineformset_factory


# Создание inline formset
OrderItemFormSet = inlineformset_factory(
    Order,              # Родительская модель
    OrderItem,          # Дочерняя модель
    fields=['product', 'quantity'],  # Поля для редактирования
    extra=1,            # Количество пустых форм
    can_delete=True     # Возможность удаления
)
```

```python
# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderItemFormSet


def order_detail(request, order_id):
    """Редактирование заказа с элементами"""
    order = get_object_or_404(Order, pk=order_id)
    
    if request.method == 'POST':
        formset = OrderItemFormSet(request.POST, instance=order)
        
        if formset.is_valid():
            formset.save()
            return redirect('order_detail', order_id=order_id)
    else:
        formset = OrderItemFormSet(instance=order)
    
    return render(request, 'order_detail.html', {
        'formset': formset,
        'order': order
    })
```

```html
<!-- templates/order_detail.html -->
<h2>Заказ #{{ order.id }}</h2>

<form method="post">
    {% csrf_token %}
    {{ formset.management_form }}  <!-- ⚠️ Обязательно! -->
    
    <table>
        <thead>
            <tr>
                <th>Товар</th>
                <th>Количество</th>
                <th>Удалить</th>
            </tr>
        </thead>
        <tbody>
            {% for form in formset %}
                <tr>
                    <td>{{ form.product }}</td>
                    <td>{{ form.quantity }}</td>
                    <td>{{ form.DELETE }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <button type="submit">Сохранить</button>
</form>
```

### 9.3 Formsets (множественные формы)

```python
from django.forms import formset_factory


# Создание formset
ProductFormSet = formset_factory(
    ProductForm,
    extra=3,            # Количество форм
    max_num=10,         # Максимум форм
    validate_max=True   # Валидация максимума
)
```

```python
def bulk_add_products(request):
    """Добавление нескольких товаров"""
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    Product.objects.create(**form.cleaned_data)
            
            return redirect('product_list')
    else:
        formset = ProductFormSet()
    
    return render(request, 'bulk_add.html', {'formset': formset})
```

---

## 10. Практические примеры

### 10.1 Форма регистрации

```python
# myapp/forms.py
from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Пользователь с таким именем уже существует'
            )
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Пользователь с таким email уже зарегистрирован'
            )
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Пароли не совпадают')
        
        return cleaned_data
```

```python
# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegistrationForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            # Создание пользователя
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            
            return redirect('login')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})
```

### 10.2 Форма поиска

```python
class SearchForm(forms.Form):
    """Форма поиска товаров"""
    query = forms.CharField(
        label='',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск товаров...'
        })
    )
    
    CATEGORY_CHOICES = [
        ('', 'Все категории'),
        ('electronics', 'Электроника'),
        ('clothing', 'Одежда'),
        ('books', 'Книги')
    ]
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    min_price = forms.DecimalField(
        label='Цена от',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '0'
        })
    )
    
    max_price = forms.DecimalField(
        label='до',
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '10000'
        })
    )
```

```python
def search_products(request):
    """Поиск товаров с фильтрами"""
    form = SearchForm(request.GET or None)
    products = Product.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if query:
            products = products.filter(name__icontains=query)
        
        if category:
            products = products.filter(category=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
    
    return render(request, 'search.html', {
        'form': form,
        'products': products
    })
```

### 10.3 Форма с динамическими полями

```python
class DynamicForm(forms.Form):
    """Форма с динамическим выбором"""
    
    def __init__(self, *args, **kwargs):
        # Получение списка категорий из БД
        categories = kwargs.pop('categories', None)
        super().__init__(*args, **kwargs)
        
        if categories:
            self.fields['category'] = forms.ChoiceField(
                choices=[(c.id, c.name) for c in categories]
            )
```

```python
def dynamic_form_view(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = DynamicForm(request.POST, categories=categories)
        if form.is_valid():
            # Обработка
            pass
    else:
        form = DynamicForm(categories=categories)
    
    return render(request, 'dynamic.html', {'form': form})
```

---

## 11. Сравнение Form vs ModelForm

### 11.1 Когда использовать Form?

✅ **Используйте Form когда:**
- Форма не связана с моделью
- Нужна полная кастомизация
- Обработка данных без сохранения в БД
- Сложная логика валидации

**Примеры:**
- Форма обратной связи
- Форма поиска
- Форма входа (логин)
- Калькуляторы

```python
class ContactForm(forms.Form):
    """Не сохраняется в БД"""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

### 11.2 Когда использовать ModelForm?

✅ **Используйте ModelForm когда:**
- Форма связана с моделью
- Нужно быстро создать CRUD
- Автоматическая валидация
- Простое сохранение в БД

**Примеры:**
- Создание/редактирование товаров
- Регистрация пользователей
- Управление профилем
- Админ-панели

```python
class ProductForm(forms.ModelForm):
    """Автоматическое создание на основе модели"""
    class Meta:
        model = Product
        fields = '__all__'
```

### 11.3 Сравнительная таблица

| Критерий | Form | ModelForm |
|----------|------|-----------|
| **Создание** | Вручную описываем поля | Автоматически из модели |
| **Сохранение** | Вручную в БД | `form.save()` |
| **Код** | Больше кода | Меньше кода |
| **Гибкость** | ✅ Максимальная | ⚡ Ограничена моделью |
| **Валидация** | Полностью кастомная | Из модели + кастомная |
| **Использование** | Любые задачи | CRUD операции |

---

## 12. Оптимизация производительности

### 12.1 Проблемы с большими формами

```python
# ❌ Плохо: N+1 запросов
class LargeForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all()  # Все авторы!
    )

# ✅ Хорошо: оптимизация запросов
class OptimizedForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.select_related('publisher').all()
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ограничение выборки
        self.fields['author'].queryset = Author.objects.filter(
            is_active=True
        )[:100]  # Только первые 100
```

### 12.2 Кеширование choices

```python
from django.core.cache import cache


class CachedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Кеширование списка категорий
        categories = cache.get('categories_list')
        if not categories:
            categories = list(
                Category.objects.values_list('id', 'name')
            )
            cache.set('categories_list', categories, 3600)  # 1 час
        
        self.fields['category'] = forms.ChoiceField(
            choices=categories
        )
```

### 12.3 Ajax валидация

```html
<script>
// Валидация на стороне клиента для уменьшения запросов к серверу
document.getElementById('email').addEventListener('blur', function() {
    const email = this.value;
    
    fetch('/api/check-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({email: email})
    })
    .then(response => response.json())
    .then(data => {
        if (data.exists) {
            showError('Email уже зарегистрирован');
        }
    });
});
</script>
```

---

## 13. Альтернативы встроенным виджетам

### 13.1 Django Crispy Forms

**Установка:**
```bash
pip install django-crispy-forms crispy-bootstrap5
```

**Настройка:**
```python
# settings.py
INSTALLED_APPS = [
    ...
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

**Использование:**
```html
{% load crispy_forms_tags %}

<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">Отправить</button>
</form>
```

**Расширенное использование:**
```python
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class StyledForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Submit('submit', 'Отправить', css_class='btn btn-primary')
        )
```

### 13.2 Django Widget Tweaks

**Установка:**
```bash
pip install django-widget-tweaks
```

**Использование:**
```html
{% load widget_tweaks %}

<form method="post">
    {% csrf_token %}
    
    <div class="mb-3">
        <label>{{ form.name.label }}</label>
        {% render_field form.name class="form-control" placeholder="Имя" %}
    </div>
    
    <div class="mb-3">
        <label>{{ form.email.label }}</label>
        {% render_field form.email class="form-control" type="email" %}
    </div>
    
    <button type="submit">Отправить</button>
</form>
```

### 13.3 Select2 (продвинутый select)

```html
<!-- Подключение Select2 -->
<link href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>

<script>
$(document).ready(function() {
    $('#id_category').select2({
        placeholder: 'Выберите категорию',
        allowClear: true
    });
});
</script>
```

---

## 14. Сложные формы с динамическими изменениями

### 14.1 Зависимые dropdown списки

```python
# myapp/models.py
class Country(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
```

```python
# myapp/views.py
from django.http import JsonResponse


def load_cities(request):
    """API для загрузки городов по стране"""
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)
```

```html
<form method="post">
    {% csrf_token %}
    
    <select name="country" id="country">
        <option value="">Выберите страну</option>
        {% for country in countries %}
            <option value="{{ country.id }}">{{ country.name }}</option>
        {% endfor %}
    </select>
    
    <select name="city" id="city">
        <option value="">Сначала выберите страну</option>
    </select>
    
    <button type="submit">Отправить</button>
</form>

<script>
document.getElementById('country').addEventListener('change', function() {
    const countryId = this.value;
    const citySelect = document.getElementById('city');
    
    // Очистка списка городов
    citySelect.innerHTML = '<option value="">Загрузка...</option>';
    
    // Загрузка городов
    fetch(`/api/cities/?country_id=${countryId}`)
        .then(response => response.json())
        .then(cities => {
            citySelect.innerHTML = '<option value="">Выберите город</option>';
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.id;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        });
});
</script>
```

### 14.2 Условное отображение полей

```python
class ConditionalForm(forms.Form):
    delivery_method = forms.ChoiceField(
        choices=[
            ('pickup', 'Самовывоз'),
            ('delivery', 'Доставка')
        ]
    )
    
    # Поля для доставки
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        
        if delivery_method == 'delivery':
            if not cleaned_data.get('address'):
                self.add_error('address', 'Укажите адрес доставки')
            if not cleaned_data.get('city'):
                self.add_error('city', 'Укажите город')
        
        return cleaned_data
```

```html
<form method="post">
    {% csrf_token %}
    
    <div class="mb-3">
        {{ form.delivery_method.label_tag }}
        {{ form.delivery_method }}
    </div>
    
    <div id="delivery-fields" style="display: none;">
        <div class="mb-3">
            {{ form.address.label_tag }}
            {{ form.address }}
        </div>
        <div class="mb-3">
            {{ form.city.label_tag }}
            {{ form.city }}
        </div>
    </div>
    
    <button type="submit">Отправить</button>
</form>

<script>
document.querySelector('[name="delivery_method"]').addEventListener('change', function() {
    const deliveryFields = document.getElementById('delivery-fields');
    deliveryFields.style.display = this.value === 'delivery' ? 'block' : 'none';
});
</script>
```

---

## 15. Безопасность форм

### 15.1 CSRF защита

**CSRF токен обязателен:**
```html
<form method="post">
    {% csrf_token %}  <!-- ⚠️ Обязательно! -->
    {{ form.as_p }}
    <button type="submit">Отправить</button>
</form>
```

**AJAX запросы:**
```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify(data)
});
```

### 15.2 XSS защита

```python
from django.utils.html import escape


class SafeForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    
    def clean_comment(self):
        """Экранирование HTML"""
        comment = self.cleaned_data['comment']
        # Django автоматически экранирует в шаблонах
        # Но для API нужно вручную
        return escape(comment)
```

### 15.3 Ограничение размера загружаемых файлов

```python
from django.core.validators import FileExtensionValidator


class FileUploadForm(forms.Form):
    document = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx']
            )
        ]
    )
    
    def clean_document(self):
        """Проверка размера файла"""
        file = self.cleaned_data['document']
        
        # Максимум 5MB
        max_size = 5 * 1024 * 1024
        if file.size > max_size:
            raise forms.ValidationError(
                f'Размер файла не должен превышать 5MB'
            )
        
        return file
```

```python
# settings.py
# Ограничение размера загружаемых файлов
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

---

## 16. Тестирование форм

### 16.1 Базовые тесты

```python
# myapp/tests.py
from django.test import TestCase
from .forms import ContactForm


class ContactFormTest(TestCase):
    def test_valid_form(self):
        """Тест валидной формы"""
        data = {
            'name': 'Иван',
            'email': 'ivan@example.com',
            'message': 'Тестовое сообщение'
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email(self):
        """Тест невалидного email"""
        data = {
            'name': 'Иван',
            'email': 'invalid-email',
            'message': 'Сообщение'
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_required_fields(self):
        """Тест обязательных полей"""
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
```

### 16.2 Тестирование view с формой

```python
from django.test import TestCase, Client
from django.urls import reverse


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
    
    def test_get_request(self):
        """Тест GET запроса"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ContactForm)
    
    def test_post_valid_data(self):
        """Тест отправки валидных данных"""
        data = {
            'name': 'Иван',
            'email': 'ivan@example.com',
            'message': 'Тест'
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('success'))
    
    def test_post_invalid_data(self):
        """Тест отправки невалидных данных"""
        data = {'name': 'Иван'}  # Неполные данные
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Обязательное поле.')
```

---

## Ключевые выводы

### Основные концепции

✅ **Формы** — инструмент для взаимодействия с пользователем  
✅ **forms.Form** — ручное создание, максимальная гибкость  
✅ **forms.ModelForm** — автоматическое создание из модели  
✅ **Валидация** — встроенная + пользовательская  
✅ **Виджеты** — управление отображением полей  

### Жизненный цикл формы

```
1. Создание формы (forms.py)
        ↓
2. Отображение в view (views.py)
        ↓
3. Рендеринг в шаблоне (template)
        ↓
4. Отправка пользователем (POST)
        ↓
5. Валидация (is_valid())
        ↓
6. Обработка данных (cleaned_data)
        ↓
7. Сохранение/редирект
```

### Лучшие практики

#### ✅ DO (Делайте)

```python
# 1. Всегда используйте CSRF токен
{% csrf_token %}

# 2. Валидируйте данные
if form.is_valid():
    # Безопасная обработка

# 3. Используйте cleaned_data
name = form.cleaned_data['name']

# 4. Обрабатывайте ошибки
if form.errors:
    # Показать ошибки пользователю

# 5. Редирект после POST
return redirect('success_page')
```

#### ❌ DON'T (Не делайте)

```python
# ❌ Не забывайте CSRF
<form method="post">  # Без {% csrf_token %}

# ❌ Не используйте данные без валидации
data = request.POST['name']  # Опасно!

# ❌ Не сохраняйте без проверки
form.save()  # Без is_valid()

# ❌ Не возвращайте render после POST
if request.method == 'POST':
    # ...
    return render(...)  # Плохо! Используйте redirect
```

---

## Полезные ресурсы

📚 **Документация:**
- Django Forms: https://docs.djangoproject.com/en/stable/topics/forms/
- ModelForm: https://docs.djangoproject.com/en/stable/topics/forms/modelforms/
- Validators: https://docs.djangoproject.com/en/stable/ref/validators/

📦 **Пакеты:**
- `django-crispy-forms` — красивые формы Bootstrap
- `django-widget-tweaks` — настройка виджетов в шаблонах
- `django-formtools` — wizard формы, preview

🔧 **Инструменты:**
- Django Debug Toolbar — отладка
- Postman — тестирование API
- Browser DevTools — проверка форм