# Конспект лекції: Models (Моделі) в Django

## 1. Повторення: Views та Templates

### Views (Представлення)

**Три типи представлень:**

| Тип | Опис | Використання |
|-----|------|--------------|
| **FBV** (Function-Based) | Функції | Проста логіка, гнучкість |
| **CBV** (Class-Based) | Класи на базі `View` | ООП, масштабованість |
| **Generic Views** | Універсальні класи | Швидка реалізація типових завдань |

### Templates (Шаблони)

**Принцип DRY (Don't Repeat Yourself)**

```
Base Template → Успадкування (extends) → Конкретні сторінки
              → Включення (include) → Фрагменти (navbar, footer)
```

**Різниця:**
- `{% extends 'base.html' %}` - наслідування структури
- `{% include 'navbar.html' %}` - вставка фрагменту

## 2. Архітектура MTV - роль Models

### Що таке Model?

> **Model (Модель)** - це Python-клас, який визначає структуру таблиці бази даних та надає інтерфейс для роботи з даними.

### MTV паттерн

```
┌─────────┐
│  Model  │ ← База даних (структура + дані)
└────┬────┘
     │
┌────┴─────┐
│ Template │ ← HTML-шаблони
└────┬─────┘
     │
┌────┴────┐
│  View   │ ← Логіка обробки
└─────────┘
```

**Models відповідають за:**
- Структуру бази даних
- Збереження даних
- Зв'язки між таблицями
- Валідацію даних

## 3. Django ORM

### Що таке ORM?

**ORM (Object-Relational Mapping)** - технологія, яка дозволяє працювати з базою даних як з Python-об'єктами.

**Переваги ORM:**
✅ Не потрібно писати SQL
✅ Працюємо з об'єктами Python
✅ Автоматична генерація таблиць
✅ Незалежність від СУБД
✅ Захист від SQL-ін'єкцій

### Альтернативи Django ORM

| ORM | Особливості |
|-----|-------------|
| **Django ORM** | Вбудований у Django, тісна інтеграція |
| **SQLAlchemy** | Універсальний, працює з різними фреймворками |
| **Pydantic** | Для Fast API, валідація даних |

## 4. Створення моделі

### Базова структура

```python
# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(default=18)
    
    def __str__(self):
        return f"Student: {self.name}"
```

### Що відбувається під капотом?

**SQL-еквівалент:**
```sql
CREATE TABLE lesson1_student (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL DEFAULT 18
);
```

**ВАЖЛИВО:** 
- Назва таблиці: `{застосунок}_{модель}` (наприклад, `lesson1_student`)
- Множина: `student` → `students` (автоматично)
- `id` створюється автоматично

## 5. Типи полів

### Основні типи

```python
from django.db import models

class Product(models.Model):
    # Текстові поля
    name = models.CharField(max_length=100)  # Обмежена довжина
    description = models.TextField()          # Необмежений текст
    
    # Числові поля
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    rating = models.FloatField()
    
    # Дата та час
    created_at = models.DateTimeField(auto_now_add=True)  # При створенні
    updated_at = models.DateTimeField(auto_now=True)       # При оновленні
    
    # Логічні
    is_active = models.BooleanField(default=True)
    
    # Email
    email = models.EmailField()
```

### Параметри полів

| Параметр | Опис | Приклад |
|----------|------|---------|
| `max_length` | Максимальна довжина | `CharField(max_length=50)` |
| `default` | Значення за замовчуванням | `IntegerField(default=0)` |
| `null` | Дозволяє NULL у БД | `null=True` |
| `blank` | Дозволяє порожнє значення у формах | `blank=True` |
| `unique` | Унікальне значення | `unique=True` |
| `db_index` | Створює індекс | `db_index=True` |

### Choices (Обмежений вибір)

```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
```

## 6. Метаклас Meta

### Налаштування моделі

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'categories'              # Назва таблиці
        ordering = ['-created_at']           # Сортування за замовчуванням
        verbose_name = 'Категорія'           # Однина
        verbose_name_plural = 'Категорії'    # Множина
```

**Навіщо `verbose_name_plural`?**

```python
# Без налаштування:
country → countrys (неправильно!)

# З налаштуванням:
class Meta:
    verbose_name_plural = 'Countries'
```

## 7. Міграції (Migrations)

### Що таке міграції?

> **Міграції** - це система контролю версій для бази даних. Вони зберігають історію змін структури БД.

### Процес міграцій

```
┌──────────┐      ┌──────────────┐      ┌──────────┐
│ models.py│ ───► │  Migrations  │ ───► │ Database │
│  (код)   │      │   (файли)    │      │ (таблиці)│
└──────────┘      └──────────────┘      └──────────┘
     │                    │                    │
  Опис моделі      Журнал змін         Фізичні дані
```

### Команди міграцій

```bash
# 1. Створити міграцію (як "git commit")
python manage.py makemigrations

# 2. Застосувати міграції (як "git push")
python manage.py migrate

# 3. Переглянути SQL-код міграції
python manage.py sqlmigrate app_name 0001

# 4. Переглянути список міграцій
python manage.py showmigrations

# 5. Відкат до конкретної міграції
python manage.py migrate app_name 0001
```

### Структура файлу міграції

```python
# migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    
    dependencies = []  # Залежності від інших міграцій
    
    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('age', models.IntegerField(default=18)),
            ],
        ),
    ]
```

### Послідовність міграцій

```
0001_initial.py        ← Початкова (створення таблиць)
    ↓
0002_category.py       ← Додано таблицю Category
    ↓
0003_book.py          ← Додано таблицю Book зі зв'язками
    ↓
0004_add_manager.py   ← Додано кастомний менеджер
```

**Залежності:**
```python
dependencies = [
    ('lesson1', '0003_book'),  # Залежить від попередньої міграції
]
```

## 8. Зв'язки між моделями

### Типи зв'язків

#### 1. One-to-One (Один до одного)

**Приклад:** Користувач ↔ Профіль

```python
class User(models.Model):
    username = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
```

**Використання:**
- Паспортні дані
- Email (унікальний)
- Телефон (унікальний)

#### 2. Many-to-One (Багато до одного) - ForeignKey

**Приклад:** Багато книг → Одна категорія

```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return self.name
```

**Параметр `on_delete`:**

| Значення | Поведінка |
|----------|-----------|
| `CASCADE` | Видаляє всі пов'язані об'єкти |
| `PROTECT` | Забороняє видалення якщо є зв'язки |
| `SET_NULL` | Встановлює NULL (потрібно `null=True`) |
| `SET_DEFAULT` | Встановлює значення за замовчуванням |

**Приклади використання:**
- Товари → Категорія
- Коментарі → Користувач
- Замовлення → Клієнт
- Пости → Автор

#### 3. Many-to-Many (Багато до багатьох)

**Приклад:** Автори ↔ Книги

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
```

**Що створюється:**

Django автоматично створює проміжну таблицю:
```
book_authors (проміжна таблиця)
├── id
├── book_id      ← ForeignKey до Book
└── author_id    ← ForeignKey до Author
```

**Приклади використання:**
- Студенти ↔ Курси
- Товари ↔ Теги
- Користувачі ↔ Групи
- Букет ↔ Квіти

## 9. Адмін-панель

### Реєстрація моделі

```python
# admin.py
from django.contrib import admin
from .models import Student, Category, Book

# Варіант 1: Проста реєстрація
admin.site.register(Student)

# Варіант 2: З налаштуваннями
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)
```

### Магічний метод `__str__`

**❌ Без `__str__`:**
```
Student object (1)
Student object (2)
Student object (3)
```

**✅ З `__str__`:**
```python
def __str__(self):
    return f"{self.name}, {self.age} років"

# Результат:
John Doe, 25 років
Jane Smith, 22 роки
```

### Створення Superuser

```bash
python manage.py createsuperuser

# Вводимо:
# Username: admin
# Email: (можна пропустити)
# Password: ******** (мінімум 8 символів)
```

**ВАЖЛИВО:** Через термінал можна створити простий пароль (наприклад, `admin`), але через веб-форму буде валідація!

## 10. CRUD операції

### Create (Створення)

```python
# Варіант 1: create()
student = Student.objects.create(name="John", age=25)

# Варіант 2: save()
student = Student(name="John", age=25)
student.save()  # БЕЗ save() дані не збережуться!
```

**ВАЖЛИВО:** Без `.save()` дані тимчасові! Ліниві обчислення.

### Read (Читання)

```python
# Всі записи
students = Student.objects.all()

# Один запис
student = Student.objects.get(id=1)

# Фільтрація
students = Student.objects.filter(age__gte=18)  # age >= 18

# З сортуванням
students = Student.objects.filter(age__gte=18).order_by('-age')
```

### Оператори фільтрації

| Оператор | SQL | Приклад |
|----------|-----|---------|
| `field` | `=` | `name="John"` |
| `field__gt` | `>` | `age__gt=18` (age > 18) |
| `field__gte` | `>=` | `age__gte=18` (age >= 18) |
| `field__lt` | `<` | `price__lt=100` |
| `field__lte` | `<=` | `price__lte=100` |
| `field__startswith` | `LIKE 'text%'` | `name__startswith='J'` |
| `field__endswith` | `LIKE '%text'` | `name__endswith='son'` |
| `field__contains` | `LIKE '%text%'` | `name__contains='oh'` |
| `field__icontains` | `ILIKE '%text%'` | Без урахування регістру |
| `field__in` | `IN (...)` | `id__in=[1, 2, 3]` |
| `field__range` | `BETWEEN` | `age__range=(18, 30)` |

### Update (Оновлення)

```python
# Варіант 1: save()
student = Student.objects.get(id=1)
student.age = 26
student.save()

# Варіант 2: update() (масове)
Student.objects.filter(age__lt=18).update(age=18)
```

### Delete (Видалення)

```python
# Один запис
student = Student.objects.get(id=1)
student.delete()

# Масове видалення
Student.objects.filter(age__lt=18).delete()
```

## 11. Менеджери (Managers)

### Що таке менеджер?

> **Manager** - це інтерфейс для взаємодії з базою даних. За замовчуванням: `objects`.

### Використання

```python
Student.objects.all()      # objects - це менеджер
Book.objects.filter(...)
```

### Кастомний менеджер

```python
# managers.py
from django.db import models

class BookstoreManager(models.Model):
    def get_queryset(self):
        # Повертає тільки перші 10 книг
        return super().get_queryset()[:10]

# models.py
class Book(models.Model):
    name = models.CharField(max_length=200)
    
    objects = models.Manager()          # Стандартний
    bookstore = BookstoreManager()      # Кастомний
```

**Використання:**
```python
Book.objects.all()      # Всі книги
Book.bookstore.all()    # Тільки перші 10
```

**Чому виносити в окремий файл `managers.py`?**
- Якщо багато менеджерів (3+)
- Для повторного використання
- Чистота коду

## 12. Оптимізація запитів

### Проблема N+1 запитів

```python
# ❌ Погано - N+1 запитів
books = Book.objects.all()
for book in books:
    print(book.category.name)  # Кожен раз запит до БД!

# ✅ Добре - 1 запит
books = Book.objects.select_related('category').all()
for book in books:
    print(book.category.name)  # Без додаткових запитів
```

### `select_related()` vs `prefetch_related()`

| `select_related()` | `prefetch_related()` |
|--------------------|----------------------|
| ForeignKey, OneToOneField | ManyToManyField |
| SQL JOIN | Окремі запити + з'єднання в Python |
| 1 запит | 2+ запити |
| Швидше | Повільніше, але ефективніше для M2M |

**Приклади:**

```python
# ForeignKey - select_related()
books = Book.objects.select_related('category').all()

# ManyToManyField - prefetch_related()
authors = Author.objects.prefetch_related('books').all()
```

## 13. Налаштування бази даних

### SQLite (за замовчуванням)

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Переваги:** Простота, не потрібна установка
**Недоліки:** Не для продакшну, обмежені можливості

### PostgreSQL

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Установка драйвера:**
```bash
pip install psycopg2-binary
```

**Кроки переходу на PostgreSQL:**
1. Встановити PostgreSQL
2. Встановити pgAdmin (візуалізація)
3. Створити базу даних
4. Змінити `settings.py`
5. Встановити драйвер
6. Виконати міграції

### Кілька баз даних

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'postgres_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        # ...
    }
}
```

## 14. Типові помилки

### Помилка 1: Забули зробити міграції

```bash
# ❌ Помилка: таблиця не існує
# Рішення:
python manage.py makemigrations
python manage.py migrate
```

### Помилка 2: DoesNotExist

```python
# ❌ Помилка
student = Student.objects.get(id=999)  # DoesNotExist!

# ✅ Рішення
try:
    student = Student.objects.get(id=999)
except Student.DoesNotExist:
    student = None
```

### Помилка 3: Неспівпадіння структури

```
Проблема: В моделі є поле, але в БД немає (або навпаки)

Рішення:
1. Перевірити останню міграцію
2. Перевірити, чи застосована міграція (migrate)
3. Перевірити структуру БД
```

### Помилка 4: Забули `.save()`

```python
# ❌ Дані не збережуться!
student = Student(name="John", age=25)
# Забули student.save()

# ✅ Правильно
student = Student(name="John", age=25)
student.save()
```

## 15. Асинхронність та Django

### Синхронний характер Django

Django за замовчуванням **синхронний**. Це означає:
- Запити виконуються послідовно
- Може бути повільно для великих завантажень

### Рішення для асинхронності

1. **Django Ninja** - асинхронне розширення
2. **Fast API** - інтеграція з Django
3. **Celery** - черги завдань
4. **AJAX/jQuery** - асинхронні запити на фронтенді

### Приклад з AJAX

```javascript
// Оновлення лічильника без перезавантаження сторінки
$.ajax({
    url: '/api/update-counter/',
    method: 'POST',
    success: function(data) {
        $('#counter').text(data.count);
    }
});
```

## 16. Практичні поради

### Іменування

```python
# ✅ Добре
class User(models.Model):
    username = models.CharField(...)

# ❌ Погано
class user(models.Model):  # Клас з маленької літери
    UsErNaMe = models.CharField(...)  # Незрозуміло
```

### Організація файлів

```
myapp/
├── models.py          # Моделі
├── managers.py        # Кастомні менеджери (якщо багато)
├── admin.py           # Адмін-панель
├── views.py           # Представлення
└── migrations/        # Міграції (автоматично)
    ├── __init__.py
    ├── 0001_initial.py
    └── 0002_category.py
```

### Workflow роботи з моделями

```
1. Написати модель (models.py)
2. makemigrations
3. migrate
4. Зареєструвати в admin.py
5. Створити superuser
6. Тестувати в адмін-панелі
```

## Домашнє завдання

### Базове завдання

1. Створити 3 моделі:
   - `Student` (ім'я, вік, група)
   - `Course` (назва, опис)
   - `Enrollment` (студент, курс, дата запису)

2. Налаштувати зв'язки:
   - Student → Enrollment (One-to-Many)
   - Course → Enrollment (One-to-Many)

3. Зареєструвати в адмін-панелі
4. Додати 5 студентів та 3 курси
5. Зробити кілька записів

### Завдання з зірочкою ⭐

**Перенести проект на PostgreSQL:**

1. Встановити PostgreSQL
2. Встановити pgAdmin
3. Створити базу даних
4. Налаштувати `settings.py`
5. Встановити `psycopg2-binary`
6. Виконати міграції
7. Перевірити, що все працює

## Корисні посилання

- **Django Models:** https://docs.djangoproject.com/en/5.0/topics/db/models/
- **QuerySet API:** https://docs.djangoproject.com/en/5.0/ref/models/querysets/
- **Migrations:** https://docs.djangoproject.com/en/5.0/topics/migrations/
- **PostgreSQL:** https://www.postgresql.org/docs/

---

**Ключові висновки:**
- **Models** - структура та логіка роботи з БД
- **ORM** - робота з БД як з Python-об'єктами
- **Міграції** - система контролю версій БД
- **Зв'язки** - ForeignKey, ManyToMany, OneToOne
- **Менеджери** - інтерфейс взаємодії з БД
- **CRUD** - створення, читання, оновлення, видалення
- Завжди робити `.save()` після змін!
- Використовувати `select_related()` для оптимізації