# MinValueValidator(0.01)

### Це означає: **≥ 0.01** (більше або дорівнює 0.01)

```python
validators=[MinValueValidator(0.01)]

# ✅ Приймає:
price = 0.01  # OK
price = 1.00  # OK
price = 100.50  # OK

# ❌ Відхиляє:
price = 0.00  # Помилка! Менше 0.01
price = -10.00  # Помилка! Менше 0.01
```

---

## 📊 Порівняння валідаторів

### 1. **MinValueValidator(0.01)** - мінімум 0.01
```python
from django.core.validators import MinValueValidator

price = models.DecimalField(
    validators=[MinValueValidator(0.01)]
)

# ✅ 0.01, 0.02, 1.00, 100.00
# ❌ 0, 0.005, -1
```

### 2. **MinValueValidator(0)** - не може бути негативним
```python
price = models.DecimalField(
    validators=[MinValueValidator(0)]
)

# ✅ 0, 0.01, 1.00, 100.00
# ❌ -1, -0.01
```

### 3. **Якщо потрібно "строго більше 0"**
```python
from django.core.validators import MinValueValidator
from decimal import Decimal

price = models.DecimalField(
    validators=[MinValueValidator(Decimal('0.01'))]
)

# АБО через custom валідатор:
def validate_positive(value):
    if value <= 0:
        raise ValidationError('Ціна повинна бути більше нуля')

price = models.DecimalField(
    validators=[validate_positive]
)
```

---

## 🔍 подвійна валідація:

1. **MinValueValidator(0.01)** - на рівні поля
2. **clean() метод** - перевіряє `price <= 0`

---

```python
# ✅ ПРИЙМАЄ (валідні значення):
price = 0.01    # Мінімальна ціна
price = 1.00
price = 99.99
price = 10000.00

# ❌ ВІДХИЛЯЄ (невалідні значення):
price = 0       # Помилка! Менше 0.01
price = 0.005   # Помилка! Менше 0.01
price = -10     # Помилка! Менше 0.01
price = None    # Помилка! (якщо blank=False)
```

---

## 💡 Різні варіанти валідаторів

### Варіант 1: Тільки MinValueValidator
```python
price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[MinValueValidator(0.01)]
)
# Мінімум: 0.01
```

### Варіант 2: Діапазон значень
```python
from django.core.validators import MinValueValidator, MaxValueValidator

price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[
        MinValueValidator(0.01),    # Мінімум 0.01
        MaxValueValidator(1000000)  # Максимум 1,000,000
    ]
)
```

### Варіант 3: Custom валідатор
```python
from django.core.exceptions import ValidationError

def validate_price(value):
    if value <= 0:
        raise ValidationError('Ціна повинна бути строго більше нуля')
    if value > 1000000:
        raise ValidationError('Ціна не може перевищувати 1,000,000')

price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    validators=[validate_price]
)
```

### Варіант 4: Метод clean (на рівні моделі)
```python
class Ad(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def clean(self):
        if self.price <= 0:
            raise ValidationError('Ціна повинна бути додатною')
```

---

## 🧪 Тестування валідації

Створю приклад тесту:

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Ad, Category, User

class PriceValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        self.category = Category.objects.create(name='Test')
    
    def test_valid_price(self):
        """Тест валідної ціни"""
        ad = Ad(
            title='Test',
            description='Test',
            price=Decimal('10.00'),  # ✅ Валідно
            user=self.user,
            category=self.category
        )
        ad.full_clean()  # Не викине помилку
        ad.save()
        self.assertEqual(ad.price, Decimal('10.00'))
    
    def test_minimum_price(self):
        """Тест мінімальної ціни"""
        ad = Ad(
            title='Test',
            description='Test',
            price=Decimal('0.01'),  # ✅ Мінімум
            user=self.user,
            category=self.category
        )
        ad.full_clean()
        ad.save()
    
    def test_zero_price(self):
        """Тест нульової ціни"""
        ad = Ad(
            title='Test',
            description='Test',
            price=Decimal('0.00'),  # ❌ Невалідно
            user=self.user,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            ad.full_clean()
    
    def test_negative_price(self):
        """Тест від'ємної ціни"""
        ad = Ad(
            title='Test',
            description='Test',
            price=Decimal('-10.00'),  # ❌ Невалідно
            user=self.user,
            category=self.category
        )
        with self.assertRaises(ValidationError):
            ad.full_clean()
```

---

## 📋 Таблиця порівняння

| Значення | MinValueValidator(0.01) | MinValueValidator(0) | Метод clean (>0) |
|----------|------------------------|---------------------|------------------|
| -10.00   | ❌                     | ❌                  | ❌               |
| 0.00     | ❌                     | ✅                  | ❌               |
| 0.005    | ❌                     | ✅                  | ❌               |
| 0.01     | ✅                     | ✅                  | ✅               |
| 1.00     | ✅                     | ✅                  | ✅               |
| 100.00   | ✅                     | ✅                  | ✅               |


