# Django Models: Повна теорія

## 1. Основна роль моделей у Django ORM

**Модель** — це Python-клас, який представляє таблицю в базі даних. Кожен атрибут моделі відповідає полю таблиці.

### Зв'язок моделей із базою даних

Django ORM (Object-Relational Mapping) автоматично перетворює Python-код у SQL-запити, що дозволяє працювати з базою даних через об'єкти Python.

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

Ця модель автоматично створить таблицю `app_article` з полями `id`, `title`, `content`, `created_at`.

---

## 2. Основні елементи моделі

### class Meta

Метаклас `Meta` містить метадані моделі, які не є полями бази даних.

```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'articles'  # Назва таблиці в БД
        ordering = ['-created_at']  # Сортування за замовчуванням
        verbose_name = 'Стаття'  # Ім'я в однині
        verbose_name_plural = 'Статті'  # Ім'я в множині
        indexes = [
            models.Index(fields=['title']),
        ]
        unique_together = ['title', 'author']  # Унікальна комбінація полів
        permissions = [
            ('can_publish', 'Can publish articles'),
        ]
```

**Основні параметри Meta:**
- `db_table` — власна назва таблиці
- `ordering` — порядок сортування за замовчуванням
- `verbose_name` / `verbose_name_plural` — назви для адмін-панелі
- `abstract = True` — абстрактна модель (не створює таблицю)
- `managed = True` — чи керує Django таблицею
- `unique_together` — унікальні комбінації полів
- `indexes` — індекси для оптимізації

---

## 3. Типи полів у Django

### Текстові поля
```python
class Post(models.Model):
    title = models.CharField(max_length=200)  # Обмежений текст
    slug = models.SlugField(unique=True)  # URL-friendly текст
    content = models.TextField()  # Необмежений текст
    email = models.EmailField()  # Email з валідацією
```

### Числові поля
```python
class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    rating = models.FloatField()
    views = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)
```

### Дата і час
```python
class Event(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Тільки при створенні
    updated_at = models.DateTimeField(auto_now=True)  # При кожному оновленні
    event_date = models.DateField()
    event_time = models.TimeField()
```

### Відносини між моделями
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Один до багатьох
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Один до одного
    
class Student(models.Model):
    courses = models.ManyToManyField('Course')  # Багато до багатьох
```

### Інші типи полів
```python
class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    image = models.ImageField(upload_to='images/')
    url = models.URLField()
    json_data = models.JSONField()
    uuid = models.UUIDField(default=uuid.uuid4)
```

---

## 4. Атрибути полів

### Значення за замовчуванням
```python
class Article(models.Model):
    status = models.CharField(
        max_length=20,
        default='draft',
        choices=[
            ('draft', 'Чернетка'),
            ('published', 'Опубліковано'),
            ('archived', 'Архів'),
        ]
    )
    views = models.IntegerField(default=0)
```

### Валідація даних
```python
from django.core.validators import MinValueValidator, MaxValueValidator, EmailValidator

class Product(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
```

### Параметри полів
```python
class User(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=True,  # Унікальне значення
        null=False,  # Чи може бути NULL в БД
        blank=False,  # Чи може бути порожнім у формах
        db_index=True,  # Створити індекс
        help_text='Email користувача',
        verbose_name='Електронна пошта',
        editable=True,  # Чи можна редагувати
    )
```

---

## 5. Робота з міграціями

### Створення міграцій
```bash
# Створити міграції для всіх змін
python manage.py makemigrations

# Створити міграцію для конкретного додатку
python manage.py makemigrations app_name

# Створити порожню міграцію
python manage.py makemigrations --empty app_name

# Переглянути SQL міграції
python manage.py sqlmigrate app_name 0001
```

### Застосування міграцій
```bash
# Застосувати всі міграції
python manage.py migrate

# Застосувати міграції для конкретного додатку
python manage.py migrate app_name

# Відкотити до певної міграції
python manage.py migrate app_name 0003

# Скасувати всі міграції додатку
python manage.py migrate app_name zero

# Показати статус міграцій
python manage.py showmigrations
```

### Структура файлу міграції
```python
# migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
```

---
## EXAMPLE

### 🟢 **1. `python manage.py makemigrations`**

> Створити міграції для всіх змін

🔹 Django сканирует твои модели (`models.py`) и **создаёт файлы миграций** (в папке `migrations/`),
в которых записаны изменения структуры таблиц — например:

* добавлено новое поле,
* изменено имя колонки,
* создана новая модель (таблица),
* удалено поле и т. д.

📘 Пример:

```bash
python manage.py makemigrations
```

➡ создаст файлы вроде `0001_initial.py`, `0002_add_field_name.py` и т. д.

---

### 🟡 **2. `python manage.py makemigrations app_name`**

> Створити міграцію для конкретного додатку

🔹 Делает то же самое, но **только для указанного приложения**.
Полезно, если у тебя несколько Django-приложений, и ты хочешь создать миграции только для одного из них.

📘 Пример:

```bash
python manage.py makemigrations users
```

➡ создаст миграции только для приложения `users`.

---

### 🔵 **3. `python manage.py makemigrations --empty app_name`**

> Створити порожню міграцію

🔹 Создаёт **пустой файл миграции**, в который ты можешь вручную добавить Python-код для сложных изменений (например, кастомные SQL-команды, изменения данных, а не структуры таблиц).

📘 Пример:

```bash
python manage.py makemigrations --empty shop
```

➡ создаст файл вроде `0005_auto_empty.py`, где ты можешь вручную дописать:

```python
operations = [
    migrations.RunSQL("UPDATE products SET price = price * 1.1;")
]
```

---

### 🔴 **4. `python manage.py sqlmigrate app_name 0001`**

> Переглянути SQL міграції

🔹 Показывает **чистый SQL**, который Django собирается выполнить в базе данных,
если ты применишь миграцию `0001`.

📘 Пример:

```bash
python manage.py sqlmigrate users 0001
```

➡ выведет SQL-команды вроде:

```sql
CREATE TABLE "users_user" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "username" varchar(150) NOT NULL,
    "email" varchar(254) NOT NULL
);
```

Это удобно, чтобы понять, **какие реальные SQL-запросы** выполнятся при миграции.

---

💡 В целом:

| Команда                           | Что делает                                         |
| :-------------------------------- | :------------------------------------------------- |
| `makemigrations`                  | Создаёт файлы миграций из изменений моделей        |
| `makemigrations app_name`         | То же, но для одного приложения                    |
| `makemigrations --empty app_name` | Создаёт пустую миграцию для ручного редактирования |
| `sqlmigrate app_name 0001`        | Показывает SQL-код миграции                        |

---

## 6. CRUD-операції з моделями

### Створення (Create)
```python
# Спосіб 1: create()
article = Article.objects.create(
    title='Назва статті',
    content='Зміст статті'
)

# Спосіб 2: save()
article = Article(title='Назва', content='Зміст')
article.save()

# Спосіб 3: bulk_create() для множинного створення
Article.objects.bulk_create([
    Article(title='Стаття 1'),
    Article(title='Стаття 2'),
])

# Спосіб 4: get_or_create()
article, created = Article.objects.get_or_create(
    title='Унікальна назва',
    defaults={'content': 'Зміст'}
)
```

### Читання (Read)
```python
# Отримати всі записи
articles = Article.objects.all()

# Отримати один запис (викидає помилку, якщо не знайдено або більше одного)
article = Article.objects.get(id=1)

# Фільтрація
articles = Article.objects.filter(status='published')
articles = Article.objects.exclude(status='draft')

# Отримати перший/останній запис
first = Article.objects.first()
last = Article.objects.last()

# Перевірити існування
exists = Article.objects.filter(title='Test').exists()

# Підрахунок
count = Article.objects.count()
```

### Оновлення (Update)
```python
# Спосіб 1: update() - оновлює без викликів save()
Article.objects.filter(status='draft').update(status='published')

# Спосіб 2: save() - оновлює окремий об'єкт
article = Article.objects.get(id=1)
article.title = 'Нова назва'
article.save()

# Спосіб 3: update_or_create()
article, created = Article.objects.update_or_create(
    id=1,
    defaults={'title': 'Оновлена назва'}
)

# Оновити одне поле
article.save(update_fields=['title'])
```

### Видалення (Delete)
```python
# Видалити один об'єкт
article = Article.objects.get(id=1)
article.delete()

# Видалити множину об'єктів
Article.objects.filter(status='draft').delete()

# Видалити всі записи
Article.objects.all().delete()
```

---

## 7. Django ORM: Запити до бази даних

### QuerySet
QuerySet — це ліниве (lazy) представлення запиту до БД. Запит виконується лише при ітерації або перетворенні.

```python
# QuerySet не виконує запит
articles = Article.objects.filter(status='published')

# Запит виконується тут
for article in articles:
    print(article.title)

# Або тут
list(articles)
len(articles)
articles[0]
```

### Фільтрація даних
```python
# Точна відповідність
Article.objects.filter(status='published')

# Не дорівнює
Article.objects.exclude(status='draft')

# Містить
Article.objects.filter(title__contains='Django')
Article.objects.filter(title__icontains='django')  # Без урахування регістру

# Починається/закінчується
Article.objects.filter(title__startswith='How')
Article.objects.filter(title__endswith='?')

# Діапазон
Article.objects.filter(views__gt=100)  # Більше
Article.objects.filter(views__gte=100)  # Більше або дорівнює
Article.objects.filter(views__lt=1000)  # Менше
Article.objects.filter(views__lte=1000)  # Менше або дорівнює
Article.objects.filter(views__range=(100, 1000))  # Між значеннями

# Дата
from datetime import date
Article.objects.filter(created_at__year=2024)
Article.objects.filter(created_at__month=12)
Article.objects.filter(created_at__date=date.today())

# IN
Article.objects.filter(id__in=[1, 2, 3])

# NULL
Article.objects.filter(author__isnull=True)

# Сортування
Article.objects.order_by('-created_at')  # За спаданням
Article.objects.order_by('title', '-views')  # Комбіноване
```

### Складні запити (Q об'єкти)
```python
from django.db.models import Q

# OR умова
Article.objects.filter(Q(status='published') | Q(status='featured'))

# AND умова
Article.objects.filter(Q(status='published') & Q(views__gt=100))

# NOT умова
Article.objects.filter(~Q(status='draft'))

# Комбінації
Article.objects.filter(
    Q(title__icontains='django') | Q(content__icontains='django'),
    status='published'
)
```

### Агрегатні функції
```python
from django.db.models import Count, Sum, Avg, Max, Min

# Агрегація по всій таблиці
result = Article.objects.aggregate(
    total_views=Sum('views'),
    avg_views=Avg('views'),
    max_views=Max('views'),
    article_count=Count('id')
)
# result = {'total_views': 5000, 'avg_views': 250, ...}

# Анотація (додавання обчисленого поля до кожного об'єкта)
articles = Article.objects.annotate(
    comment_count=Count('comments')
)
for article in articles:
    print(article.comment_count)
```

### Групування даних
```python
# Групування по полю
authors_stats = Article.objects.values('author').annotate(
    article_count=Count('id'),
    total_views=Sum('views')
)

# Унікальні значення
Article.objects.values('status').distinct()

# Вибрати тільки певні поля
Article.objects.values('id', 'title')
Article.objects.values_list('id', 'title')  # Повертає кортежі
Article.objects.values_list('title', flat=True)  # Список значень
```

---

## 8. Відносини між моделями

### ForeignKey (один до багатьох)
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Article(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,  # Видалити статті при видаленні автора
        related_name='articles',  # Зворотній зв'язок: author.articles.all()
        null=True,
        blank=True
    )

# on_delete параметри:
# CASCADE - видалити пов'язані об'єкти
# PROTECT - заборонити видалення, якщо є пов'язані об'єкти
# SET_NULL - встановити NULL (потрібен null=True)
# SET_DEFAULT - встановити default значення
# SET(...) - встановити конкретне значення
# DO_NOTHING - нічого не робити

# Використання
author = Author.objects.create(name='Іван')
article = Article.objects.create(title='Стаття', author=author)

# Отримати статті автора
author.articles.all()

# Фільтрація через зв'язок
Article.objects.filter(author__name='Іван')
```

### OneToOneField (один до одного)
```python
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')

# Використання
user = User.objects.create(username='john')
profile = Profile.objects.create(user=user, bio='Developer')

# Доступ
user.profile.bio
profile.user.username
```

### ManyToManyField (багато до багатьох)
```python
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(
        Tag,
        related_name='articles',
        blank=True
    )

# Використання
article = Article.objects.create(title='Django Tutorial')
tag1 = Tag.objects.create(name='Python')
tag2 = Tag.objects.create(name='Django')

# Додати зв'язки
article.tags.add(tag1, tag2)
article.tags.set([tag1, tag2])  # Замінити всі

# Видалити зв'язки
article.tags.remove(tag1)
article.tags.clear()  # Видалити всі

# Отримати
article.tags.all()
tag1.articles.all()
```

### ManyToMany з проміжною моделлю
```python
class Student(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField('Course', through='Enrollment')

class Course(models.Model):
    name = models.CharField(max_length=100)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    enrolled_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']

# Використання
student = Student.objects.create(name='Іван')
course = Course.objects.create(name='Python')
Enrollment.objects.create(student=student, course=course, grade='A')

# Отримати з додатковими даними
enrollments = student.enrollment_set.all()
for enrollment in enrollments:
    print(enrollment.course.name, enrollment.grade)
```

---

## 9. Менеджери моделей

### Стандартний менеджер objects
```python
class Article(models.Model):
    title = models.CharField(max_length=200)
    
# Article.objects - це стандартний менеджер
```

### Кастомні менеджери
```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Article(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    
    objects = models.Manager()  # Стандартний менеджер
    published = PublishedManager()  # Кастомний менеджер

# Використання
Article.objects.all()  # Всі статті
Article.published.all()  # Тільки опубліковані
```

### Методи менеджера
```python
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='published')
    
    def by_author(self, author):
        return self.filter(author=author)
    
    def recent(self, days=7):
        from datetime.timedelta import days
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

class Article(models.Model):
    objects = ArticleManager()

# Використання
Article.objects.published()
Article.objects.by_author('John')
Article.objects.recent(30)

# Ланцюжок викликів
Article.objects.published().recent(7).order_by('-views')
```

---

## 10. Робота з транзакціями

### atomic()
```python
from django.db import transaction

# Декоратор
@transaction.atomic
def create_article_with_tags(title, tags):
    article = Article.objects.create(title=title)
    for tag_name in tags:
        tag = Tag.objects.create(name=tag_name)
        article.tags.add(tag)
    return article

# Контекстний менеджер
def transfer_money(from_account, to_account, amount):
    with transaction.atomic():
        from_account.balance -= amount
        from_account.save()
        
        to_account.balance += amount
        to_account.save()
```

### select_for_update()
```python
from django.db import transaction

with transaction.atomic():
    # Блокує рядки для оновлення
    article = Article.objects.select_for_update().get(id=1)
    article.views += 1
    article.save()
```

### Обробка помилок
```python
from django.db import IntegrityError, DatabaseError

try:
    Article.objects.create(title='Test')
except IntegrityError as e:
    print(f"Помилка унікальності: {e}")
except DatabaseError as e:
    print(f"Помилка БД: {e}")
```

---

## 11. Оптимізація роботи з моделями

### select_related() - для ForeignKey і OneToOne
```python
# Неоптимально (N+1 запитів)
articles = Article.objects.all()
for article in articles:
    print(article.author.name)  # Новий запит для кожної статті

# Оптимально (1 запит з JOIN)
articles = Article.objects.select_related('author')
for article in articles:
    print(article.author.name)  # Без додаткових запитів
```

### prefetch_related() - для ManyToMany і зворотних ForeignKey
```python
# Неоптимально
articles = Article.objects.all()
for article in articles:
    print(article.tags.all())  # Новий запит для кожної статті

# Оптимально (2 запити)
articles = Article.objects.prefetch_related('tags')
for article in articles:
    print(article.tags.all())  # Без додаткових запитів
```

### Комбінування
```python
articles = Article.objects.select_related('author').prefetch_related('tags', 'comments')
```

### only() і defer()
```python
# only() - завантажити тільки певні поля
Article.objects.only('id', 'title')

# defer() - не завантажувати певні поля
Article.objects.defer('content')
```

### Індекси
```python
class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['title', 'created_at']),
            models.Index(fields=['-created_at']),
        ]
```

### Кешування запитів
```python
from django.core.cache import cache

def get_articles():
    articles = cache.get('articles')
    if not articles:
        articles = list(Article.objects.all())
        cache.set('articles', articles, 300)  # 5 хвилин
    return articles
```

---

## 12. Адмін-панель і Django Models

### Базова реєстрація
```python
# admin.py
from django.contrib import admin
from .models import Article

admin.site.register(Article)
```

### Кастомізація відображення
```python
from django.contrib import admin

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    # Відображення в списку
    list_display = ['title', 'author', 'status', 'created_at', 'views']
    
    # Фільтри
    list_filter = ['status', 'created_at', 'author']
    
    # Пошук
    search_fields = ['title', 'content']
    
    # Поля тільки для читання
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    # Порядок полів
    fields = ['title', 'content', 'author', 'status']
    
    # Горизонтальний фільтр для ManyToMany
    filter_horizontal = ['tags']
    
    # Дії
    actions = ['make_published']
    
    # Кількість записів на сторінці
    list_per_page = 50
    
    # Сортування за замовчуванням
    ordering = ['-created_at']
    
    # Дата ієрархії
    date_hierarchy = 'created_at'
    
    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Опублікувати вибрані статті"
```

### Інлайни (вкладені моделі)
```python
class CommentInline(admin.TabularInline):  # або admin.StackedInline
    model = Comment
    extra = 1
    fields = ['author', 'text']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
```

---
# Реєстрації моделей в адмін-панелі  

Команда для реєстрації моделей в адмін-панелі - це  **код у файлі `admin.py`**.

## 📝 Реєстрація моделей в адмін-панелі

### Спосіб 1: Простий (декоратор)

```python
from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
```

### Спосіб 2: Класичний

```python
from django.contrib import admin
from .models import Category, Ad, Comment, UserProfile

admin.site.register(Category)
admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(UserProfile)
```

---
## ✅ Всі 4 моделі зареєстровані:

1. **`@admin.register(UserProfile)`** - рядок 13
2. **`@admin.register(Category)`** - рядок 27  
3. **`@admin.register(Ad)`** - рядок 55
4. **`@admin.register(Comment)`** - рядок 129 (далі у файлі)---

## 🎨 Що додано до адмін-панелі?

### 1. **UserProfile**
- Відображення: user, phone_number, address
- Пошук за username та phone_number

### 2. **Category**
- Відображення: name, description, **кількість активних оголошень**
- Пошук за назвою та описом

### 3. **Ad** (найбільше налаштувань!)
- Відображення: title, category, user, price, is_active, created_at, **кількість коментарів**
- **Фільтри**: за статусом (активне/неактивне), категорією, датою
- Пошук за заголовком, описом, username
- Організовані поля у групи (Основна інформація, Користувач, Статус, Дати)

### 4. **Comment**
- Відображення: user, ad, скорочений контент, created_at
- Фільтр за датою створення
- Пошук за текстом, username, заголовком оголошення
