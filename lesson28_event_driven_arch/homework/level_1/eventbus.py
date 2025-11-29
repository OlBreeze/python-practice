from datetime import datetime
from typing import Callable, Dict, List

class EventBus:
    """EventBus з підтримкою wildcard та логування"""

    def __init__(self):
        # Словник: ключ = назва події, значення = список callback функцій
        self.listeners: Dict[str, List[Callable]] = {}
        # Список для логування всіх подій
        self.event_log: List[Dict] = []

    def subscribe(self, event_name: str, callback: Callable):
        """Підписатися на подію"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)
        print(f"✅ Підписка: {callback.__name__} -> {event_name}")

    def unsubscribe(self, event_name: str, callback: Callable):
        """Відписатися від події"""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)
            print(f"❌ Відписка: {callback.__name__} від {event_name}")

    def emit(self, event_name: str, data: dict = None):
        """Випустити подію"""
        # Логуємо подію
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "data": data
        }
        self.event_log.append(log_entry)
        print(f"\n🔔 Подія: {event_name} | Дані: {data}")

        # Викликаємо всі listener-и для точної події
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"❗ Помилка в {callback.__name__}: {e}")

        # Обробка wildcard підписок (наприклад, user.*)
        event_parts = event_name.split('.')
        if len(event_parts) >= 2:
            wildcard = event_parts[0] + ".*"
            if wildcard in self.listeners:
                for callback in self.listeners[wildcard]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"❗ Помилка в {callback.__name__}: {e}")

    def get_logs(self):
        """Отримати всі логи подій"""
        return self.event_log

    def print_logs(self):
        """Вивести всі логи"""
        print("\n📋 Логи подій:")
        for log in self.event_log:
            print(f"  {log['timestamp']} | {log['event']} | {log['data']}")

