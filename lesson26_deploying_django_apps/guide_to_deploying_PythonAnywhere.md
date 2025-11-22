# Посібник з розгортання Django на PythonAnywhere

## Крок 1: Підготовка локального проєкту

### 1.1 Створення мінімального проєкту (якщо немає існуючого)

```bash
# Створіть та активуйте віртуальне середовище
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows

# Встановіть Django
pip install django

# Створіть проєкт
django-admin startproject myproject
cd myproject

# Створіть додаток
python manage.py startapp hello
```

### 1.2 Додайте просту view (hello/views.py)

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>Hello World from PythonAnywhere!</h1>")
```

### 1.3 Налаштуйте URLs (hello/urls.py - створіть файл)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

### 1.4 Підключіть додаток (myproject/urls.py)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hello.urls')),
]
```

### 1.5 Додайте додаток до INSTALLED_APPS (myproject/settings.py)

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hello',  # Додайте цей рядок
]
```

## Крок 2: Налаштування для продакшну

### 2.1 Відредагуйте settings.py

```python
# myproject/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# БЕЗПЕКА: Вимкніть DEBUG
DEBUG = False

# ВАЖЛИВО: Додайте ваш домен PythonAnywhere
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# Статичні файли
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Опціонально: додаткові директорії зі статичними файлами
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
```

### 2.2 Створіть requirements.txt

```bash
pip freeze > requirements.txt
```

Або створіть вручну з мінімальними залежностями:
```
Django==4.2.7
```

### 2.3 Ініціалізуйте Git репозиторій

```bash
git init
git add .
git commit -m "Initial commit"
```

### 2.4 Завантажте на GitHub

```bash
# Створіть новий репозиторій на GitHub, потім:
git remote add origin https://github.com/yourusername/your-repo.git
git branch -M main
git push -u origin main
```

## Крок 3: Налаштування на PythonAnywhere

### 3.1 Зареєструйтеся на PythonAnywhere

1. Перейдіть на https://www.pythonanywhere.com
2. Створіть безкоштовний аккаунт (Beginner)
3. Увійдіть в систему

### 3.2 Відкрийте Bash консоль

1. Натисніть на вкладку "Consoles"
2. Створіть нову "Bash" консоль

### 3.3 Клонуйте ваш репозиторій

```bash
# У Bash консолі PythonAnywhere:
cd ~
git clone https://github.com/OlBreeze/deploy_pyanywhere.git myproject
cd myproject
```

### 3.4 Створіть віртуальне середовище

```bash
# Створіть venv з Python 3.10 (або іншою версією)
#mkvirtualenv --python=/usr/bin/python3.10 myproject-venv
mkvirtualenv --python=/usr/bin/python3.13 myproject-venv
# Активуйте (якщо не активовано автоматично)
workon myproject-venv

# Встановіть залежності
pip install -r requirements.txt
```

### 3.5 Виконайте міграції

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Крок 4: Налаштування Web App

### 4.1 Створіть Web App

1. Перейдіть на вкладку "Web"
2. Натисніть "Add a new web app"
3. Виберіть "Manual configuration"
4. Виберіть Python версію (наприклад, Python 3.10)
5. Натисніть "Next"

### 4.2 Налаштуйте шляхи

У розділі "Code" на сторінці Web:

**Source code:**
```
/home/fmwmf/myproject
```

**Working directory:**
```
/home/fmwmf/myproject
```

**Virtualenv:**
```
/home/fmwmf/.virtualenvs/myproject-venv
```

### 4.3 Налаштуйте Static files

У розділі "Static files":

| URL | Directory |
|-----|-----------|
| /static/ | /home/fmwmf/myproject/staticfiles |

### 4.4 Відредагуйте WSGI файл

1. Натисніть на посилання WSGI configuration file
2. Видаліть весь існуючий код
3. Додайте наступний код:

```python
import os
import sys

# Додайте шлях до вашого проєкту
path = '/home/fmwmf/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

# Встановіть змінну середовища для settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

# Імпортуйте Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**ВАЖЛИВО:** Замініть `yourusername` на ваше ім'я користувача PythonAnywhere!

### 4.5 Перезавантажте застосунок

1. Поверніться на вкладку "Web"
2. Натисніть зелену кнопку "Reload yourusername.pythonanywhere.com"

## Крок 5: Перевірка

Відкрийте у браузері: `https://yourusername.pythonanywhere.com`

Ви повинні побачити "Hello World from PythonAnywhere!"

## Типові проблеми та їх вирішення

### Помилка 500: Internal Server Error

1. Перевірте Error log на вкладці Web
2. Переконайтеся, що ALLOWED_HOSTS містить ваш домен
3. Перевірте шляхи у WSGI файлі

### Статичні файли не завантажуються

1. Переконайтеся, що виконали `collectstatic`
2. Перевірте налаштування Static files на вкладці Web
3. Перевірте STATIC_ROOT у settings.py

### ModuleNotFoundError

1. Переконайтеся, що віртуальне середовище правильно налаштовано
2. Перевірте, що всі залежності встановлені: `pip list`
3. Перевірте шлях до проєкту у WSGI файлі

## Оновлення застосунку

```bash
# У Bash консолі PythonAnywhere:
cd ~/myproject
workon myproject-venv

# Отримайте останні зміни
git pull

# Встановіть нові залежності (якщо є)
pip install -r requirements.txt

# Виконайте міграції та collectstatic
python manage.py migrate
python manage.py collectstatic --noinput

# Перезавантажте застосунок через вкладку Web
```

## Корисні команди

```bash
# Перевірити версію Python
python --version

# Переглянути встановлені пакети
pip list

# Перевірити синтаксис settings.py
python manage.py check

# Відкрити Django shell
python manage.py shell

# Переглянути логи (у Bash консолі)
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Чек-лист перед розгортанням

- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS містить домен PythonAnywhere
- [ ] STATIC_ROOT налаштовано
- [ ] requirements.txt створено
- [ ] Код завантажено на GitHub
- [ ] Віртуальне середовище створено на PythonAnywhere
- [ ] Залежності встановлено
- [ ] Міграції виконано
- [ ] collectstatic виконано
- [ ] WSGI файл відредаговано
- [ ] Static files налаштовано у Web App
- [ ] Застосунок перезавантажено

Успіхів у розгортанні! 🚀

---
# Безпека секретного ключа

Налаштуйте змінну середовища DJANGO_SECRET_KEY на сторінці Web App на PythonAnywhere і змініть ваш settings.py так, 
щоб він зчитував SECRET_KEY саме з цієї змінної, а не зберігав його безпосередньо у коді.


Ваш SECRET_KEY знаходиться у файлі `settings.py` вашого Django проєкту! Давайте знайдемо його і налаштуємо безпечно.

## Крок 1: Знайдіть ваш поточний SECRET_KEY

### Варіант А: Через Bash консоль на PythonAnywhere

```bash
cd ~/myproject
cat myproject/settings.py | grep SECRET_KEY
```

Ви побачите щось на кшталт:
```python
SECRET_KEY = 'django-insecure-a8j2k_9sd@f#$lk3j4_sdk2j3k4@#$lksjdf_23j4k'
```

### Варіант Б: Через Files на PythonAnywhere

1. Перейдіть на вкладку **Files**
2. Відкрийте `/home/yourusername/myproject/myproject/settings.py`
3. Знайдіть рядок з `SECRET_KEY =`

### Варіант В: Локально на вашому комп'ютері

Відкрийте файл `myproject/settings.py` і знайдіть SECRET_KEY

---

## Крок 2: Згенеруйте новий SECRET_KEY (рекомендовано)

Краще створити новий ключ для продакшну! У Bash консолі PythonAnywhere:

```bash
cd ~/myproject
workon myproject-venv  # або source myproject-venv/bin/activate

# Згенеруйте новий ключ
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Скопіюйте** згенерований ключ (наприклад):
```
django-insecure-abc123xyz789!@#$%^&*()_+-=[]{}|:;"'<>,.?/~`
```

---

## Крок 3: Додайте SECRET_KEY у WSGI файл

1. **Відкрийте** вкладку **Web** на PythonAnywhere
2. **Натисніть** на посилання **WSGI configuration file** (наприклад, `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Додайте** змінну середовища **перед** імпортом Django:

```python
import os
import sys

# ============================================
# ДОДАЙТЕ ЦЕЙ РЯДОК з вашим новим SECRET_KEY
# ============================================
os.environ['DJANGO_SECRET_KEY'] = 'ваш-згенерований-ключ-тут'

# Додайте шлях до вашого проєкту
path = '/home/yourusername/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**ВАЖЛИВО:** Замініть:
- `yourusername` на ваше ім'я користувача
- `ваш-згенерований-ключ-тут` на ваш справжній SECRET_KEY

4. **Збережіть** файл (Ctrl+S або кнопка Save)

---

## Крок 4: Змініть settings.py

У вашому локальному проєкті відредагуйте `myproject/settings.py`:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# ЗМІНІТЬ ЦЕЙ РЯДОК
# ============================================
# Було:
# SECRET_KEY = 'django-insecure-старий-ключ'

# Стало:
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-key-for-local-development')

# Опціонально: додайте перевірку для продакшну
if not os.environ.get('DJANGO_SECRET_KEY') and not DEBUG:
    raise ValueError("DJANGO_SECRET_KEY environment variable must be set in production!")

DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

# ... решта налаштувань
```

---

## Крок 5: Закомітьте зміни (БЕЗ SECRET_KEY!)

```bash
# Локально:
git add myproject/settings.py
git commit -m "Use environment variable for SECRET_KEY"
git push origin main
```

**ВАЖЛИВО:** Перевірте, що у `settings.py` немає жорстко закодованого SECRET_KEY!

---

## Крок 6: Оновіть код на PythonAnywhere

```bash
# У Bash консолі PythonAnywhere:
cd ~/myproject
git pull
```

---

## Крок 7: Перезавантажте застосунок

1. Перейдіть на вкладку **Web**
2. Натисніть зелену кнопку **Reload yourusername.pythonanywhere.com**

---

## Крок 8: Перевірте, що все працює

Відкрийте ваш сайт у браузері. Якщо бачите вашу сторінку - все добре! ✅

### Якщо помилка:

Перегляньте **Error log** на вкладці Web:

```bash
# Або у консолі:
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

---

## Повний приклад WSGI файлу:

```python
import os
import sys

# Встановіть SECRET_KEY (замініть на ваш!)
os.environ['DJANGO_SECRET_KEY'] = 'django-insecure-abc123xyz789!@#$%^&*()_+-=[]{}|:;"'

# Додайте шлях до проєкту (замініть yourusername!)
path = '/home/yourusername/myproject'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## Що ви досягли? 🎉

✅ SECRET_KEY тепер **НЕ** у Git репозиторії  
✅ Ключ зберігається **безпечно** у WSGI файлі на сервері  
✅ Локально можете використовувати fallback ключ  
✅ Продакшн використовує окремий, безпечний ключ

---

**Питання:** Чи знайшли ви ваш SECRET_KEY? Напишіть перші 20 символів (не весь!), щоб я міг підтвердити, що це правильний ключ.