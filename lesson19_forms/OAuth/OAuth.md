# 🔐 НАЛАШТУВАННЯ OAuth АВТЕНТИФІКАЦІЇ

## Google та Facebook Login через django-allauth

---

## 📋 ЗМІСТ

1. [Що встановлено](#що-встановлено)
2. [Налаштування Google OAuth](#налаштування-google-oauth)
3. [Налаштування Facebook OAuth](#налаштування-facebook-oauth)
4. [Адміністрування в Django](#адміністрування-в-django)
5. [Тестування](#тестування)
6. [Troubleshooting](#troubleshooting)

---

## 📦 Що встановлено
```bash

  cd /home/claude/user_management && pip install django-allauth --break-system-packages

```
### Бібліотека
```bash
django-allauth==65.12.1
```

### Додані додатки в INSTALLED_APPS (см. settings.py):
- `django.contrib.sites`
- `allauth`
- `allauth.account`
- `allauth.socialaccount`
- `allauth.socialaccount.providers.google`
- `allauth.socialaccount.providers.facebook`

# URLs

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),  # OAuth URLs
    path('', RedirectView.as_view(url='/accounts/register/', permanent=False)),
]
```
### Кнопки OAuth додані:
- ✅ Сторінка входу (`/accounts/login/`)
- ✅ Сторінка реєстрації (`/accounts/register/`)
```HTML
                <!-- OAuth кнопки -->
                <div class="d-grid gap-2 mb-4">
                    <a href="{% provider_login_url 'google' %}" class="btn btn-outline-danger">
                        <i class="bi bi-google"></i> Увійти через Google
                    </a>
                    <a href="{% provider_login_url 'facebook' %}" class="btn btn-outline-primary">
                        <i class="bi bi-facebook"></i> Увійти через Facebook
                    </a>
                </div>
                
                <div class="text-center mb-3">
                    <span class="text-muted">або</span>
                </div>

------
                <!-- OAuth кнопки -->
                <div class="d-grid gap-2 mb-4">
                    <a href="{% provider_login_url 'google' %}" class="btn btn-outline-danger">
                        <i class="bi bi-google"></i> Зареєструватися через Google
                    </a>
                    <a href="{% provider_login_url 'facebook' %}" class="btn btn-outline-primary">
                        <i class="bi bi-facebook"></i> Зареєструватися через Facebook
                    </a>
                </div>
                
                <div class="text-center mb-3">
                    <span class="text-muted">або</span>
                </div>
```
---
### Тепер виконаємо міграції для allauth:
```bash

  cd /home/claude/user_management && python manage.py migrate

```
## 🔑 Налаштування Google OAuth

### Крок 1: Створення проекту в Google Cloud Console

1. **Відкрийте Google Cloud Console**
   - URL: https://console.cloud.google.com/

2. **Створіть новий проект**
   - Натисніть "Select a project" → "New Project"
   - Ім'я: "User Management System"
   - Натисніть "Create"

3. **Активуйте Google+ API**
   - Перейдіть: APIs & Services → Library
   - Знайдіть "Google+ API"
   - Натисніть "Enable"

### Крок 2: Створення OAuth 2.0 Credentials

1. **Налаштуйте OAuth consent screen**
   - Перейдіть: APIs & Services → OAuth consent screen
   - User Type: **External**
   - App name: "User Management System"
   - User support email: ваш email
   - Developer contact: ваш email
   - Натисніть "Save and Continue"

2. **Додайте Scopes**
   - Add or Remove Scopes
   - Виберіть:
     - `/auth/userinfo.email`
     - `/auth/userinfo.profile`
   - Натисніть "Update" → "Save and Continue"

3. **Додайте Test Users** (для розробки)
   - Add Users: додайте свої email для тестування
   - Натисніть "Save and Continue"

4. **Створіть Credentials**
   - Перейдіть: APIs & Services → Credentials
   - Натисніть "+ CREATE CREDENTIALS" → "OAuth client ID"
   - Application type: **Web application**
   - Name: "Django App"
   
   **Authorized JavaScript origins:**
   ```
   http://localhost:8000
   http://127.0.0.1:8000
   ```
   
   **Authorized redirect URIs:**
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
   
   - Натисніть "Create"

5. **Скопіюйте дані**
   - **Client ID**: довгий рядок типу `123456789-abc...apps.googleusercontent.com`
   - **Client Secret**: короткий рядок типу `GOCSPX-...`

### Крок 3: Додавання в Django

#### Варіант A: Через settings.py (не рекомендується для продакшн)

```python
# В settings.py
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'ВАШ_CLIENT_ID_ТУТ',
            'secret': 'ВАШ_SECRET_ТУТ',
            'key': ''
        }
    }
}
```

#### Варіант B: Через Django Admin (рекомендується) ⭐

1. Запустіть сервер: `python manage.py runserver`
2. Відкрийте: http://127.0.0.1:8000/admin/
3. Перейдіть: **Social applications** → **Add social application**
4. Заповніть:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: [ваш Client ID]
   - **Secret key**: [ваш Secret]
   - **Sites**: виберіть "example.com" (перемістіть з Available sites до Chosen sites)
5. Натисніть "Save"

---

## 👥 Налаштування Facebook OAuth

### Крок 1: Створення Facebook App

1. **Відкрийте Facebook Developers**
   - URL: https://developers.facebook.com/

2. **Створіть App**
   - Натисніть "My Apps" → "Create App"
   - Use case: **Authenticate and request data from users with Facebook Login**
   - App type: **Consumer**
   - Натисніть "Next"

3. **Налаштуйте App**
   - App display name: "User Management"
   - App contact email: ваш email
   - Натисніть "Create App"

### Крок 2: Налаштування Facebook Login

1. **Додайте Facebook Login**
   - В Dashboard знайдіть "Facebook Login"
   - Натисніть "Set Up"
   - Виберіть platform: **Web**

2. **Site URL:**
   ```
   http://localhost:8000
   ```

3. **Налаштування OAuth**
   - Перейдіть: Settings → Basic
   - Скопіюйте:
     - **App ID**: число типу `123456789`
     - **App Secret**: рядок (натисніть "Show")

4. **Valid OAuth Redirect URIs**
   - Перейдіть: Facebook Login → Settings
   - В полі "Valid OAuth Redirect URIs" додайте:
   ```
   http://localhost:8000/accounts/facebook/login/callback/
   http://127.0.0.1:8000/accounts/facebook/login/callback/
   ```
   - Натисніть "Save Changes"

### Крок 3: Додавання в Django

#### Через Django Admin (рекомендується) ⭐

1. Відкрийте: http://127.0.0.1:8000/admin/
2. Перейдіть: **Social applications** → **Add social application**
3. Заповніть:
   - **Provider**: Facebook
   - **Name**: Facebook OAuth
   - **Client id**: [ваш App ID]
   - **Secret key**: [ваш App Secret]
   - **Sites**: виберіть "example.com"
4. Натисніть "Save"

---

## 🖥️ Адміністрування в Django

### Налаштування Sites

1. Відкрийте Django Admin: http://127.0.0.1:8000/admin/
2. Перейдіть: **Sites**
3. Редагуйте "example.com":
   - **Domain name**: `localhost:8000` (або ваш домен)
   - **Display name**: `User Management System`
4. Натисніть "Save"

### Перегляд Social Accounts

- **Social applications**: Налаштування Google/Facebook
- **Social accounts**: Прив'язані соціальні акаунти користувачів
- **Email addresses**: Email адреси користувачів

---

## 🧪 Тестування

### 1. Перевірка кнопок

```bash
python manage.py runserver
```

Відкрийте:
- http://127.0.0.1:8000/accounts/login/
- http://127.0.0.1:8000/accounts/register/

Ви повинні побачити кнопки:
- "Увійти через Google" (червона)
- "Увійти через Facebook" (синя)

### 2. Тестування Google OAuth

1. Натисніть "Увійти через Google"
2. Виберіть Google акаунт
3. Дайте дозволи
4. Ви маєте автоматично увійти в систему
5. Перевірте що створився профіль

### 3. Тестування Facebook OAuth

1. Натисніть "Увійти через Facebook"
2. Введіть логін/пароль Facebook
3. Дайте дозволи
4. Ви маєте автоматично увійти
5. Перевірте що створився профіль

### 4. Перевірка в Admin

```bash
# Django shell
python manage.py shell

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

# Список всіх користувачів
User.objects.all()

# Користувачі з соціальних мереж
SocialAccount.objects.all()

# Дізнатися через що увійшов користувач
user = User.objects.get(username='john')
social = SocialAccount.objects.filter(user=user)
for s in social:
    print(f"Provider: {s.provider}, UID: {s.uid}")
```

---

## ❌ Troubleshooting

### Помилка: "redirect_uri_mismatch"

**Проблема:** URL перенаправлення не співпадає

**Рішення:**
1. Перевірте що в Google/Facebook додані:
   ```
   http://localhost:8000/accounts/google/login/callback/
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
2. Переконайтесь що немає зайвих слешів в кінці
3. Використовуйте саме `http` (не `https`) для localhost

### Помилка: "Access blocked: This app's request is invalid"

**Проблема:** App не налаштований правильно

**Рішення для Google:**
1. Перевірте OAuth consent screen
2. Додайте свій email до Test Users
3. Переконайтесь що API активовано

### Помилка: "Can't Load URL"

**Проблема:** Facebook не може завантажити redirect URL

**Рішення:**
1. Перевірте Valid OAuth Redirect URIs в Facebook
2. Переконайтесь що App є в режимі Development
3. Для локальної розробки використовуйте `localhost`

### Помилка: "SocialApp matching query does not exist"

**Проблема:** Не додано Social Application в Django Admin

**Рішення:**
1. Відкрийте http://127.0.0.1:8000/admin/
2. Перейдіть до Sites, переконайтесь що site існує
3. Створіть Social Application для Google/Facebook
4. Прив'яжіть до site

### Помилка: "Site matching query does not exist"

**Проблема:** SITE_ID не співпадає

**Рішення:**
```python
# Django shell
from django.contrib.sites.models import Site
Site.objects.all()  # Перевірити ID
```

В `settings.py`:
```python
SITE_ID = 1  # Використайте правильний ID
```

### Користувач створюється без профілю

**Проблема:** Signal не спрацював для OAuth користувача

**Рішення:** Перевірте signals.py:
```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
```

---

## 🚀 Продакшн налаштування

### Для продакшн сервера:

1. **Оновіть Redirect URIs:**
   ```
   https://yourdomain.com/accounts/google/login/callback/
   https://yourdomain.com/accounts/facebook/login/callback/
   ```

2. **Використовуйте змінні оточення:**
   ```python
   # settings.py
   import os
   
   SOCIALACCOUNT_PROVIDERS = {
       'google': {
           'APP': {
               'client_id': os.getenv('GOOGLE_CLIENT_ID'),
               'secret': os.getenv('GOOGLE_SECRET'),
               'key': ''
           }
       },
       'facebook': {
           'APP': {
               'client_id': os.getenv('FACEBOOK_APP_ID'),
               'secret': os.getenv('FACEBOOK_SECRET'),
               'key': ''
           }
       }
   }
   ```

3. **Оновіть Sites в Admin:**
   - Domain: `yourdomain.com`

4. **Facebook App в Live Mode:**
   - App Review → Request Advanced Access
   - Опублікуйте app

---

## 📊 Статистика після налаштування

### Доступні методи входу:

- ✅ Username + Password (стандартний)
- ✅ Email + Password (стандартний)
- ✅ Google OAuth 2.0
- ✅ Facebook OAuth 2.0

### Переваги OAuth:

- 🚀 Швидка реєстрація (1 клік)
- 🔐 Безпечна автентифікація
- 📧 Автоматична верифікація email
- 👤 Автоматичне отримання даних профілю

---

## 📚 Додаткові ресурси

- **django-allauth docs**: https://docs.allauth.org/
- **Google OAuth**: https://console.cloud.google.com/
- **Facebook Login**: https://developers.facebook.com/
- **Підтримувані провайдери**: https://docs.allauth.org/en/latest/socialaccount/providers/index.html

---

## ✨ Інші провайдери

django-allauth підтримує 50+ провайдерів:

- GitHub
- Twitter
- LinkedIn
- Instagram
- Microsoft
- Apple
- Discord
- Telegram
- і багато інших...

Для додавання іншого провайдера:
```python
# settings.py
INSTALLED_APPS += ['allauth.socialaccount.providers.github']
```

---

**OAuth налаштовано! Користувачі тепер можуть входити через Google та Facebook! 🎉**

**Важливо:** Для роботи OAuth обов'язково налаштуйте Social Applications в Django Admin!