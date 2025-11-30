import fnmatch
from datetime import datetime
from typing import Callable, Dict, List


class EventBus:
    """EventBus з підтримкою wildcard та логування"""

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_log: List[Dict] = []

    def subscribe(self, event_name: str, callback: Callable):
        self.listeners.setdefault(event_name, []).append(callback)
        print(f"✅ Підписка: {callback.__name__} -> {event_name}")

    def unsubscribe(self, event_name: str, callback: Callable):
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)
            print(f"❌ Відписка: {callback.__name__} від {event_name}")

    def emit(self, event_name: str, data: dict = None):
        # Лог події
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "data": data
        }
        self.event_log.append(log_entry)
        print(f"\n🔔 Подія: {event_name} | Дані: {data}")

        # Exact match listeners
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                self._safe_call(callback, data)

        # Wildcard listeners (user.*, *.created, user.*.deleted, etc.)
        for pattern, callbacks in self.listeners.items():
            if "*" in pattern and fnmatch.fnmatch(event_name, pattern): # проверяет, соответствует ли заданная строка определённому шаблону, используя специальные символы, такие как * (любое количество символов) и ? (один символ). Это удобный инструмент для поиска файлов по шаблонам или фильтрации строк
                for callback in callbacks:
                    self._safe_call(callback, data)

    def _safe_call(self, callback, data):
        try:
            callback(data)
        except Exception as e:
            print(f"❗ Помилка в {callback.__name__}: {e}")

    def get_logs(self):
        return self.event_log

    def print_logs(self):
        print("\n📋 Логи подій:")
        for log in self.event_log:
            print(f"  {log['timestamp']} | {log['event']} | {log['data']}")
