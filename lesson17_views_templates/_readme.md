# Конспект лекції: Views (Представлення) та Templates (Шаблони) в Django

## 1. Повторення: Routing (Маршрутизація)

### Основні поняття

**Routing (Маршрутизація)** - визначення шляхів (URL), за якими користувач може отримати доступ до різних сторінок.

### Ключові файли

| Файл | Призначення |
|------|-------------|
| `settings.py` | Налаштування проекту |
| `urls.py` (проект) | Точка відліку маршрутизації |
| `urls.py` (застосунок) | Маршрути конкретного застосунку |
| `views.py` | Логіка обробки запитів |

### Функції маршрутизації

**1. `path()`** - статичні маршрути
```python
path('home/', views.home, name='home')
```

**2. `re_path()`** - динамічні маршрути з regex
```python
re_path(r'^articles/(?P<slug>[\w-]+)/$', views.article_detail)
```

**3. `include()`** - підключення маршрутів з застосунків
```python
path('lesson1/', include('lesson1.urls'))
```

### Навіщо `include()`?

**Переваги:**
✅ Модульність - кожен застосунок має свої маршрути
✅ Зручність - легко знайти та змінити
✅ Швидкість розробки - не потрібно шукати по всьому проекту

## 2. Архітектура MTV в Django

### Від MVC до MTV

Django використовує модифікацію класичного MVC:

```
┌──────────────┐
│   Request    │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   URLs.py    │ ← Маршрутизація
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   Views.py   │ ← Логіка обробки (Controller)
└──────┬───────┘
       │
       ├──→ Models (база даних)
       │
       ↓
┌──────────────┐
│  Templates   │ ← Відображення (View)
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   Response   │
└──────────────┘
```

**MTV компоненти:**
- **Model** - робота з базою даних
- **Template** - HTML-шаблони для відображення
- **View** - обробка запитів та бізнес-логіка

## 3. Templates (Шаблони)

### Що таке шаблон?

> **Шаблон** - це HTML-файл, який містить шаблонну мову Django (DTL) для динамічного рендерингу контенту.

### Навіщо шаблони?

**Принцип DRY (Don't Repeat Yourself)**

```python
# ❌ Погано - повторюваний код
def page1(request):
    return HttpResponse("<html><head>...</head><body>Page 1</body></html>")

def page2(request):
    return HttpResponse("<html><head>...</head><body>Page 2</body></html>")

# ✅ Добре - шаблони
def page1(request):
    return render(request, 'page1.html')

def page2(request):
    return render(request, 'page2.html')
```

### Структура шаблонів

```
myproject/
├── templates/              # Загальна директорія
│   ├── base.html          # Базовий шаблон
│   ├── lesson1/           # Шаблони застосунку
│   │   ├── home.html
│   │   ├── about.html
│   │   └── contact.html
│   └── lesson2/
│       └── ...
```

**ВАЖЛИВО:** Кожен застосунок має свою піддиректорію в `templates/`

## 4. Django Template Language (DTL)

### Чотири типи об'єктів

#### 1. Змінні (Variables)

**Синтаксис:** `{{ variable }}`

```html
<p>Привіт, {{ user.username }}!</p>
<p>Ваш вік: {{ user.age }}</p>
```

**З контексту:**
```python
def profile(request):
    context = {
        'user': {
            'username': 'John',
            'age': 25
        }
    }
    return render(request, 'profile.html', context)
```

#### 2. Теги (Tags)

**Синтаксис:** `{% tag %}...{% endtag %}`

**Умовні конструкції:**
```html
{% if user.is_authenticated %}
    <p>Привіт, {{ user.username }}!</p>
{% else %}
    <p>Будь ласка, увійдіть у систему</p>
{% endif %}
```

**Цикли:**
```html
<ul>
{% for product in products %}
    <li>{{ product.name }} - {{ product.price }}₴</li>
{% endfor %}
</ul>
```

**Блоки (для наслідування):**
```html
{% block content %}
    <!-- Контент тут -->
{% endblock %}
```

#### 3. Фільтри (Filters)

**Синтаксис:** `{{ variable|filter }}`

```html
<!-- Дата -->
<p>Сьогодні: {{ today|date:"Y-m-d" }}</p>

<!-- Текст -->
<p>{{ text|lower }}</p>          <!-- нижній регістр -->
<p>{{ text|upper }}</p>          <!-- верхній регістр -->
<p>{{ text|title }}</p>          <!-- Title Case -->
<p>{{ text|capitalize }}</p>     <!-- Перша літера велика -->

<!-- Довжина -->
<p>Кількість символів: {{ text|length }}</p>
```

**З параметрами:**
```html
{{ text|truncatewords:5 }}  <!-- Перші 5 слів -->
```

#### 4. Коментарі (Comments)

**Синтаксис:** `{# коментар #}`

```html
{# Це коментар - не відображається в HTML #}

{% comment %}
    Багаторядковий
    коментар
{% endcomment %}
```

### Порівняльна таблиця

| Тип | Синтаксис | Призначення |
|-----|-----------|-------------|
| Змінні | `{{ var }}` | Вивід даних |
| Теги | `{% tag %}` | Логіка (if, for, block) |
| Фільтри | `{{ var\|filter }}` | Обробка даних |
| Коментарі | `{# text #}` | Коментарі в коді |

## 5. Наслідування шаблонів (Template Inheritance)

### Концепція

Як у класах - створюємо базовий шаблон, потім наслідуємо його.

### Базовий шаблон (`base.html`)

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мій сайт{% endblock %}</title>
</head>
<body>
    <header>
        <h1>{% block header %}Заголовок сайту{% endblock %}</h1>
        {% include 'navbar.html' %}
    </header>
    
    <main>
        {% block content %}
            <!-- Контент за замовчуванням -->
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>© 2025 Мій сайт</p>
        {% endblock %}
    </footer>
</body>
</html>
```

### Дочірній шаблон (`home.html`)

```html
{% extends 'base.html' %}

{% block title %}Головна сторінка{% endblock %}

{% block content %}
    <h2>Ласкаво просимо!</h2>
    <p>Це головна сторінка нашого сайту.</p>
{% endblock %}
```

### Що відбувається?

1. `{% extends 'base.html' %}` - наслідуємо базовий шаблон
2. Django підставляє вміст блоків з `home.html` у відповідні блоки `base.html`
3. Блоки, які не перевизначені, залишаються як у базовому шаблоні

## 6. Включення шаблонів (Template Inclusion)

### Концепція

Як композиція в класах - включаємо один шаблон в інший.

### Фрагмент навігації (`navbar.html`)

```html
<nav>
    <ul>
        <li><a href="{% url 'home' %}">Головна</a></li>
        <li><a href="{% url 'about' %}">Про нас</a></li>
        <li><a href="{% url 'contact' %}">Контакти</a></li>
    </ul>
</nav>
```

### Включення в базовий шаблон

```html
<header>
    <h1>Мій сайт</h1>
    {% include 'navbar.html' %}
</header>
```

### Різниця між `extends` та `include`

| `extends` | `include` |
|-----------|-----------|
| Наслідування | Включення |
| Один раз на файл | Скільки завгодно разів |
| Перевизначає блоки | Вставляє як є |
| Для структури сторінки | Для фрагментів коду |

## 7. Views (Представлення)

### Що таке View?

> **View** - функція або клас, що обробляє HTTP-запит та повертає HTTP-відповідь.

### Типи представлень

#### 1. Function-Based Views (FBV)

**Найпростіший варіант:**

```python
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Привіт з функції!")

def about(request):
    context = {
        'title': 'Про нас',
        'description': 'Інформація про компанію'
    }
    return render(request, 'about.html', context)
```

**Структура:**
```python
def view_name(request):
    # 1. Обробка даних
    # 2. Робота з моделями (БД)
    # 3. Формування контексту
    # 4. Повернення відповіді
    return render(request, 'template.html', context)
```

**Переваги FBV:**
✅ Просто і зрозуміло
✅ Гнучкість
✅ Підходить для простої логіки

**Недоліки FBV:**
❌ Багато повторюваного коду
❌ Потрібно самостійно перевіряти методи (GET, POST)

#### 2. Class-Based Views (CBV)

**На базі `View`:**

```python
from django.views import View
from django.http import HttpResponse

class HomeView(View):
    def get(self, request):
        return HttpResponse("GET запит")
    
    def post(self, request):
        return HttpResponse("POST запит")
```

**Переваги CBV:**
✅ Автоматична обробка методів (GET, POST, DELETE)
✅ Можливість наслідування
✅ Менше коду

**Недоліки CBV:**
❌ Складніше для початківців
❌ Потрібно знати методи класу

#### 3. Generic Views

**Найлаконічніший варіант:**

```python
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'lesson1/home.html'
```

**Це все!** Django автоматично:
- Обробляє запит
- Рендерить шаблон
- Повертає відповідь

**Типи Generic Views:**

| Generic View | Призначення |
|--------------|-------------|
| `TemplateView` | Відображення простого шаблону |
| `ListView` | Список об'єктів |
| `DetailView` | Деталі одного об'єкта |
| `CreateView` | Створення об'єкта |
| `UpdateView` | Оновлення об'єкта |
| `DeleteView` | Видалення об'єкта |

### Порівняння типів Views

```python
# FBV
def home(request):
    return render(request, 'home.html', {'message': 'Hello'})

# CBV на базі View
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html', {'message': 'Hello'})

# Generic View
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Hello'
        return context
```

## 8. Передача даних між Views та Templates

### Контекст (Context)

**Context** - словник даних, які передаються з view у template.

```python
def user_profile(request):
    context = {
        'username': 'John',
        'age': 25,
        'email': 'john@example.com',
        'friends': ['Alice', 'Bob', 'Charlie']
    }
    return render(request, 'profile.html', context)
```

**У шаблоні (`profile.html`):**
```html
<h1>Профіль {{ username }}</h1>
<p>Вік: {{ age }}</p>
<p>Email: {{ email }}</p>

<h2>Друзі:</h2>
<ul>
{% for friend in friends %}
    <li>{{ friend }}</li>
{% endfor %}
</ul>
```

### Request об'єкт

Django автоматично додає `request` у контекст:

```html
<!-- Поточний користувач -->
<p>Привіт, {{ request.user.username }}</p>

<!-- Метод запиту -->
<p>Метод: {{ request.method }}</p>

<!-- GET параметри -->
<p>Пошук: {{ request.GET.q }}</p>
```

## 9. Redirects (Перенаправлення)

### Статус-коди 3xx

**300-ті** - перенаправлення (redirects)

### Використання `redirect()`

```python
from django.shortcuts import redirect

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')  # За ім'ям маршруту
    else:
        return redirect('/login/')  # За шляхом

def logout_view(request):
    # Вихід з системи
    return redirect('login')
```

### Redirect після форми

```python
def register(request):
    if request.method == 'POST':
        # Обробка форми
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Збереження користувача
        # ...
        
        # Автоматичний вхід після реєстрації
        return redirect('home')
    
    return render(request, 'register.html')
```

### Переваги використання `name` у URLs

```python
# urls.py
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
]

# У view
return redirect('home')  # Не потрібно знати точний шлях

# У template
<a href="{% url 'home' %}">Головна</a>
```

## 10. Повний приклад роботи MTV

### Структура проекту

```
mysite/
├── mysite/
│   ├── settings.py
│   └── urls.py          # path('', include('blog.urls'))
├── blog/
│   ├── urls.py          # Маршрути застосунку
│   ├── views.py         # Логіка
│   └── templates/
│       └── blog/
│           ├── base.html
│           ├── home.html
│           └── about.html
└── manage.py
```

### 1. URLs проекту (`mysite/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Корінь → blog
]
```

### 2. URLs застосунку (`blog/urls.py`)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
```

### 3. Views (`blog/views.py`)

```python
from django.shortcuts import render

def home(request):
    context = {
        'title': 'Головна',
        'message': 'Ласкаво просимо на наш сайт!'
    }
    return render(request, 'blog/home.html', context)

def about(request):
    context = {
        'title': 'Про нас',
        'company': 'Django Company',
        'year': 2025
    }
    return render(request, 'blog/about.html', context)

def contact(request):
    context = {
        'title': 'Контакти',
        'email': 'info@example.com',
        'phone': '+380123456789'
    }
    return render(request, 'blog/contact.html', context)
```

### 4. Базовий шаблон (`templates/blog/base.html`)

```html
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Мій сайт{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Мій блог</h1>
        {% include 'blog/navbar.html' %}
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>© 2025 Всі права захищені</p>
    </footer>
</body>
</html>
```

### 5. Навігація (`templates/blog/navbar.html`)

```html
<nav>
    <ul>
        <li><a href="{% url 'home' %}">Головна</a></li>
        <li><a href="{% url 'about' %}">Про нас</a></li>
        <li><a href="{% url 'contact' %}">Контакти</a></li>
    </ul>
</nav>
```

### 6. Сторінка Home (`templates/blog/home.html`)

```html
{% extends 'blog/base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h2>{{ message }}</h2>
    <p>Це головна сторінка</p>
{% endblock %}
```

### 7. Сторінка About (`templates/blog/about.html`)

```html
{% extends 'blog/base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h2>Про компанію {{ company }}</h2>
    <p>Ми працюємо з {{ year }} року</p>
{% endblock %}
```

## 11. Типові помилки та їх вирішення

### Помилка 1: Template Does Not Exist

```
TemplateDoesNotExist at /
blog/home.html
```

**Причини:**
- Неправильний шлях до шаблону
- Шаблон знаходиться не в тій директорії
- Не створена директорія `templates/`

**Рішення:**
```python
# Перевірте шлях
return render(request, 'blog/home.html', context)
#                       └──┬──┘ └───┬───┘
#                     застосунок  файл

# Структура:
# templates/
#   └── blog/
#       └── home.html
```

### Помилка 2: Syntax Error у шаблоні

```
TemplateSyntaxError at /
Invalid block tag
```

**Причини:**
- Відсутність закриваючого тегу
- Пробіли в тегах `{{ variable }}` (правильно) vs `{{ variable}}` (неправильно)
- Неправильний синтаксис

**Рішення:**
```html
<!-- ❌ Погано -->
{% if user %}
    <p>Hello</p>
{# Немає {% endif %} #}

<!-- ✅ Добре -->
{% if user %}
    <p>Hello</p>
{% endif %}
```

### Помилка 3: View не знайдено

```
AttributeError: module 'blog.views' has no attribute 'home'
```

**Причина:** Функція не створена або помилка в назві

**Рішення:**
```python
# views.py
def home(request):  # Має співпадати з urls.py
    return render(request, 'home.html')

# urls.py
path('', views.home, name='home')  # views.home
```

## 12. Найкращі практики

### Організація шаблонів

```
✅ Правильно:
templates/
├── base.html           # Загальний базовий
├── blog/
│   ├── home.html
│   └── post_list.html
└── shop/
    ├── products.html
    └── cart.html

❌ Неправильно:
templates/
├── home.html          # Невідомо, чий це шаблон
├── products.html
└── cart.html
```

### Іменування

```python
# ✅ Добре
def user_profile(request):
    ...

class UserProfileView(TemplateView):
    ...

# ❌ Погано
def view1(request):  # Незрозуміла назва
    ...
```

### Контекст

```python
# ✅ Добре - зрозумілі ключі
context = {
    'username': user.name,
    'post_count': Post.objects.count(),
    'is_admin': request.user.is_staff
}

# ❌ Погано
context = {
    'a': user.name,
    'b': Post.objects.count(),
    'c': request.user.is_staff
}
```

## 13. Корисні шаблонні теги

### URL

```html
<!-- Посилання за ім'ям маршруту -->
<a href="{% url 'home' %}">Головна</a>

<!-- З параметрами -->
<a href="{% url 'post_detail' post.id %}">Читати</a>
```

### Static files (пізніше)

```html
{% load static %}
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

### CSRF токен (для форм)

```html
<form method="POST">
    {% csrf_token %}
    <input type="text" name="username">
    <button type="submit">Надіслати</button>
</form>
```

## Домашнє завдання

### Завдання: Створити Django застосунок з шаблонами

**Вимоги:**
1. Створити застосунок `my_app` або `lesson2`
2. Реалізувати 3 представлення:
   - **Home** (`home.html`) - вітальна сторінка
   - **About** (`about.html`) - інформація про сайт
   - **Contact** (`contact.html`) - контактна інформація

3. Використати шаблонну систему Django:
   - Створити `base.html` з загальним каркасом
   - Успадкувати `base.html` у всіх шаблонах
   - Додати навігаційну панель через `{% include 'navbar.html' %}`

4. Налаштувати URL-адреси
5. Запустити сервер та протестувати

**Бонус:**
- Використати Generic Views
- Додати динамічний контекст

## Корисні посилання

- **Django Templates:** https://docs.djangoproject.com/en/5.0/topics/templates/
- **Class-Based Views:** https://docs.djangoproject.com/en/5.0/topics/class-based-views/
- **Generic Views:** https://docs.djangoproject.com/en/5.0/ref/class-based-views/

---

**Ключові висновки:**
- **DRY принцип** - не повторюйте код
- **Наслідування шаблонів** - створюйте базовий та успадковуйте
- **3 типи Views** - FBV (просто), CBV (гнучко), Generic (швидко)
- **Контекст** - словник для передачі даних у шаблон
- **4 типи DTL** - змінні `{{ }}`, теги `{% %}`, фільтри `|`, коментарі `{# #}`