# WebSockets в Django: Работа с системами реального времени

## Введение

**WebSocket** — это протокол, обеспечивающий постоянное двустороннее соединение между клиентом и сервером. В отличие от классического HTTP, где клиент всегда инициирует запрос, WebSocket позволяет серверу отправлять данные клиенту в любой момент без ожидания запроса.

---

## Сравнение HTTP и WebSocket

| Параметр | HTTP | WebSocket |
|----------|------|-----------|
| **Тип связи** | Request-Response (запрос-ответ) | Постоянное двустороннее соединение |
| **Инициатор** | Только клиент | Клиент и сервер |
| **Overhead** | Полные заголовки при каждом запросе | Минимальные заголовки после установки соединения |
| **Режим реального времени** | Нет | Да |
| **Примеры использования** | REST API, обычные веб-страницы | Чаты, дашборды, онлайн-игры |

---

## Области применения WebSocket

### 1. Мессенджеры и чаты
- Telegram, WhatsApp, Slack
- Корпоративные системы связи
- Служба поддержки в реальном времени

### 2. Дашборды и аналитика
- Мониторинг в реальном времени
- KPI метрики
- Графики и визуализация данных

### 3. Совместная работа
- Google Docs стиль редактирования
- Figma для дизайна
- Онлайн-трекеры задач (CRM, Project Management)

### 4. Финансовые приложения
- Биржевые торги
- Курсы валют в реальном времени
- Криптовалютные биржи

### 5. Онлайн-игры
- Многопользовательские игры (например, World of Tanks)
- Браузерные игры
- Синхронизация состояния игры между игроками

### 6. Системы уведомлений
- Push-уведомления
- Трекинг изменений (новые задачи, заказы)
- Колл-центры и CRM

---

## Django и асинхронность

### Исторический контекст

Django — **синхронный фреймворк** по умолчанию:
- Работает с WSGI (Web Server Gateway Interface)
- Принцип: один поток = один запрос = один ответ
- **Не подходит** для WebSocket из коробки

### Эволюция Django

- **До версии 3.0**: Полностью синхронный
- **С версии 3.0+**: Частичная поддержка асинхронности
- **Решение для WebSocket**: ASGI (Asynchronous Server Gateway Interface)

### WSGI vs ASGI

- **WSGI** (`wsgi.py`): Синхронный сервер
- **ASGI** (`asgi.py`): Асинхронный сервер, поддерживает:
  - WebSockets
  - Асинхронные представления
  - Long polling
  - Background tasks

---

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

## Пример: Счетчик онлайн-пользователей

### Consumer

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