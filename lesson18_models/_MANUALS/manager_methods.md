**Manager = посередник між Моделлю та Базою даних** 🎯
## 🔍 Що таке Manager?

**Manager** - це інтерфейс для взаємодії з базою даних.

## 📚 `Ad.objects` - це Manager (Менеджер)

```python
Ad.objects
 ↑    ↑
 |    └─ Manager (менеджер)
 └────── Model (модель)
```
---

```python
class Ad(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField()
    
    objects = models.Manager()  # ← Менеджер (створюється автоматично)
```

---

## 🎯 Для чого потрібен?

Manager надає методи для роботи з БД:

```python
# Всі ці методи - це методи Manager
Ad.objects.all()           # Всі записи
Ad.objects.filter(...)     # Фільтрація
Ad.objects.get(id=1)       # Один запис
Ad.objects.create(...)     # Створити
Ad.objects.count()         # Підрахунок
Ad.objects.exists()        # Перевірка існування
```

---

## 📊 Структура

```python
# Модель
class Ad(models.Model):
    title = models.CharField()
    
    # Manager (за замовчуванням)
    objects = models.Manager()  ← ЦЕ МЕНЕДЖЕР

# Використання
Ad.objects.all()  # objects - це екземпляр Manager
    ↑
   Manager
```

---

## 🔧 За замовчуванням

Django **автоматично** створює менеджер `objects`:

```python
class Ad(models.Model):
    title = models.CharField()
    # objects створюється автоматично!

# Можна використовувати одразу:
Ad.objects.all()
```

---

## 🎨 Власний Manager

Можна створити власний:

```python
class ActiveAdsManager(models.Manager):
    """Менеджер тільки для активних оголошень"""
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Ad(models.Model):
    title = models.CharField()
    is_active = models.BooleanField(default=True)
    
    # Стандартний менеджер
    objects = models.Manager()
    
    # Власний менеджер
    active = ActiveAdsManager()

# Використання:
Ad.objects.all()      # Всі оголошення
Ad.active.all()       # Тільки активні
```

---

## 📋 Методи Manager

### Методи що повертають QuerySet:

```python
Ad.objects.all()                    # QuerySet всіх записів
Ad.objects.filter(price__gt=1000)   # QuerySet з фільтром
Ad.objects.exclude(is_active=False) # QuerySet без умови
Ad.objects.order_by('-created_at')  # QuerySet відсортований
```

### Методи що повертають об'єкт:

```python
Ad.objects.get(id=1)        # Один об'єкт Ad
Ad.objects.first()          # Перший запис
Ad.objects.last()           # Останній запис
```

### Методи що створюють:

```python
Ad.objects.create(title='...', price=1000)  # Створити і зберегти
Ad.objects.get_or_create(title='...')       # Знайти або створити
Ad.objects.bulk_create([...])               # Створити багато
```

### Методи що змінюють:

```python
Ad.objects.filter(id=1).update(price=2000)  # Оновити
Ad.objects.filter(id=1).delete()            # Видалити
```

### Методи агрегації:

```python
Ad.objects.count()                   # Кількість
Ad.objects.exists()                  # Чи є записи
Ad.objects.aggregate(Avg('price'))   # Середнє значення
Ad.objects.annotate(comments_count=Count('comments')) # см. ниже
#          ↑                ↑              ↑
#       метод          нове поле      що рахувати
```

---

## 🔄 Ланцюжок викликів

```python
Ad.objects                   # Manager
    .filter(is_active=True)  # QuerySet
    .filter(price__gt=1000)  # QuerySet
    .order_by('-price')      # QuerySet
    .select_related('user')  # QuerySet
    [:10]                    # QuerySet (обмеження)

# Все це - один Manager → QuerySet → QuerySet → ...
```

---

## ✅ Підсумок

```python
Ad.objects  ← ТАК, це Manager!
    ↑
   Надає інтерфейс для роботи з БД
```
---
**`````````````````````````````````````````````````````````````````**
---

## 🏷️ `.annotate()` - Додавання обчислених полів

---

## 🎯 Що таке `annotate()`?

**`annotate()`** - метод Manager/QuerySet, який **додає нові поля** до кожного об'єкта в результаті запиту.

```python
Ad.objects.annotate(comments_count=Count('comments'))
#          ↑                ↑              ↑
#       метод          нове поле      що рахувати
```

---

## 📊 Простий приклад

### Без annotate:
```python
ads = Ad.objects.all()

for ad in ads:
    # Для кожного оголошення окремий запит до БД! ❌
    comments_count = ad.comments.count()
    print(f"{ad.title}: {comments_count} коментарів")

# Проблема: N+1 запитів (повільно!)
```

### З annotate:
```python
ads = Ad.objects.annotate(comments_count=Count('comments'))

for ad in ads:
    # Все в одному запиті! ✅
    print(f"{ad.title}: {ad.comments_count} коментарів")
    #                       ↑
    #               нове поле, додане через annotate
```

---

## 🔍 Як це працює?

### Python код:
```python
ads = Ad.objects.annotate(comments_count=Count('comments'))
```

### SQL який генерується:
```sql
SELECT 
    board_ad.*,
    COUNT(board_comment.id) AS comments_count  ← Додаткове поле
FROM board_ad
LEFT JOIN board_comment ON board_comment.ad_id = board_ad.id
GROUP BY board_ad.id
```

### Результат:
```python
# Кожен об'єкт Ad тепер має додаткове поле:
for ad in ads:
    print(ad.id)              # Звичайне поле моделі
    print(ad.title)           # Звичайне поле моделі
    print(ad.comments_count)  # ← НОВЕ поле з annotate
```

---

## 📚 Функції агрегації

### `Count` - підрахунок

```python
from django.db.models import Count

# Кількість коментарів
Ad.objects.annotate(comments_count=Count('comments'))

# Кількість активних оголошень у категорії
Category.objects.annotate(
    active_ads=Count('ads', filter=Q(ads__is_active=True))
)
```

### `Avg` - середнє значення

```python
from django.db.models import Avg

# Середня ціна оголошень у кожній категорії
Category.objects.annotate(avg_price=Avg('ads__price'))

for cat in categories:
    print(f"{cat.name}: середня ціна {cat.avg_price} грн")
```

### `Sum` - сума

```python
from django.db.models import Sum

# Загальна вартість всіх оголошень користувача
User.objects.annotate(total_value=Sum('ads__price'))

for user in users:
    print(f"{user.username}: {user.total_value} грн")
```

### `Max` і `Min` - максимум/мінімум

```python
from django.db.models import Max, Min

# Найдорожче і найдешевше оголошення в категорії
Category.objects.annotate(
    max_price=Max('ads__price'),
    min_price=Min('ads__price')
)

for cat in categories:
    print(f"{cat.name}: від {cat.min_price} до {cat.max_price} грн")
```

---

## 🎨 Складні приклади

### Приклад 1: Кілька анотацій

```python
Category.objects.annotate(
    total_ads=Count('ads'),                                    # Всього
    active_ads=Count('ads', filter=Q(ads__is_active=True)),   # Активних
    avg_price=Avg('ads__price'),                              # Середня ціна
    max_price=Max('ads__price'),                              # Макс ціна
    min_price=Min('ads__price')                               # Мін ціна
)

for cat in categories:
    print(f"""
    {cat.name}:
        Всього: {cat.total_ads}
        Активних: {cat.active_ads}
        Середня: {cat.avg_price:.2f} грн
        Від {cat.min_price} до {cat.max_price} грн
    """)
```

### Приклад 2: З фільтром

```python
from django.db.models import Q

# Тільки активні оголошення
Category.objects.annotate(
    active_count=Count('ads', filter=Q(ads__is_active=True))
)
```

### Приклад 3: З умовою Case/When

```python
from django.db.models import Case, When, IntegerField

Ad.objects.annotate(
    price_category=Case(
        When(price__lt=1000, then=1),      # Дешеві
        When(price__lt=10000, then=2),     # Середні
        default=3,                          # Дорогі
        output_field=IntegerField()
    )
)

for ad in ads:
    categories = {1: 'Дешеве', 2: 'Середнє', 3: 'Дороге'}
    print(f"{ad.title}: {categories[ad.price_category]}")
```

---

## 🔄 `annotate()` vs `aggregate()`

### `annotate()` - додає поле до КОЖНОГО об'єкта

```python
# Повертає QuerySet з новими полями
ads = Ad.objects.annotate(comments_count=Count('comments'))

for ad in ads:  # Можна ітерувати
    print(ad.title, ad.comments_count)
```

### `aggregate()` - повертає загальну статистику

```python
# Повертає словник з одним результатом
stats = Ad.objects.aggregate(
    total=Count('id'),
    avg_price=Avg('price')
)

print(stats)  # {'total': 100, 'avg_price': 15000.50}
# Це НЕ QuerySet, не можна ітерувати!
```

---

## 📊 Візуальне порівняння

### annotate():
```python
Category.objects.annotate(ads_count=Count('ads'))

# Результат:
[
    Category(id=1, name='Електроніка', ads_count=25),  ← кожен має поле
    Category(id=2, name='Транспорт', ads_count=15),    ← кожен має поле
    Category(id=3, name='Нерухомість', ads_count=8)    ← кожен має поле
]
```

### aggregate():
```python
Category.objects.aggregate(total_ads=Count('ads'))

# Результат:
{'total_ads': 48}  ← один словник для всіх
```

---

## 🎯 Практичні приклади з проєкту

### 1. Оголошення з коментарями

```python
# queries.py
def get_ads_with_comments_count():
    return Ad.objects.annotate(
        comments_count=Count('comments')
    ).order_by('-comments_count')

# Використання:
ads = get_ads_with_comments_count()
for ad in ads:
    print(f"{ad.title}: {ad.comments_count} коментарів")
```

### 2. Категорії зі статистикою

```python
def get_categories_with_stats():
    return Category.objects.annotate(
        total_ads=Count('ads'),
        active_ads=Count('ads', filter=Q(ads__is_active=True)),
        avg_price=Avg('ads__price')
    )

# Використання:
categories = get_categories_with_stats()
for cat in categories:
    print(f"{cat.name}:")
    print(f"  Всього: {cat.total_ads}")
    print(f"  Активних: {cat.active_ads}")
    print(f"  Середня ціна: {cat.avg_price:.2f}")
```

### 3. Користувачі з кількістю оголошень

```python
from django.contrib.auth.models import User

users = User.objects.annotate(
    ads_count=Count('ads'),
    active_ads=Count('ads', filter=Q(ads__is_active=True))
)

for user in users:
    print(f"{user.username}: {user.ads_count} оголошень")
```

---

## 🔍 SQL під капотом

### Python:
```python
Ad.objects.annotate(comments_count=Count('comments'))
```

### SQL:
```sql
SELECT 
    board_ad.id,
    board_ad.title,
    board_ad.price,
    board_ad.description,
    COUNT(board_comment.id) AS comments_count
FROM board_ad
LEFT OUTER JOIN board_comment 
    ON board_comment.ad_id = board_ad.id
GROUP BY board_ad.id
```

---

## ⚡ Продуктивність

### ❌ Повільно (N+1 запитів):
```python
ads = Ad.objects.all()  # 1 запит

for ad in ads:
    count = ad.comments.count()  # +N запитів (по одному на кожне ad)
    print(f"{ad.title}: {count}")

# Всього: 1 + N запитів до БД
```

### ✅ Швидко (1 запит):
```python
ads = Ad.objects.annotate(
    comments_count=Count('comments')
)  # 1 запит з JOIN

for ad in ads:
    print(f"{ad.title}: {ad.comments_count}")  # Без запитів!

# Всього: 1 запит до БД
```

---

## 📋 Методи Manager з annotate

```python
Ad.objects
    .filter(is_active=True)           # Фільтр
    .annotate(comments_count=Count('comments'))  # Додати поле
    .order_by('-comments_count')      # Сортувати по новому полю
    .select_related('category')       # Оптимізація
    [:10]                             # Обмеження
```

---

## ✅ Підсумок

**`annotate()`** - це:

```python
Ad.objects.annotate(new_field=...)
           ↑
   Додає нове обчислене поле до кожного об'єкта
```

| Характеристика | Опис |
|----------------|------|
| **Що робить** | Додає нові поля до об'єктів |
| **Повертає** | QuerySet з новими полями |
| **Запити** | 1 SQL запит (з JOIN/GROUP BY) |
| **Використання** | Агрегація даних, статистика |
| **Функції** | Count, Sum, Avg, Max, Min, Case... |

**Головне:** Annotate додає поля до **кожного** об'єкта, aggregate - одне значення для **всіх**! 🎯
