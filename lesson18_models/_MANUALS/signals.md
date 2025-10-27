## 🎯 Що таке сигнали (Signals)?

**Сигнали** - це система **подій** в Django, яка дозволяє різним частинам програми спілкуватися між собою.

### Простими словами:

```
📢 Щось сталося (подія) → 🔔 Сигнал → 👂 Хтось почув → ⚡ Виконалась дія
```

**Приклад з життя:**
- 🔔 Дзвінок у двері (сигнал)
- 👂 Ви почули (receiver)
- ⚡ Відкрили двері (дія)

---

## 📡 Як працюють сигнали в Django?

### Схема:

```python
Модель User                Сигнал post_save          Функція-обробник
    │                           │                          │
    │ Створюється користувач    │                          │
    ├───────────────────────────►                          │
    │                           │                          │
    │                           │  "Користувач створений!" │
    │                           ├──────────────────────────►
    │                           │                          │
    │                           │          Створює профіль │
    │                           │          UserProfile     │
```

---

## 🔍 Приклад із вашого проєкту

Давайте подивимося на файл `signals.py`:## 📚 Розбір коду покроково

### Сигнал 1: Створення профілю

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

**Що відбувається:**
1. `@receiver` - декоратор, який "підписує" функцію на сигнал
2. `post_save` - сигнал "після збереження"
3. `sender=User` - реагуємо на збереження User
4. `created=True` - тільки якщо користувач НОВИЙ
5. → Створюємо профіль автоматично!

**Візуалізація:**
```
User.objects.create_user(username='ivan', password='pass')
          ↓
    [Користувач створений]
          ↓
    🔔 post_save сигнал
          ↓
    👂 create_user_profile() почула
          ↓
    ⚡ UserProfile.objects.create(user=ivan)
          ↓
    ✅ Профіль створено автоматично!
```

---

### Сигнал 2: Надсилання email

```python
@receiver(post_save, sender=Ad)
def send_ad_created_email(sender, instance, created, **kwargs):
    if created and instance.user.email:
        send_mail(...)
```

**Що відбувається:**
1. Коли створюється нове оголошення (`Ad`)
2. Автоматично надсилається email користувачу
3. Без додаткового коду у views!

**Візуалізація:**
```
Ad.objects.create(title='Продам iPhone', ...)
          ↓
    [Оголошення створене]
          ↓
    🔔 post_save сигнал
          ↓
    👂 send_ad_created_email() почула
          ↓
    ⚡ send_mail(...) надсилає листа
          ↓
    ✅ Email відправлено!
```

---

## 🔌 Підключення сигналів

### В `apps.py`  

```python
def ready(self):
    """Викликається коли застосунок готовий"""
    import board.signals  # ← ПІДКЛЮЧЕННЯ СИГНАЛІВ
```

**Що робить:**
1. Django запускає застосунок `board`
2. Викликає метод `ready()`
3. Імпортує `signals.py`
4. Реєструє всі `@receiver` декоратори
5. Тепер сигнали працюють! ✅

---

## 🎓 Види сигналів у Django

### 1. **Сигнали моделей**

```python
from django.db.models.signals import (
    pre_save,      # Перед збереженням
    post_save,     # Після збереження
    pre_delete,    # Перед видаленням
    post_delete,   # Після видалення
    m2m_changed,   # Зміна Many-to-Many
)
```

#### Приклад: `pre_save` vs `post_save`

```python
@receiver(pre_save, sender=Ad)
def before_save(sender, instance, **kwargs):
    print(f"Зараз збережеться: {instance.title}")
    # instance ще НЕ в базі даних

@receiver(post_save, sender=Ad)
def after_save(sender, instance, created, **kwargs):
    print(f"Збережено: {instance.title}")
    # instance вже В базі даних
    # created = True якщо новий запис
```

### 2. **Сигнали запитів (request/response)**

```python
from django.core.signals import (
    request_started,   # Початок обробки запиту
    request_finished,  # Кінець обробки запиту
)
```

### 3. **Сигнали підключення до БД**

```python
from django.db.backends.signals import (
    connection_created,  # Підключення до БД створене
)
```

---

## 💡 Практичні приклади

### Приклад 1: Логування змін

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Ad
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Ad)
def log_ad_saved(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Створено оголошення: {instance.title}")
    else:
        logger.info(f"Оновлено оголошення: {instance.title}")

@receiver(post_delete, sender=Ad)
def log_ad_deleted(sender, instance, **kwargs):
    logger.warning(f"Видалено оголошення: {instance.title}")
```

### Приклад 2: Автоматичний slug

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Category

@receiver(pre_save, sender=Category)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
```

### Приклад 3: Кеш-інвалідація

```python
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from .models import Ad

@receiver([post_save, post_delete], sender=Ad)
def clear_ads_cache(sender, instance, **kwargs):
    # Очищуємо кеш при зміні оголошень
    cache.delete('active_ads_list')
    cache.delete(f'category_{instance.category_id}_ads')
```

### Приклад 4: Сповіщення адміністратора

```python
from django.db.models.signals import post_save
from .models import Ad

@receiver(post_save, sender=Ad)
def notify_admin_new_ad(sender, instance, created, **kwargs):
    if created:
        # Надіслати Telegram повідомлення адміну
        send_telegram_message(
            f"Нове оголошення: {instance.title}\n"
            f"Автор: {instance.user.username}\n"
            f"Ціна: {instance.price}"
        )
```

---

## ⚠️ Важливі моменти

### 1. **Сигнали викликаються при `.save()`**

```python
# ✅ Сигнал спрацює
user = User.objects.create_user(username='ivan')

# ✅ Сигнал спрацює
user = User(username='maria')
user.save()

# ❌ Сигнал НЕ спрацює (bulk операція)
User.objects.bulk_create([
    User(username='ivan'),
    User(username='maria')
])

# ❌ Сигнал НЕ спрацює (update без save)
User.objects.filter(username='ivan').update(email='new@email.com')
```

### 2. **Уникайте рекурсії**

```python
# ❌ ПОГАНО - безкінечний цикл!
@receiver(post_save, sender=User)
def bad_signal(sender, instance, **kwargs):
    instance.last_modified = timezone.now()
    instance.save()  # ← Знову викличе post_save!

# ✅ ДОБРЕ - використовуємо update
@receiver(post_save, sender=User)
def good_signal(sender, instance, **kwargs):
    User.objects.filter(id=instance.id).update(
        last_modified=timezone.now()
    )
```

### 3. **Сигнали можуть сповільнити роботу**

```python
# ❌ ПОВІЛЬНО - якщо створюється 1000 користувачів
@receiver(post_save, sender=User)
def slow_signal(sender, instance, created, **kwargs):
    if created:
        time.sleep(1)  # Імітація повільної операції

# ✅ КРАЩЕ - використати Celery для асинхронних задач
@receiver(post_save, sender=User)
def fast_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.id)  # Celery task
```

---

## 🧪 Як перевірити, що сигнали працюють?

### Тест 1: Через shell

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from board.models import UserProfile

# Створюємо користувача
user = User.objects.create_user(username='test_signal', password='test')

# Перевіряємо чи є профіль
try:
    profile = user.profile
    print("✅ Сигнал спрацював! Профіль створено.")
    print(f"Профіль ID: {profile.id}")
except UserProfile.DoesNotExist:
    print("❌ Сигнал НЕ спрацював! Профіль не створено.")
```

### Тест 2: Через код

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin_board.settings')
django.setup()

from django.contrib.auth.models import User
from board.models import UserProfile

# Видаляємо старого тестового користувача
User.objects.filter(username='test_signal').delete()

# Створюємо нового
user = User.objects.create_user(username='test_signal', password='test')

# Перевіряємо
if UserProfile.objects.filter(user=user).exists():
    print("✅ Сигнали працюють!")
else:
    print("❌ Сигнали НЕ працюють!")
    print("Перевірте:")
    print("1. board/apps.py має метод ready() з import board.signals")
    print("2. board/__init__.py містить: default_app_config = 'board.apps.BoardConfig'")
    print("   АБО settings.py має: 'board.apps.BoardConfig' в INSTALLED_APPS")
```

---

## 📋 Чек-лист налаштування сигналів

- [ ] 1. Створити файл `signals.py`
- [ ] 2. Написати функції з декоратором `@receiver`
- [ ] 3. У `apps.py` додати метод `ready()` з `import board.signals`
- [ ] 4. У `settings.py` переконатися що застосунок у `INSTALLED_APPS`
- [ ] 5. Перезапустити сервер
- [ ] 6. Протестувати створення користувача

---

## ✅ Підсумок

**Що таке сигнали?**
- 📡 Система подій у Django
- 🔔 Автоматичні дії при певних подіях
- 🎯 Зменшують дублювання коду

**Навіщо потрібні?**
- ✅ Автоматичне створення профілів
- ✅ Надсилання email
- ✅ Логування змін
- ✅ Очищення кешу
- ✅ Сповіщення

