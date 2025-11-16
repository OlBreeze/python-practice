# 📚 Пошагове пояснення структури Django проекту

## 🎯 Загальна логіка

Django проект складається з:
1. **Головної папки проекту** (налаштування)
2. **Додатків** (функціонал)
3. **Шаблонів** (HTML)
4. **Статики** (CSS/JS/зображення)

---

## 📂 РІВЕНЬ 1: Корінь проекту

```
project/                    # Головна папка (контейнер)
├── manage.py              # Головний інструмент управління проектом
├── requirements.txt       # Список всіх бібліотек для встановлення
└── db.sqlite3            # База даних (створюється після migrate)
```

### `manage.py`
**Призначення**: Головна команда для всіх операцій
```bash
python manage.py runserver      # Запустити сервер
python manage.py migrate        # Застосувати міграції
python manage.py createsuperuser # Створити адміна
```

### `requirements.txt`
**Призначення**: Список залежностей проекту
```txt
Django==4.2.7
djangorestframework==3.14.0
...
```
Встановлення: `pip install -r requirements.txt`

---

## 📂 РІВЕНЬ 2: Папка налаштувань `project/`

```
project/project/           # Папка з налаштуваннями проекту
├── __init__.py           # Робить папку Python пакетом
├── settings.py           # ГОЛОВНИЙ файл налаштувань
├── urls.py               # ГОЛОВНИЙ маршрутизатор URL
├── wsgi.py              # Для розгортання на сервері
└── asgi.py              # Для асинхронних додатків
```

### `settings.py` ⭐ НАЙВАЖЛИВІШИЙ
**Призначення**: Всі налаштування проекту
```python
# Що тут налаштовується:
SECRET_KEY = '...'                    # Секретний ключ
DEBUG = True                          # Режим розробки
ALLOWED_HOSTS = ['localhost']         # Дозволені хости

INSTALLED_APPS = [                    # Встановлені додатки
    'django.contrib.admin',
    'blog',  # ← Наш додаток
]

DATABASES = {...}                     # Підключення до БД
TEMPLATES = {...}                     # Налаштування шаблонів
STATIC_URL = '/static/'              # URL для статики
MEDIA_URL = '/media/'                # URL для завантажених файлів

AUTH_USER_MODEL = 'blog.CustomUser'  # Кастомна модель користувача
```

### `urls.py` (головний)
**Призначення**: Головний маршрутизатор - розподіляє URL по додатках
```python
urlpatterns = [
    path('admin/', admin.site.urls),        # /admin/ → адмінка Django
    path('', include('blog.urls')),         # / → додаток blog
    path('api/', include('blog.api_urls')), # /api/ → REST API
]
```

**Логіка**:
- Користувач заходить на `/article/test/`
- Django дивиться в головний `urls.py`
- Бачить `path('', include('blog.urls'))` 
- Передає запит в `blog/urls.py`
- Там знаходить відповідний view

---

## 📂 РІВЕНЬ 3: Додаток `blog/`

Додаток = окрема функціональна частина проекту (блог, магазин, форум...)

```
blog/                      # Додаток блогу
├── __init__.py           
├── apps.py               # Конфігурація додатку
├── models.py             # Моделі даних (таблиці БД)
├── views.py              # Логіка обробки запитів
├── urls.py               # Маршрути додатку
├── admin.py              # Налаштування адмінки
├── forms.py              # Форми
├── tests.py              # Тести
└── migrations/           # Історія змін БД
```

---

## 🗄️ МОДЕЛІ (`models.py`)

**Призначення**: Опис структури даних (таблиць БД)

```python
class Article(models.Model):
    title = models.CharField(max_length=200)  # Колонка title
    content = models.TextField()              # Колонка content
    author = models.ForeignKey(User)          # Зв'язок з User
```

**Що відбувається**:
1. Ви описуєте модель в коді Python
2. Django генерує SQL (`makemigrations`)
3. Створює таблицю в БД (`migrate`)

**Файли в артефакті**:
- `models.py` - основні моделі (Article, Comment, Tag...)
- **Кастомні поля**: `UpperCaseCharField`, `PhoneNumberField`, `JSONField`

---

## 📝 ФОРМИ (`forms.py`)

**Призначення**: Валідація та обробка даних від користувача

```python
class ArticleForm(forms.ModelForm):
    def clean_title(self):
        # Перевірка заголовку
        if len(title) < 10:
            raise ValidationError("Замало символів!")
```

**Логіка**:
1. Користувач заповнює форму
2. Django перевіряє дані через валідатори
3. Якщо OK → зберігає, якщо ні → показує помилки

**В артефакті**:
- **Кастомні валідатори**: `validate_no_profanity`, `validate_min_words`
- **Кастомні віджети**: `ColorPickerWidget`, `TagSelectWidget`
- **Кастомні поля**: `HexColorField`, `PhoneNumberFormField`

---

## 👁️ VIEWS (`views.py`)

**Призначення**: Логіка обробки HTTP запитів

```python
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    
    def get_queryset(self):
        # Отримати статті з БД
        return Article.objects.filter(status='published')
```

**Логіка роботи**:
1. Користувач заходить на URL (`/`)
2. `urls.py` викликає відповідний View
3. View отримує дані з БД (моделі)
4. Передає в шаблон
5. Повертає HTML

**В артефакті**:
- `ArticleListView` - список статей з фільтрами
- `ArticleDetailView` - деталі статті + форма коментарів
- `ArticleCreateView` - створення статті
- `SearchView` - пошук

---

## 🎨 АДМІНКА (`admin.py`)

**Призначення**: Налаштування панелі адміністратора Django

```python
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status']  # Що показувати
    list_filter = ['status', 'created_at']        # Фільтри
    search_fields = ['title', 'content']          # Пошук
    actions = ['publish_articles']                # Дії
```

**Що можна**:
- Переглядати/редагувати дані
- Фільтрувати і сортувати
- Виконувати масові операції
- Inline-редагування (редагувати пов'язані об'єкти)

**В артефакті**:
- **Кастомні фільтри**: `ViewsCountFilter`, `RecentArticlesFilter`
- **Кастомні дії**: публікація, архівування, схвалення
- **Inline-моделі**: редагування коментарів всередині статті

---

## 🛣️ МАРШРУТИ (`urls.py`)

**Призначення**: Зв'язок URL → View

```python
# blog/urls.py
urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
]
```

**Як працює**:
- `/` → `ArticleListView`
- `/article/test-article/` → `ArticleDetailView` (передає `slug='test-article'`)

**Два файли**:
- `blog/urls.py` - веб-інтерфейс
- `blog/api_urls.py` - REST API

---

## 🔌 MIDDLEWARE (`middleware.py`)

**Призначення**: Обробка ВСІХ запитів до/після View

```python
class CustomHeaderMiddleware:
    def process_response(self, request, response):
        response['X-Custom-Header'] = 'MyValue'
        return response
```

**Логіка**:
```
Запит → Middleware 1 → Middleware 2 → View → Middleware 2 → Middleware 1 → Відповідь
```

**В артефакті**:
- `CustomHeaderMiddleware` - додає кастомні заголовки
- `RequestTimingMiddleware` - вимірює час обробки
- `SecurityMiddleware` - додає security заголовки
- `UserActivityMiddleware` - відстежує активність

**Налаштування** в `settings.py`:
```python
MIDDLEWARE = [
    'blog.middleware.CustomHeaderMiddleware',  # ← Тут
]
```

---

## 📡 REST API

### `serializers.py`
**Призначення**: Перетворення моделей в JSON і назад

```python
class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer()  # Вкладений серіалізатор
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'content']
```

**Що робить**:
```python
# Python об'єкт → JSON
article = Article.objects.first()
serializer = ArticleSerializer(article)
print(serializer.data)  # {'id': 1, 'title': '...', ...}

# JSON → Python об'єкт
data = {'title': 'New', 'content': '...'}
serializer = ArticleSerializer(data=data)
serializer.is_valid()
serializer.save()  # Створює Article в БД
```

### `api_views.py`
**Призначення**: ViewSets для REST API (як View, але для API)

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]  # Фільтрація
```

**Автоматично створює**:
- `GET /api/articles/` - список
- `POST /api/articles/` - створити
- `GET /api/articles/1/` - деталі
- `PUT /api/articles/1/` - оновити
- `DELETE /api/articles/1/` - видалити

**В артефакті**:
- Фільтрація: `?status=published&tag=python`
- Пошук: `?search=django`
- Кастомні ендпоінти: `/api/articles/popular/`
- Дозволи: `IsAuthorOrReadOnly`

---

## 📶 СИГНАЛИ (`signals.py`)

**Призначення**: Виконання коду автоматично при певних подіях

```python
@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    if created:
        # Коли створюється нова стаття
        send_email(...)
        print(f"Створено: {instance.title}")
```

**Події**:
- `post_save` - після збереження
- `pre_save` - перед збереженням
- `post_delete` - після видалення
- `m2m_changed` - при зміні many-to-many зв'язків

**В артефакті**:
- Відправка email при публікації
- Автогенерація slug
- Логування всіх операцій
- Сповіщення автора про коментар

---

## 🗃️ SQL ЗАПИТИ (`queries.py`)

**Призначення**: Складні SQL запити через ORM або raw SQL

```python
# Через ORM
Article.objects.filter(status='published').annotate(
    comment_count=Count('comments')
).order_by('-views_count')

# Через raw SQL
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM blog_article WHERE status='published'")
    return cursor.fetchall()
```

**Коли використовувати**:
- Складні агрегації
- Оптимізація продуктивності
- Специфічні SQL функції

---

## 📊 МЕТРИКИ (`metrics.py`)

**Призначення**: Збір статистики роботи додатку

```python
class RequestMetrics:
    def record_request(self, path, duration):
        # Записати час обробки запиту
        
class BlogMetrics:
    def get_article_metrics(self):
        # Статистика статей
        return {
            'total': Article.objects.count(),
            'published': Article.objects.filter(status='published').count(),
        }
```

**Що відстежується**:
- Кількість запитів до кожного URL
- Середній час відповіді
- Рівень помилок
- Статистика блогу

**Перегляд**: `python manage.py show_metrics`

---

## 📝 ЛОГУВАННЯ (`logging_config.py`)

**Призначення**: Запис логів в файли

```python
LOGGING = {
    'handlers': {
        'file': {
            'filename': 'logs/blog.log',
        },
        'error_file': {
            'filename': 'logs/errors.log',
        }
    }
}
```

**Файли логів**:
- `logs/blog.log` - всі події
- `logs/errors.log` - тільки помилки
- `logs/access.log` - запити користувачів

**Використання в коді**:
```python
import logging
logger = logging.getLogger('blog')
logger.info("Створено статтю")
logger.error("Помилка!")
```

---

## 🎨 ШАБЛОНИ (`templates/`)

```
templates/
├── base.html                    # Базовий шаблон (header, footer)
└── blog/
    ├── article_list.html       # Список статей
    ├── article_detail.html     # Деталі статті
    └── article_form.html       # Форма створення
```

### `base.html`
**Призначення**: Загальна структура всіх сторінок

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Блог{% endblock %}</title>
</head>
<body>
    <nav>...</nav>
    {% block content %}{% endblock %}
    <footer>...</footer>
</body>
</html>
```

### `article_list.html`
**Призначення**: Відображення списку статей

```html
{% extends 'base.html' %}

{% block content %}
    <h1>Статті</h1>
    {% for article in articles %}
        <h2>{{ article.title }}</h2>
        <p>{{ article.content|truncatewords:50 }}</p>
    {% endfor %}
{% endblock %}
```

---

## 🏷️ TEMPLATE TAGS (`templatetags/blog_tags.py`)

**Призначення**: Кастомні функції для шаблонів

```python
@register.simple_tag
def get_popular_articles(count=5):
    return Article.objects.order_by('-views_count')[:count]

@register.filter
def reading_time(text):
    words = len(text.split())
    return words / 200  # хвилин
```

**Використання**:
```html
{% load blog_tags %}

{% get_popular_articles 10 as popular %}
{% for article in popular %}...{% endfor %}

<p>Час читання: {{ article.content|reading_time }} хв</p>
```

---

## 📦 ДОПОМІЖНІ ФАЙЛИ

### `context_processors.py`
**Призначення**: Глобальні змінні для ВСІХ шаблонів

```python
def global_context(request):
    return {
        'site_name': 'Мій Блог',
        'current_year': 2025,
        'recent_articles': Article.objects.all()[:5]
    }
```

Тепер в будь-якому шаблоні: `{{ site_name }}`, `{{ current_year }}`

### `apps.py`
**Призначення**: Конфігурація додатку

```python
class BlogConfig(AppConfig):
    name = 'blog'
    
    def ready(self):
        import blog.signals  # Завантажити сигнали
```

---

## 🎯 ЯК ВСЕ ПРАЦЮЄ РАЗОМ

### Приклад: Користувач створює статтю

```
1. Користувач: заходить на /article/create/
   ↓
2. urls.py: path('article/create/') → ArticleCreateView
   ↓
3. Middleware: CustomHeaderMiddleware → вимірює час
   ↓
4. View (ArticleCreateView):
   - Створює форму (ArticleForm)
   - Передає в шаблон
   ↓
5. Template (article_form.html):
   - Відображає форму
   - Користувач заповнює і надсилає
   ↓
6. View:
   - Валідує через форму (forms.py)
   - Зберігає в БД (models.py)
   ↓
7. Signal (post_save):
   - Автоматично генерує slug
   - Відправляє email
   - Логує подію
   ↓
8. Redirect на деталі статті
```

---

## 💡 ПІДСУМОК

| Файл | Призначення | Коли редагувати |
|------|-------------|-----------------|
| `settings.py` | Налаштування всього | При додаванні функцій |
| `urls.py` | Маршрути | При додаванні сторінок |
| `models.py` | Структура БД | При зміні даних |
| `views.py` | Логіка сторінок | Для кожної сторінки |
| `forms.py` | Валідація форм | При створенні форм |
| `admin.py` | Адмінка | Для зручності адміна |
| `serializers.py` | API JSON | Для REST API |
| `templates/` | HTML | Для відображення |
| `signals.py` | Автоматизація | Для фонових завдань |

**Головне правило**: Кожен файл має свою роль - не змішуйте! 🎯