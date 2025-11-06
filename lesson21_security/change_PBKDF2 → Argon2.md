# поменять хешер паролей в Django (с PBKDF2 → Argon2)  

Ниже — **инструкция** + советы по миграции паролей, примеры кода и предостережения.

---

## 1) Установить Argon2

```bash
pip install argon2-cffi
```

(в production лучше фиксировать версию в requirements.txt)

---

## 2) Подключить Argon2 в `settings.py`

Добавь `Argon2PasswordHasher` **первым** в список `PASSWORD_HASHERS`. Оставь старые хешеры ниже — это позволит валидировать старые пароли.

```python
# settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',        # <--- новый предпочтительный
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

После этого **новые** пароли будут хешироваться Argon2.

---

## 3) Что будет с уже существующими паролями?

* Django проверяет хеш, перебирая все хешеры из `PASSWORD_HASHERS`. Поэтому старые пароли останутся рабочими — до тех пор, пока в списке сохранён старый алгоритм (PBKDF2).
* **Новые хеши (Argon2)** появятся:

  * когда пользователь сменит пароль, или
  * при реализации логики «пере-хеширования» при входе (см. ниже).

Важно: нельзя восстановить оригинальные пароли — можно только перехешировать, имея raw password (его дает процесс логина или смены пароля).

---

## 4) Автоматическое пере-хеширование при логине (рекомендуемый вариант)

Если хочешь плавно перевести всех пользователей на Argon2, можно **при успешной аутентификации** перехешировать пароль (у тебя есть raw password в момент логина). Пример — в кастомном view логина:

```python
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Если текущий алгоритм хеширования не Argon2 — перехешируем
            hasher_name = user.password.split('$', 1)[0]  # быстрое определение по префиксу
            if 'argon2' not in user.password:   # простая проверка
                user.set_password(password)     # set_password использует текущий (Argon2) hasher
                user.save(update_fields=['password'])
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')
```

Более аккуратно можно использовать `django.contrib.auth.hashers.identify_hasher()` для определения алгоритма.

---

## 5) Как принудительно пере-хешировать ВСЕ пароли? (неполная опция)

Нельзя получить raw-пароли пользователей из хешей — поэтому массового автоматического перекодирования **без участия пользователей** сделать нельзя. Опции:

* Предложить пользователям массовую **вынужденную смену пароля** (email + сброс).
* Или реализовать автоматическое пере-хеширование при следующем логине (как выше). Это наиболее безопасный и прозрачный путь.

---

## 6) Тонкая настройка параметров Argon2

Если нужны отличные от дефолтных параметры (time_cost, memory_cost, parallelism), можно создать свой хешер:

```python
# my_hashers.py
from django.contrib.auth.hashers import Argon2PasswordHasher

class CustomArgon2PasswordHasher(Argon2PasswordHasher):
    time_cost = 4          # default примерно 2-4 — увеличивать для безопасности
    memory_cost = 102400   # килобайты (пример)
    parallelism = 8
```

И подключить его в `PASSWORD_HASHERS`:

```python
PASSWORD_HASHERS = [
    'path.to.my_hashers.CustomArgon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    ...
]
```

**ВАЖНО:** увеличивая параметры, ты повышаешь безопасность, но и ресурсозатраты (CPU/RAM, latency). Протестируй нагрузку и настрой подходящие параметры для твоей инфраструктуры.

---

## 7) Мониторинг и тестирование

* Тестируй время хеширования в dev/stage при реальных нагрузках.
* Мониторь CPU/Memory после релиза.
* Протестируй процесс логина, reset password, админку и всё, что использует `set_password`/`check_password`.

---

## 8) Checklist перед продом

* [ ] Установлен `argon2-cffi` и включён в requirements.
* [ ] `PASSWORD_HASHERS` обновлён (Argon2 — первым).
* [ ] Реализовано/тестировано пере-хеширование при логине (или план по смене пароля).
* [ ] Проверены и, при необходимости, настроены параметры Argon2.
* [ ] Протестирована производительность логина на staging.
* [ ] Обновлены доки/CI и деплой-процедуры.

---

## 9) Коротко о плюсах/минусах Argon2

**Плюсы:**

* Современный memory-hard алгоритм, сильная защита от GPU/ASIC атак.
* Хорошо подходит для новых проектов, микросервисов и публичных сервисов.

**Минусы:**

* Более тяжёлый по ресурсам (CPU/RAM) чем PBKDF2 — нужно тестировать.
* Требует установки внешней библиотеки (`argon2-cffi`) и небольшой настройки.

---


