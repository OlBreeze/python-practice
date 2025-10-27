## 📧 Як працює сигнал надсилання email

### 1️⃣ У `signals.py`:

```python
@receiver(post_save, sender=Ad)
def send_ad_created_email(sender, instance, created, **kwargs):
    """Надсилає email при створенні нового оголошення"""
    if created and instance.user.email:  # ← Тільки якщо НОВЕ і є email
        subject = f'Ваше оголошення "{instance.title}" створено'
        message = f"""
        Вітаємо, {instance.user.username}!
        
        Ваше оголошення "{instance.title}" успішно створено.
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=True,
        )
```

---

## 🔄 Потік роботи:

```
1. Користувач створює оголошення
   ↓
2. Ad.objects.create(...) або ad.save()
   ↓
3. 🔔 Django викликає сигнал post_save
   ↓
4. 👂 Функція send_ad_created_email() "чує" сигнал
   ↓
5. ✅ Перевірка: created=True? (нове оголошення)
   ✅ Перевірка: user.email існує?
   ↓
6. 📧 send_mail() надсилає листа
   ↓
7. ✅ Користувач отримує email
```

---

## 📝 Параметри функції:

```python
def send_ad_created_email(sender, instance, created, **kwargs):
    #                      ↑       ↑         ↑
    #                      |       |         |
    #              Клас Ad  |   True/False  |
    #                    Об'єкт оголошення  |
    #                              Чи нове оголошення?
```

- **`sender`** = `Ad` (клас моделі)
- **`instance`** = конкретне оголошення (об'єкт)
- **`created`** = `True` якщо нове, `False` якщо оновлення

---

## ⚙️ Налаштування email у `settings.py`:

```python
# Для розробки (ВИВОДИТЬ В КОНСОЛЬ!!!!)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# АБО для продакшену (Gmail):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

---

## 🧪 Як перевірити:

```bash
python manage.py shell
```

```python
from board.models import Ad, Category
from django.contrib.auth.models import User

user = User.objects.get(username='ivan')
category = Category.objects.first()

# Створюємо оголошення
ad = Ad.objects.create(
    title='Тестове оголошення',
    description='Опис',
    price=1000,
    user=user,
    category=category
)

# 🔔 Сигнал спрацює автоматично!
# 📧 Email виведеться в консоль (якщо console backend)
```

---

## ✅ Короткий підсумок:

1. **Сигнал підключений** ✅ (`apps.py` → `from . import signals`)
2. **Спрацьовує автоматично** ✅ (при `Ad.objects.create()`)
3. **Перевіряє умови** ✅ (`created=True` + `email` існує)
4. **Надсилає листа** ✅ (через `send_mail()`)

**Зараз працює з `console` backend** - листи виводяться в консоль Django, а не реально надсилаються.