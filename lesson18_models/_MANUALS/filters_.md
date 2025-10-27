## 🔍 Як працюють фільтри - Повний розбір

---

## 📊 Загальна схема роботи

```
1. Користувач заповнює форму
   ↓
2. Натискає "Застосувати"
   ↓
3. Браузер відправляє GET запит з параметрами
   ↓
4. Django отримує параметри в request.GET
   ↓
5. views.py фільтрує QuerySet
   ↓
6. Повертає відфільтровані результати
   ↓
7. Шаблон відображає результати
```

---

## 🎯 Крок 1: Користувач заповнює форму

```html
<form method="get">
  <!--      ↑ GET метод - параметри в URL -->
  
  <input name="search" value="iPhone">
  <select name="category">
    <option value="1">Електроніка</option>
  </select>
  <input name="min_price" value="1000">
  <button type="submit">Застосувати</button>
</form>
```

---

## 🌐 Крок 2: Формується URL з параметрами

Після submit браузер формує URL:

```
http://127.0.0.1:8000/ads/?search=iPhone&category=1&min_price=1000
                         ↑
                    GET параметри
```

**Структура URL:**
```
/ads/?параметр1=значення1&параметр2=значення2
```

---

## 📥 Крок 3: Django отримує параметри

У `views.py`:

```python
def ad_list(request):
    # Django автоматично парсить URL параметри в request.GET
    
    print(request.GET)
    # <QueryDict: {'search': ['iPhone'], 'category': ['1'], 'min_price': ['1000']}>
    
    # Отримання окремих параметрів:
    search_query = request.GET.get('search')      # 'iPhone'
    category_id = request.GET.get('category')     # '1'
    min_price = request.GET.get('min_price')      # '1000'
```

---

## 🔍 Крок 4: Фільтрація QuerySet

### Базовий QuerySet (без фільтрів):

```python
ads = Ad.objects.filter(is_active=True)
# SQL: SELECT * FROM board_ad WHERE is_active = TRUE
```

### 🔎 Фільтр 1: Пошук за заголовком

```python
search_query = request.GET.get('search')  # 'iPhone'

if search_query:
    ads = ads.filter(title__icontains=search_query) # icontains - тип пошуку; i = insensitive (нечутливий до регістру); contains -  містить (LIKE у SQL)
    # SQL: WHERE title ILIKE '%iPhone%'
    #                ↑
    #          регістронезалежний пошук
```

**Приклад:**
```python
# Було: [iPhone 15, Samsung S24, MacBook, Toyota Camry]
# Після фільтру 'iPhone': [iPhone 15]
```

---

### 📁 Фільтр 2: За категорією

```python
category_id = request.GET.get('category')  # '1'

if category_id:
    ads = ads.filter(category_id=category_id)
    # SQL: WHERE category_id = 1
```

**Приклад:**
```python
# Було: [iPhone (Електроніка), Camry (Транспорт), MacBook (Електроніка)]
# Після фільтру category=1: [iPhone, MacBook]
```

---

### 💰 Фільтр 3: Мінімальна ціна

```python
min_price = request.GET.get('min_price')  # '1000'

if min_price:
    ads = ads.filter(price__gte=min_price)
    #                      ↑
    #    gte = Greater Than or Equal (>=)
    # SQL: WHERE price >= 1000
```

**Приклад:**
```python
# Було: [iPhone 42000грн, Велосипед 500грн, MacBook 48000грн]
# Після фільтру min_price=1000: [iPhone 42000, MacBook 48000]
```

---

### 💰 Фільтр 4: Максимальна ціна

```python
max_price = request.GET.get('max_price')  # '50000'

if max_price:
    ads = ads.filter(price__lte=max_price)
    #                      ↑
    #    lte = Less Than or Equal (<=)
    # SQL: WHERE price <= 50000
```

**Приклад:**
```python
# Було: [iPhone 42000, Camry 850000, MacBook 48000]
# Після фільтру max_price=50000: [iPhone 42000, MacBook 48000]
```

---

### 📊 Фільтр 5: Сортування

```python
sort_by = request.GET.get('sort', '-created_at')  # '-price'
#                                ↑
#                    default значення якщо параметр відсутній

allowed_sorts = ['price', '-price', 'created_at', '-created_at']

if sort_by in allowed_sorts:
    ads = ads.order_by(sort_by)
    #               ↑
    #         '-' означає DESC (від більшого до меншого)
    #    без '-' означає ASC (від меншого до більшого)
```

**Приклади:**
```python
# sort=price (зростання)
# SQL: ORDER BY price ASC
# [500грн, 1000грн, 42000грн, 850000грн]

# sort=-price (спадання)
# SQL: ORDER BY price DESC
# [850000грн, 42000грн, 1000грн, 500грн]

# sort=-created_at (нові спочатку)
# SQL: ORDER BY created_at DESC
# [2024-10-27, 2024-10-26, 2024-10-25]
```

---

## 🧩 Комбінування фільтрів

Django дозволяє **ланцюжково** застосовувати фільтри:

```python
ads = Ad.objects.filter(is_active=True)  # Крок 1

# Крок 2: Додаємо фільтр за категорією
if category_id:
    ads = ads.filter(category_id=category_id)
    # SQL: WHERE is_active = TRUE AND category_id = 1

# Крок 3: Додаємо пошук
if search_query:
    ads = ads.filter(title__icontains=search_query)
    # SQL: WHERE is_active = TRUE 
    #       AND category_id = 1 
    #       AND title ILIKE '%iPhone%'

# Крок 4: Додаємо ціновий діапазон
if min_price:
    ads = ads.filter(price__gte=min_price)
if max_price:
    ads = ads.filter(price__lte=max_price)
    # SQL: WHERE is_active = TRUE 
    #       AND category_id = 1 
    #       AND title ILIKE '%iPhone%'
    #       AND price >= 1000
    #       AND price <= 50000

# Крок 5: Сортуємо
ads = ads.order_by('-price')
# SQL: ... ORDER BY price DESC
```

---

## 🔄 Повний приклад

### URL з параметрами:
```
/ads/?search=phone&category=1&min_price=1000&max_price=50000&sort=-price
```

### Що відбувається у views.py:

```python
def ad_list(request):
    # Стартовий QuerySet
    ads = Ad.objects.filter(is_active=True)
    # SQL: SELECT * FROM board_ad WHERE is_active = TRUE
    # Результат: [iPhone, Samsung, MacBook, Велосипед, Camry, ...]
    
    # Фільтр: пошук
    search = request.GET.get('search')  # 'phone'
    if search:
        ads = ads.filter(title__icontains=search)
        # Результат: [iPhone, Samsung]
    
    # Фільтр: категорія
    category_id = request.GET.get('category')  # '1'
    if category_id:
        ads = ads.filter(category_id=category_id)
        # Результат: [iPhone, Samsung] (обидва в категорії Електроніка)
    
    # Фільтр: мін ціна
    min_price = request.GET.get('min_price')  # '1000'
    if min_price:
        ads = ads.filter(price__gte=min_price)
        # Результат: [iPhone 42000, Samsung 35000]
    
    # Фільтр: макс ціна
    max_price = request.GET.get('max_price')  # '50000'
    if max_price:
        ads = ads.filter(price__lte=max_price)
        # Результат: [iPhone 42000, Samsung 35000]
    
    # Сортування
    sort = request.GET.get('sort', '-created_at')  # '-price'
    ads = ads.order_by(sort)
    # Результат: [iPhone 42000, Samsung 35000] (від більшої ціни)
    
    return render(request, 'board/ad_list.html', {'ads': ads})
```

---

## 🎨 Крок 5: Збереження стану фільтрів у формі

Щоб після submit форма показувала вибрані значення:

### У формі:

```html
<!-- Пошук -->
<input name="search" value="{{ request.GET.search }}">
<!--                         ↑ Відновлює значення з URL -->

<!-- Категорія -->
<select name="category">
    <option value="">Всі</option>
    {% for category in categories %}
        <option value="{{ category.id }}" 
            {% if request.GET.category == category.id|stringformat:"d" %}selected{% endif %}>
            <!--  ↑ Якщо ID співпадає - робить selected -->
            {{ category.name }}
        </option>
    {% endfor %}
</select>

<!-- Ціна -->
<input name="min_price" value="{{ request.GET.min_price }}">
<input name="max_price" value="{{ request.GET.max_price }}">

<!-- Сортування -->
<select name="sort">
    <option value="-created_at" 
        {% if request.GET.sort == "-created_at" %}selected{% endif %}>
        Нові спочатку
    </option>
</select>
```

---

## 🔄 Django lookup типи

```python
# Точна відповідність
ads.filter(price=1000)          # WHERE price = 1000

# Більше/менше
ads.filter(price__gt=1000)      # WHERE price > 1000
ads.filter(price__gte=1000)     # WHERE price >= 1000
ads.filter(price__lt=1000)      # WHERE price < 1000
ads.filter(price__lte=1000)     # WHERE price <= 1000

# Пошук у тексті
ads.filter(title__contains='iPhone')      # WHERE title LIKE '%iPhone%'
ads.filter(title__icontains='iphone')     # WHERE title ILIKE '%iphone%' (без регістру)
ads.filter(title__startswith='iPhone')    # WHERE title LIKE 'iPhone%'
ads.filter(title__endswith='Pro')         # WHERE title LIKE '%Pro'
ads.filter(title__exact='iPhone 15')      # точна відповідність WHERE title = 'iPhone 15'
# iexact - точна відповідність БЕЗ регістру
# Діапазон
ads.filter(price__range=(1000, 50000))    # WHERE price BETWEEN 1000 AND 50000

# В списку
ads.filter(category_id__in=[1, 2, 3])     # WHERE category_id IN (1, 2, 3)

# Дата
ads.filter(created_at__date='2024-10-27') # Точна дата WHERE DATE(created_at) = '2024-10-27'
ads.filter(created_at__year=2024)         # WHERE YEAR(created_at) = 2024
ads.filter(created_at__month=10)
ads.filter(created_at__day=27)

# Діапазон дат
from datetime import datetime, timedelta

today = datetime.now()
week_ago = today - timedelta(days=7)

ads.filter(created_at__gte=week_ago)  # За останній тиждень
```

## 📖 Повний список Text Lookups

| Lookup | Опис | Регістр | SQL |
|--------|------|---------|-----|
| `exact` | Точна відповідність | ✅ Враховує | `= 'value'` |
| `iexact` | Точна відповідність | ❌ Ігнорує | `ILIKE 'value'` |
| `contains` | Містить | ✅ Враховує | `LIKE '%value%'` |
| `icontains` | Містить | ❌ Ігнорує | `ILIKE '%value%'` |
| `startswith` | Починається з | ✅ Враховує | `LIKE 'value%'` |
| `istartswith` | Починається з | ❌ Ігнорує | `ILIKE 'value%'` |
| `endswith` | Закінчується на | ✅ Враховує | `LIKE '%value'` |
| `iendswith` | Закінчується на | ❌ Ігнорує | `ILIKE '%value'` |
| `regex` | Регулярний вираз | ✅ Враховує | `REGEXP 'pattern'` |
| `iregex` | Регулярний вираз | ❌ Ігнорує | `REGEXP 'pattern'` |

---
## 🔗 Lookups для ForeignKey

```python
# За ID зв'язаного об'єкта
Ad.objects.filter(category_id=1)

# За полем зв'язаного об'єкта
Ad.objects.filter(category__name='Електроніка')
Ad.objects.filter(category__name__icontains='електр')

# Через кілька зв'язків
Ad.objects.filter(user__profile__phone_number__icontains='050')
#                  ↑      ↑         ↑
#                User → Profile → phone_number
```

---

## 📊 SQL який генерується

```python
# Python код:
ads = Ad.objects.filter(is_active=True) \
                .filter(category_id=1) \
                .filter(price__gte=1000) \
                .filter(price__lte=50000) \
                .order_by('-price')

# SQL який виконується:
SELECT * FROM board_ad 
WHERE is_active = TRUE 
  AND category_id = 1 
  AND price >= 1000 
  AND price <= 50000 
ORDER BY price DESC;
```

---

## ✅ Підсумок роботи фільтрів

| Крок | Що відбувається |
|------|-----------------|
| 1️⃣ | Користувач заповнює форму |
| 2️⃣ | Submit → URL з GET параметрами |
| 3️⃣ | Django отримує `request.GET` |
| 4️⃣ | `views.py` фільтрує QuerySet |
| 5️⃣ | Відфільтровані дані → template |
| 6️⃣ | Форма відновлює вибрані значення |

**Ключовий момент:** Кожен фільтр додається **послідовно** до QuerySet, створюючи один SQL запит з усіма умовами!

```python
ads = Ad.objects.all()              # Початок
ads = ads.filter(is_active=True)    # + умова 1
ads = ads.filter(category_id=1)     # + умова 2
ads = ads.filter(price__gte=1000)   # + умова 3
ads = ads.order_by('-price')        # + сортування
# Всі умови об'єднуються в ОДИН SQL запит!
```