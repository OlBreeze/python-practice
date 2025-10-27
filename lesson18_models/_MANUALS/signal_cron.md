
# автоматична деактивації через 30 днів
🎯 **Важливо:** Сигнал `post_save` сам по собі не запускається через 30 днів - 
потрібен зовнішній тригер (cron, celery або ручний запуск команди)!
---

## ✅ Що потрібно додати

Є **два підходи** для автоматичної деактивації:

### Підхід 1: Через Celery (кращий для продакшену)
Використовує асинхронні задачі

### Підхід 2: Через Django management команду + cron
Простіший, не потребує додаткових сервісів

**У проєкті вже є:** Management команда `deactivate_expired_ads.py` ✅

---

## 📝 Оновлений signals.py## ⚠️ Проблема з цим підходом

**Сигнал `post_save` спрацьовує ТІЛЬКИ коли:**
- Створюється нове оголошення
- Редагується існуюче оголошення

**НЕ спрацьовує:**
- Автоматично через 30 днів (якщо ніхто не редагує оголошення)

---

## 🎯 Кращі рішення для автоматичної деактивації

### ✅ Рішення 1: Management команда + Cron (РЕКОМЕНДОВАНО)

**У вас вже є команда:** `board/management/commands/deactivate_expired_ads.py`

#### Налаштування Windows Task Scheduler:

1. Відкрийте **Task Scheduler** (Планувальник завдань)
2. Create Basic Task
3. Name: "Deactivate Expired Ads"
4. Trigger: Daily, 3:00 AM
5. Action: Start a program
6. Program: `C:\Python\python.exe`
7. Arguments: `C:\path\to\project\manage.py deactivate_expired_ads`

#### Налаштування Linux Cron:

```bash
# Відкрийте crontab
crontab -e

# Додайте рядок (виконувати щодня о 3:00)
0 3 * * * cd /path/to/project && python manage.py deactivate_expired_ads
```

---

### ✅ Рішення 2: Celery Beat (для продакшену)

Встановіть Celery:
```bash
pip install celery redis
```---

### ✅ Рішення 3: Сигнал з перевіркою при кожному запиті (простіший)

Додати сигнал, який перевіряє при збереженні:---

## 📊 Порівняння підходів

| Підхід | Плюси | Мінуси | Складність |
|--------|-------|--------|------------|
| **Сигнал post_save** | Просто | Не працює автоматично | ⭐ |
| **Management команда + Cron** | Надійно, просто | Треба налаштувати cron | ⭐⭐ |
| **Celery Beat** | Професійно, гнучко | Потребує Redis/RabbitMQ | ⭐⭐⭐⭐ |

---

## 🎯 Рекомендація для вашого проєкту

### Варіант 1: Використати існуючу команду (найпростіше)

**Запускати вручну:**
```bash
python manage.py deactivate_expired_ads
```

**Або автоматично через Windows Task Scheduler:**
1. Створіть `.bat` файл:2. Налаштуйте Task Scheduler запускати цей файл щодня

---

### Варіант 2: Додати перевірку при перегляді оголошення

У `views.py`:

```python
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    
    # Перевірити чи не застаріле
    ad.deactivate_if_expired()
    ad.refresh_from_db()  # Оновити дані
    
    # Решта коду...
```

---

## 📋 Підсумок

### Що є зараз:
- ✅ Management команда `deactivate_expired_ads.py`
- ✅ Метод моделі `deactivate_if_expired()`
- ⚠️ **Відсутній:** автоматичний запуск

### Що додав:
1. ✅ Оновлений `signals.py` з сигналом деактивації → [signals_with_deactivation.py](computer:///mnt/user-data/outputs/signals_with_deactivation.py)
2. ✅ Приклад Celery задачі → [celery_tasks_example.py](computer:///mnt/user-data/outputs/celery_tasks_example.py)
3. ✅ Bat файл для Windows → [run_deactivation.bat](computer:///mnt/user-data/outputs/run_deactivation.bat)

### Рекомендація:
**Використовуйте Management команду + Task Scheduler/Cron** ⭐

Це найпростіше і найнадійніше рішення для вашого проєкту!

```bash
# Просто запускайте щодня:
python manage.py deactivate_expired_ads
```

