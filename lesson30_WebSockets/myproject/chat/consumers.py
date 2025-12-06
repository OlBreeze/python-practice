import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User

# Глобальный счетчик (в продакшене используй Redis)
online_users = {}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'
        self.user = self.scope["user"]

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # ЗАДАЧА 1: Увеличиваем счетчик онлайн
        online_users[self.channel_name] = {
            'username': self.user.username if self.user.is_authenticated else 'Guest',
            'authenticated': self.user.is_authenticated
        }

        # Отправляем всем обновленный счетчик
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count',
                'count': len(online_users)
            }
        )

        # Отправляем приветственное сообщение
        username = self.user.username if self.user.is_authenticated else 'Guest'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': username
            }
        )

    async def disconnect(self, close_code):
        # ЗАДАЧА 1: Уменьшаем счетчик при отключении
        if self.channel_name in online_users:
            username = online_users[self.channel_name]['username']
            del online_users[self.channel_name]

            # Уведомляем всех о выходе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'username': username
                }
            )

            # Обновляем счетчик
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'online_count',
                    'count': len(online_users)
                }
            )

        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        # ЗАДАЧА 3: Проверяем аутентификацию для сообщений
        if message_type == 'chat_message':
            if not self.user.is_authenticated:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'You must be logged in to send messages'
                }))
                return

            message = data.get('message', '')

            # Отправляем сообщение всем в группе
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username
                }
            )

        # Push уведомления
        elif message_type == 'push_notification':
            notification_text = data.get('text', 'New notification!')

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'push_notification',
                    'text': notification_text,
                    'sender': self.user.username if self.user.is_authenticated else 'Guest'
                }
            )

    # Обработчики событий
    async def online_count(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username']
        }))

    async def push_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'push_notification',
            'text': event['text'],
            'sender': event['sender']
        }))

    async def user_join(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username']
        }))

    async def user_leave(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username']
        }))
