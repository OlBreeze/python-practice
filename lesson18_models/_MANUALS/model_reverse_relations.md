🎯 магія Django ORM і **зворотних зв'язків** (reverse relations)! 

## 🔗 Звідки `self.ads`?  in ` return self.ads.filter(is_active=True).count()` 

Подивімося на модель `Ad`:

```python
class Ad(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='ads',  # ← ОСЬ КЛЮЧ!
        verbose_name='Категорія'
    )
```

### Що відбувається:

1. **Пряме посилання** (`Ad → Category`):
   ```python
   ad = Ad.objects.get(id=1)
   category = ad.category  # Отримуємо категорію оголошення
   ```

2. **Зворотне посилання** (`Category → Ad`):
   ```python
   category = Category.objects.get(id=1)
   ads = category.ads.all()  # Отримуємо всі оголошення категорії
   ```

---

## 📊 Візуальне пояснення

```
┌──────────────┐                    ┌───────────────┐
│  Category    │                    │      Ad       │
├──────────────┤                    ├───────────────┤
│ id = 1       │◄───────────────────│ id = 1        │
│ name = "Авто"│   category_id = 1  │ title = "BMW" │
└──────────────┘                    ├───────────────┤
      ▲                             │ id = 2        │
      │                             │ title = "Audi"│
      │         category_id = 1     └───────────────┘
      │
      └── category.ads.all() поверне обидва оголошення
```

---
Django автоматично створює зворотне посилання: `category.ad_set.all()`

```python
category = Category.objects.get(id=1)
ads = category.ad_set.all()  # За замовчуванням: modelname_set
```

### З `related_name='ads'`:
```python
class Ad(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='ads'  # Задаємо своє ім'я
    )
```

Тепер використовуємо кастомне ім'я:
```python
category = Category.objects.get(id=1)
ads = category.ads.all()  # Зручніше!
```

---

## 📚 Всі зворотні зв'язки в проєкті

### 1. Category → Ad
```python
category = Category.objects.get(id=1)
category.ads.all()  # Всі оголошення категорії
category.ads.filter(is_active=True)  # Тільки активні
category.ads.count()  # Кількість оголошень
```

### 2. User → Ad
```python
user = User.objects.get(id=1)
user.ads.all()  # Всі оголошення користувача
user.ads.filter(is_active=True)  # Тільки активні
```

### 3. User → Comment
```python
user = User.objects.get(id=1)
user.comments.all()  # Всі коментарі користувача
```

### 4. Ad → Comment
```python
ad = Ad.objects.get(id=1)
ad.comments.all()  # Всі коментарі до оголошення
ad.comments.count()  # Кількість коментарів
```

### 5. User → UserProfile
```python
user = User.objects.get(id=1)
user.profile  # Профіль користувача (OneToOne, без .all())
user.profile.phone_number  # Телефон
```

---

## 💡 Практичні приклади

### Приклад 1: Підрахунок
```python
# В моделі Category
def get_active_ads_count(self):
    return self.ads.filter(is_active=True).count()

# Використання
category = Category.objects.get(name='Електроніка')
count = category.get_active_ads_count()
print(f"Активних оголошень: {count}")
```

### Приклад 2: Видалення
```python
category = Category.objects.get(id=1)
category.ads.all().delete()  # Видалить всі оголошення категорії
```

### Приклад 3: Оновлення
```python
category = Category.objects.get(id=1)
category.ads.filter(price__lt=100).update(is_active=False)
# Деактивує дешеві оголошення
```

---

## 🔄 Схема всіх зв'язків

```python
User
 │
 ├─ user.ads  (related_name='ads')
 │   └─ Ad.user = ForeignKey(User, related_name='ads')
 │
 ├─ user.comments  (related_name='comments')
 │   └─ Comment.user = ForeignKey(User, related_name='comments')
 │
 └─ user.profile  (related_name='profile')
     └─ UserProfile.user = OneToOneField(User, related_name='profile')

Category
 │
 └─ category.ads  (related_name='ads')
     └─ Ad.category = ForeignKey(Category, related_name='ads')

Ad
 │
 └─ ad.comments  (related_name='comments')
     └─ Comment.ad = ForeignKey(Ad, related_name='comments')
```

---

## ✅ Підсумок

**Питання:** Звідки `self.ads` в Category?

**Відповідь:** З `related_name='ads'` в моделі Ad:

```python
class Ad(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='ads'  # ← Створює category.ads
    )
```

Django автоматично створює **зворотний зв'язок** від Category до Ad через це поле!