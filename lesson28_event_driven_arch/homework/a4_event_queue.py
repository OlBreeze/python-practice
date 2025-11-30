import queue
import threading
import time
from datetime import datetime


# ====================================
# EVENTBUS З ЧЕРГОЮ
# ====================================
class EventBusWithQueue:
    """EventBus з асинхронною обробкою через чергу"""

    def __init__(self):
        self.listeners = {}
        self.event_log = []
        # Створюємо чергу для подій
        self.event_queue = queue.Queue()
        # Прапорець для зупинки worker-а
        self.running = True

    def subscribe(self, event_name, callback):
        """Підписатися на подію"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)
        print(f"✅ Підписка: {callback.__name__} -> {event_name}")

    def emit(self, event_name, data=None):
        """Додати подію в чергу (не обробляється одразу!)"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "name": event_name,
            "data": data
        }
        self.event_queue.put(event)
        print(f"➕ Подія додана в чергу: {event_name}")

    def process_event(self, event):
        """Обробити одну подію"""
        event_name = event["name"]
        data = event["data"]

        # Логуємо
        self.event_log.append(event)
        print(f"\n🔔 Обробка події: {event_name} | {data}")

        # Викликаємо всі listener-и
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"❗ Помилка в {callback.__name__}: {e}")
                    # Worker НЕ падає від помилок!

    def worker(self):
        """Worker для обробки подій з черги"""
        print("🚀 Worker запущено")

        while self.running:
            try:
                # Чекаємо подію з черги (timeout 1 секунда)
                event = self.event_queue.get(timeout=1)
                self.process_event(event)
                self.event_queue.task_done()
            except queue.Empty:
                # Черга порожня - просто чекаємо далі
                continue
            except Exception as e:
                print(f"❗ Критична помилка в worker: {e}")
                # Worker продовжує працювати!

        print("🛑 Worker зупинено")

    def start_worker(self):
        """Запустити worker в окремому потоці"""
        worker_thread = threading.Thread(target=self.worker, daemon=True)
        worker_thread.start()
        return worker_thread

    def stop(self):
        """Зупинити worker"""
        self.running = False
        self.event_queue.join()  # Чекаємо обробки всіх подій


# ====================================
# ПРИКЛАД ВИКОРИСТАННЯ
# ====================================

# Створюємо listener-и
def send_email(data):
    print(f"  📧 Email: Привіт, користувач {data['user_id']}!")
    time.sleep(0.5)  # Імітація повільної операції


def save_to_db(data):
    print(f"  💾 DB: Збережено в базу даних")
    time.sleep(0.3)


def send_sms(data):
    print(f"  📱 SMS: Повідомлення надіслано")
    time.sleep(0.2)


def buggy_listener(data):
    """Listener з помилкою - worker НЕ повинен падати"""
    print(f"  🐛 Buggy: Починаю обробку...")
    raise Exception("Ой! Щось пішло не так!")


# Створюємо EventBus
bus = EventBusWithQueue()

# Підписуємося
bus.subscribe("user.registered", send_email)
bus.subscribe("user.registered", save_to_db)
bus.subscribe("user.registered", buggy_listener)  # Цей listener з помилкою!
bus.subscribe("order.created", send_sms)
bus.subscribe("order.created", save_to_db)

# Запускаємо worker в окремому потоці
print("=" * 50)
print("ЗАПУСК АСИНХРОННОЇ ОБРОБКИ ПОДІЙ")
print("=" * 50 + "\n")

worker_thread = bus.start_worker()

# Генеруємо події (producer)
print("\n📤 Producer генерує події:\n")

bus.emit("user.registered", {"user_id": 123, "email": "test@example.com"})
bus.emit("user.registered", {"user_id": 456, "email": "user@example.com"})
bus.emit("order.created", {"order_id": 789, "amount": 1500})
bus.emit("user.registered", {"user_id": 999, "email": "admin@example.com"})

print("\n📤 Всі події додані в чергу. Worker обробляє...")

# Чекаємо, поки worker обробить всі події
time.sleep(5)

# Зупиняємо worker
print("\n" + "=" * 50)
print("ЗУПИНКА")
print("=" * 50)
bus.stop()

# Статистика
print(f"\n📊 Оброблено подій: {len(bus.event_log)}")
print(f"📋 Події в черзі: {bus.event_queue.qsize()}")

print("\n✅ Програма завершена. Зверни увагу:")
# print("   - Події оброблялися асинхронно (не одразу)")
# print("   - Worker НЕ впав, навіть коли buggy_listener викинув помилку")
# print("   - Решта listener-ів продовжили працювати")