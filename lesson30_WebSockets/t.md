

## Установка и настройка Django Channels

### 1. Установка зависимостей

```bash
pip install channels
pip install channels-redis
pip install uvicorn[standard]
```

**Компоненты:**
- `channels` — библиотека для WebSocket в Django
- `channels-redis` — бэкенд для групповых сообщений (рекомендуется)
- `uvicorn` — ASGI сервер (аналог Gunicorn для async)

### 2. Настройка `settings.py`

```python
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'channels',  # Добавляем channels
    'your_app',  # Ваше приложение
]

# Указываем ASGI application
ASGI_APPLICATION = 'your_project.asgi.application'

# Настройка Channel Layers (для групповых сообщений)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Для разработки без Redis (не для production!):
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer'
#     }
# }
```

### 3. Настройка `asgi.py`

```python
# asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from your_app import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
```

---

## Создание WebSocket Consumer

### Что такое Consumer?

**Consumer** — это аналог Django View для WebSocket. Он обрабатывает:
- Подключение клиента (`connect`)
- Отключение клиента (`disconnect`)
- Получение сообщений (`receive`)
- Отправку сообщений (`send`)

### Пример: Чат-комната

#### 1. Файл `routing.py`

```python
# your_app/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
```

#### 2. Файл `consumers.py`

```python
# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Получаем имя комнаты из URL
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Принимаем соединение
        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Получаем сообщение от клиента
        data = json.loads(text_data)
        message = data['message']

        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        # Получаем сообщение из группы и отправляем клиенту
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
```

---

## Frontend: Подключение к WebSocket

### HTML Template

```html
<!-- templates/chat.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Chat Room</title>
</head>
<body>
    <div id="chat-log"></div>
    <input id="chat-message-input" type="text">
    <button id="chat-message-submit">Send</button>

    <script>
        const roomName = "{{ room_name }}";
        const socket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );

        // Получение сообщения
        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const message = data.message;
            
            const chatLog = document.getElementById('chat-log');
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            chatLog.appendChild(messageElement);
        };

        // Отправка сообщения
        document.getElementById('chat-message-submit').onclick = function(e) {
            const messageInput = document.getElementById('chat-message-input');
            const message = messageInput.value;
            
            socket.send(JSON.stringify({
                'message': message
            }));
            
            messageInput.value = '';
        };

        // Обработка ошибок
        socket.onclose = function(e) {
            console.error('WebSocket closed unexpectedly');
        };
    </script>
</body>
</html>
```

---

## Запуск сервера

```bash
# Вместо традиционного:
# python manage.py runserver

# Используем uvicorn для ASGI:
uvicorn your_project.asgi:application --reload
```

**Важно:** `manage.py runserver` не поддерживает WebSocket!

---

## Блокирующие vs неблокирующие операции

### Синхронный код (блокирующий)

```python
import time

def process():
    time.sleep(5)  # Блокирует поток на 5 секунд
    return "Done"
```

**Проблема:** Пока выполняется `sleep`, сервер не может обрабатывать другие запросы.

### Асинхронный код (неблокирующий)

```python
import asyncio

async def process():
    await asyncio.sleep(5)  # НЕ блокирует поток
    return "Done"
```

**Преимущество:** Пока ожидается ответ, сервер может обрабатывать другие запросы.

---

## Асинхронный доступ к базе данных

### Проблема

Django ORM по умолчанию **синхронный**:

```python
# Синхронный код - НЕ РАБОТАЕТ в async consumer
user = User.objects.get(id=1)
```

### Решение

Используйте **асинхронные адаптеры**:

```python
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)

# В async функции:
user = await get_user(1)
```

**Альтернатива:** Используйте асинхронные ORM библиотеки (например, `databases`, `tortoise-orm`).

---

## Тестирование WebSocket

### С помощью Postman

1. Выберите тип запроса: **WebSocket**
2. Введите URL: `ws://127.0.0.1:8000/ws/chat/room1/`
3. Нажмите **Connect**
4. Отправляйте JSON-сообщения:
   ```json
   {
       "message": "Hello, World!"
   }
   ```
5. Наблюдайте за ответами в окне Response

### С помощью браузера (DevTools)

```javascript
// В консоли браузера
const socket = new WebSocket('ws://localhost:8000/ws/chat/test/');
socket.onmessage = (e) => console.log('Received:', e.data);
socket.send(JSON.stringify({message: 'Test'}));
```

---

## Практические примеры: Полное решение заданий

### Задание 1: Счетчик онлайн-пользователей

#### Consumer

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

online_users = 0

class OnlineUsersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        global online_users
        online_users += 1
        
        await self.channel_layer.group_add('online_users', self.channel_name)
        await self.accept()
        
        # Отправляем обновленное количество всем
        await self.channel_layer.group_send(
            'online_users',
            {
                'type': 'count_update',
                'count': online_users
            }
        )

    async def disconnect(self, close_code):
        global online_users
        online_users -= 1
        
        await self.channel_layer.group_discard('online_users', self.channel_name)
        
        # Отправляем обновленное количество всем
        await self.channel_layer.group_send(
            'online_users',
            {
                'type': 'count_update',
                'count': online_users
            }
        )

    async def count_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))
```

#### Routing

```python
# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/online/

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

```

#### HTML Template

```html
<!-- templates/online_users.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Online Users Counter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            text-align: center;
        }
        #counter {
            font-size: 48px;
            color: #28a745;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>Пользователи онлайн</h1>
    <div id="counter">0</div>

    <script>
        const socket = new WebSocket('ws://' + window.location.host + '/ws/online/');

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'online_count') {
                document.getElementById('counter').textContent = data.count;
            }
        };

        socket.onclose = function(e) {
            console.error('WebSocket closed');
        };
    </script>
</body>
</html>
```

---

### Задание 2: Push-уведомления

#### Consumer

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notifications', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        
        # Отправляем уведомление всем подключенным клиентам
        await self.channel_layer.group_send(
            'notifications',
            {
                'type': 'send_notification',
                'message': message,
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event['message'],
            'timestamp': event['timestamp']
        }))
```

#### Routing (добавить к существующему)

```python
# routing.py
websocket_urlpatterns = [
    re_path(r'ws/online/

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---


## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

---

## Дополнительные ресурсы

- [Официальная документация Django Channels](https://channels.readthedocs.io/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Channels Examples на GitHub](https://github.com/django/channels-examples)

---

## Резюме

**WebSocket** — мощный инструмент для создания приложений реального времени:

✅ Двустороннее общение  
✅ Минимальная задержка  
✅ Эффективное использование ресурсов  
✅ Поддержка групповых сообщений  
✅ Масштабируемость с Redis  

**Django Channels** делает интеграцию WebSocket простой и удобной, сохраняя привычную структуру Django-проектов., consumers.NotificationConsumer.as_asgi()),
]
```

#### HTML Template

```html
<!-- templates/notifications.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Push Notifications</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        #notifications {
            border: 1px solid #ddd;
            padding: 20px;
            min-height: 300px;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        .notification {
            background: white;
            padding: 10px;
            margin: 10px 0;
            border-left: 4px solid #007bff;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .timestamp {
            color: #666;
            font-size: 12px;
        }
        input {
            width: 70%;
            padding: 10px;
            font-size: 16px;
        }
        button {
            width: 25%;
            padding: 10px;
            font-size: 16px;
            background: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Push Notifications System</h1>
    <div id="notifications"></div>
    
    <input id="message-input" type="text" placeholder="Введите сообщение">
    <button id="send-btn">Отправить</button>

    <script>
        const socket = new WebSocket('ws://' + window.location.host + '/ws/notifications/');
        const notificationsDiv = document.getElementById('notifications');
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            if (data.type === 'notification') {
                const notif = document.createElement('div');
                notif.className = 'notification';
                notif.innerHTML = `
                    <div>${data.message}</div>
                    <div class="timestamp">${data.timestamp}</div>
                `;
                notificationsDiv.insertBefore(notif, notificationsDiv.firstChild);
            }
        };

        sendBtn.onclick = function() {
            const message = messageInput.value.trim();
            if (message) {
                socket.send(JSON.stringify({
                    'message': message
                }));
                messageInput.value = '';
            }
        };

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendBtn.click();
            }
        });
    </script>
</body>
</html>
```

---

### Задание 3: Чат с аутентификацией

#### Consumer

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Получаем пользователя из scope
        self.user = self.scope['user']
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Отправляем приветственное сообщение
        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.user.username} присоединился к чату',
                    'username': 'System'
                }
            )

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': f'{self.user.username} покинул чат',
                    'username': 'System'
                }
            )
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        
        # Проверяем аутентификацию
        if not self.user.is_authenticated:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Только авторизованные пользователи могут писать сообщения'
            }))
            return
        
        # Отправляем сообщение в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username']
        }))
```

#### Routing (обновленный)

```python
# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/online/

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

---

## Дополнительные ресурсы

- [Официальная документация Django Channels](https://channels.readthedocs.io/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Channels Examples на GitHub](https://github.com/django/channels-examples)

---

## Резюме

**WebSocket** — мощный инструмент для создания приложений реального времени:

✅ Двустороннее общение  
✅ Минимальная задержка  
✅ Эффективное использование ресурсов  
✅ Поддержка групповых сообщений  
✅ Масштабируемость с Redis  

**Django Channels** делает интеграцию WebSocket простой и удобной, сохраняя привычную структуру Django-проектов., consumers.OnlineUsersConsumer.as_asgi()),
    re_path(r'ws/notifications/

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

---

## Дополнительные ресурсы

- [Официальная документация Django Channels](https://channels.readthedocs.io/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Channels Examples на GitHub](https://github.com/django/channels-examples)

---

## Резюме

**WebSocket** — мощный инструмент для создания приложений реального времени:

✅ Двустороннее общение  
✅ Минимальная задержка  
✅ Эффективное использование ресурсов  
✅ Поддержка групповых сообщений  
✅ Масштабируемость с Redis  

**Django Channels** делает интеграцию WebSocket простой и удобной, сохраняя привычную структуру Django-проектов., consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>\w+)/

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

---

## Дополнительные ресурсы

- [Официальная документация Django Channels](https://channels.readthedocs.io/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Channels Examples на GitHub](https://github.com/django/channels-examples)

---

## Резюме

**WebSocket** — мощный инструмент для создания приложений реального времени:

✅ Двустороннее общение  
✅ Минимальная задержка  
✅ Эффективное использование ресурсов  
✅ Поддержка групповых сообщений  
✅ Масштабируемость с Redis  

**Django Channels** делает интеграцию WebSocket простой и удобной, сохраняя привычную структуру Django-проектов., consumers.ChatConsumer.as_asgi()),
]
```

#### HTML Template

```html
<!-- templates/chat.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Chat Room: {{ room_name }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        #chat-log {
            border: 1px solid #ddd;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            background: #f9f9f9;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }
        .username {
            font-weight: bold;
            color: #007bff;
        }
        .system {
            color: #6c757d;
            font-style: italic;
        }
        .error {
            color: #dc3545;
            background: #f8d7da;
            padding: 10px;
            border-radius: 5px;
        }
        #message-input {
            width: 80%;
            padding: 10px;
            font-size: 16px;
        }
        #send-btn {
            width: 18%;
            padding: 10px;
            font-size: 16px;
            background: #28a745;
            color: white;
            border: none;
            cursor: pointer;
        }
        #send-btn:hover {
            background: #218838;
        }
        #user-info {
            background: #e7f3ff;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Чат: {{ room_name }}</h1>
    
    <div id="user-info">
        {% if user.is_authenticated %}
            <strong>Вы вошли как:</strong> {{ user.username }}
        {% else %}
            <strong>Внимание:</strong> Вы гость. Войдите, чтобы писать сообщения.
            <a href="{% url 'login' %}">Войти</a>
        {% endif %}
    </div>

    <div id="chat-log"></div>
    
    <input id="message-input" type="text" placeholder="Введите сообщение">
    <button id="send-btn">Отправить</button>

    <script>
        const roomName = "{{ room_name }}";
        const socket = new WebSocket(
            'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
        );

        const chatLog = document.getElementById('chat-log');
        const messageInput = document.getElementById('message-input');
        const sendBtn = document.getElementById('send-btn');

        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            const messageDiv = document.createElement('div');
            
            if (data.type === 'error') {
                messageDiv.className = 'error';
                messageDiv.textContent = data.message;
            } else if (data.type === 'message') {
                messageDiv.className = 'message';
                if (data.username === 'System') {
                    messageDiv.className += ' system';
                    messageDiv.textContent = data.message;
                } else {
                    messageDiv.innerHTML = `
                        <span class="username">${data.username}:</span>
                        ${data.message}
                    `;
                }
            }
            
            chatLog.appendChild(messageDiv);
            chatLog.scrollTop = chatLog.scrollHeight;
        };

        sendBtn.onclick = function() {
            const message = messageInput.value.trim();
            if (message) {
                socket.send(JSON.stringify({
                    'message': message
                }));
                messageInput.value = '';
            }
        };

        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendBtn.click();
            }
        });

        socket.onclose = function(e) {
            console.error('WebSocket closed');
        };
    </script>
</body>
</html>
```

#### Views для отображения страниц

```python
# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def online_users(request):
    return render(request, 'online_users.html')

def notifications(request):
    return render(request, 'notifications.html')

def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
    })
```

#### URLs

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('online/', views.online_users, name='online_users'),
    path('notifications/', views.notifications, name='notifications'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
```

---

## Best Practices

### 1. Безопасность

- **Аутентификация**: Используйте `AuthMiddlewareStack` для проверки пользователей
- **CSRF**: WebSocket не использует CSRF токены
- **Валидация**: Всегда проверяйте входящие данные

### 2. Производительность

- **Redis**: Используйте Redis для production (не InMemory)
- **Оптимизация запросов**: Минимизируйте обращения к БД
- **Кэширование**: Используйте кэш для часто запрашиваемых данных

### 3. Масштабирование

- **Horizontal scaling**: Redis Channel Layer поддерживает несколько серверов
- **Load balancing**: Используйте Nginx для распределения нагрузки
- **Мониторинг**: Следите за количеством активных соединений

---

## Middleware для WebSocket

```python
# middleware.py
from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user(token):
    # Ваша логика аутентификации
    try:
        return User.objects.get(auth_token=token)
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Извлекаем токен из query string
        token = dict(scope['query_string']).get(b'token')
        if token:
            scope['user'] = await get_user(token.decode())
        else:
            scope['user'] = AnonymousUser()
        
        return await self.app(scope, receive, send)

# В asgi.py:
# application = ProtocolTypeRouter({
#     'websocket': TokenAuthMiddleware(
#         URLRouter(routing.websocket_urlpatterns)
#     ),
# })
```

---

## Частые ошибки

### 1. Использование `manage.py runserver`
**Ошибка:** WebSocket не работает  
**Решение:** Используйте `uvicorn` или `daphne`

### 2. Синхронный код в async consumer
**Ошибка:** `SynchronousOnlyOperation`  
**Решение:** Оберните в `database_sync_to_async`

### 3. Забыли добавить channels в INSTALLED_APPS
**Ошибка:** `ModuleNotFoundError`  
**Решение:** Добавьте `'channels'` в `INSTALLED_APPS`

### 4. Redis не запущен
**Ошибка:** `ConnectionRefusedError`  
**Решение:** Запустите Redis сервер: `redis-server`

---

## Дополнительные ресурсы

- [Официальная документация Django Channels](https://channels.readthedocs.io/)
- [WebSocket MDN](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Channels Examples на GitHub](https://github.com/django/channels-examples)

---

## Резюме

**WebSocket** — мощный инструмент для создания приложений реального времени:

✅ Двустороннее общение  
✅ Минимальная задержка  
✅ Эффективное использование ресурсов  
✅ Поддержка групповых сообщений  
✅ Масштабируемость с Redis  

**Django Channels** делает интеграцию WebSocket простой и удобной, сохраняя привычную структуру Django-проектов.