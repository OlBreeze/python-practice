"""
ІМІТАЦІЯ RABBITMQ
Це спрощена версія без реального RabbitMQ для демонстрації концепції.

ДЛЯ РЕАЛЬНОЇ РОБОТИ З RABBITMQ:
1. Встанови RabbitMQ через Docker:
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

2. Встанови бібліотеку:
   pip install pika

3. Використовуй код нижче, замінивши SimulatedQueue на справжній pika
"""

import time
import threading
import json
from queue import Queue
from typing import Callable


# ====================================
# ІМІТАЦІЯ RABBITMQ ЧЕРЕЗ QUEUE
# ====================================

class SimulatedRabbitMQ:
    """Проста імітація RabbitMQ для навчання"""

    def __init__(self):
        # Словник черг: {"exchange_name": Queue()}
        self.exchanges = {}
        self.running = True

    def create_exchange(self, exchange_name):
        """Створити exchange (точку обміну повідомленнями)"""
        if exchange_name not in self.exchanges:
            self.exchanges[exchange_name] = Queue()
            print(f"✅ Exchange '{exchange_name}' створено")

    def publish(self, exchange_name, message):
        """Опублікувати повідомлення (Producer)"""
        if exchange_name in self.exchanges:
            self.exchanges[exchange_name].put(message)
            print(f"📤 Опубліковано в '{exchange_name}': {message}")
        else:
            print(f"❌ Exchange '{exchange_name}' не існує")

    def consume(self, exchange_name, callback: Callable, worker_name: str):
        """Споживати повідомлення (Consumer/Worker)"""
        print(f"🚀 Worker '{worker_name}' підключився до '{exchange_name}'")

        while self.running:
            try:
                # Отримуємо повідомлення з черги
                message = self.exchanges[exchange_name].get(timeout=1)
                print(f"\n📥 [{worker_name}] Отримано: {message}")

                try:
                    callback(message)
                except Exception as e:
                    print(f"❗ [{worker_name}] Помилка обробки: {e}")

                self.exchanges[exchange_name].task_done()

            except:
                # Черга порожня - чекаємо далі
                continue

    def stop(self):
        """Зупинити всі worker-и"""
        self.running = False


# ====================================
# PRODUCER (Сервер)
# ====================================

class UserRegistrationService:
    """Сервіс реєстрації користувачів"""

    def __init__(self, rabbitmq: SimulatedRabbitMQ):
        self.rabbitmq = rabbitmq

    def register_user(self, user_id: int, email: str):
        """Зареєструвати користувача"""
        message = {
            "event": "user.registered",
            "data": {
                "user_id": user_id,
                "email": email,
                "timestamp": time.time()
            }
        }

        # Публікуємо подію в RabbitMQ
        self.rabbitmq.publish("user_events", json.dumps(message))
        print(f"✅ Користувач {email} зареєстрований\n")


# ====================================
# CONSUMER 1: Email Worker
# ====================================

def email_worker(message):
    """Worker для відправки email"""
    data = json.loads(message)
    user_id = data['data']['user_id']
    email = data['data']['email']

    print(f"  📧 [Email Worker] Відправляю вітальний email на {email}...")
    time.sleep(1)  # Імітація відправки
    print(f"  ✅ [Email Worker] Email надіслано")


# ====================================
# CONSUMER 2: Analytics Worker
# ====================================

class AnalyticsWorker:
    """Worker для збору аналітики"""

    def __init__(self):
        self.total_users = 0

    def process(self, message):
        """Обробити подію"""
        data = json.loads(message)
        self.total_users += 1

        print(f"  📊 [Analytics Worker] Оновлюю статистику...")
        time.sleep(0.5)
        print(f"  📈 [Analytics Worker] Всього користувачів: {self.total_users}")


# ====================================
# ЗАПУСК СИСТЕМИ
# ====================================

if __name__ == "__main__":
    print("=" * 60)
    print("ДЕМОНСТРАЦІЯ RABBITMQ PATTERN")
    print("=" * 60 + "\n")

    # Створюємо "RabbitMQ"
    rabbitmq = SimulatedRabbitMQ()
    rabbitmq.create_exchange("user_events")

    # Створюємо analytics worker
    analytics = AnalyticsWorker()

    # Запускаємо worker-ів в окремих потоках
    email_thread = threading.Thread(
        target=rabbitmq.consume,
        args=("user_events", email_worker, "Email Worker"),
        daemon=True
    )

    analytics_thread = threading.Thread(
        target=rabbitmq.consume,
        args=("user_events", analytics.process, "Analytics Worker"),
        daemon=True
    )

    email_thread.start()
    analytics_thread.start()

    # Даємо worker-ам час на підключення
    time.sleep(1)

    print("\n" + "=" * 60)
    print("PRODUCER: Реєструємо користувачів")
    print("=" * 60 + "\n")

    # Створюємо producer (сервіс реєстрації)
    registration_service = UserRegistrationService(rabbitmq)

    # Реєструємо користувачів
    registration_service.register_user(1, "alice@example.com")
    time.sleep(2)

    registration_service.register_user(2, "bob@example.com")
    time.sleep(2)

    registration_service.register_user(3, "charlie@example.com")
    time.sleep(2)

    # Зупиняємо
    print("\n" + "=" * 60)
    print("Зупинка системи...")
    print("=" * 60)
    rabbitmq.stop()
    time.sleep(1)

    print("\n" + "=" * 60)
    print("ВИСНОВКИ:")
    print("=" * 60)
    print("✅ Producer (сервіс реєстрації) відокремлений від Consumer-ів")
    print("✅ Кожна подія обробляється ОБОМА worker-ами незалежно")
    print("✅ Якщо один worker падає - інший продовжує працювати")
    print("✅ Легко додати нових worker-ів без зміни Producer-а")
    print("\n📌 Це основна ідея RabbitMQ, Kafka, AWS SQS та інших черг повідомлень")

    # print("\n" + "=" * 60)
    # print("ДЛЯ РЕАЛЬНОЇ РОБОТИ З RABBITMQ:")
    # print("=" * 60)
    # print("1. docker run -d --name rabbitmq -p 5672:5672 rabbitmq:3-management")
    # print("2. pip install pika")
    # print("3. Замініть SimulatedRabbitMQ на справжній pika.BlockingConnection")
    # print("\nПриклад коду з pika знайдеш в документації: https://www.rabbitmq.com/tutorials")