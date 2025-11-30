"""
WEBHOOK SERVER - Отримання подій через HTTP

ВСТАНОВЛЕННЯ:
pip install flask

ЗАПУСК:
python webhook_server.py

ТЕСТУВАННЯ:
curl -X POST http://localhost:5000/webhook/order \
  -H "Content-Type: application/json" \
  -d '{"order_id": 777, "status": "created"}'
"""

from flask import Flask, request, jsonify
import threading
import time
from datetime import datetime
from queue import Queue


# ====================================
# EVENTBUS ДЛЯ WEBHOOK
# ====================================

class EventBus:
    """Простий EventBus для обробки webhook-ів"""

    def __init__(self):
        self.listeners = {}
        self.event_queue = Queue()
        self.event_log = []
        self.running = True

    def subscribe(self, event_name, callback):
        """Підписатися на подію"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data):
        """Додати подію в чергу"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "data": data
        }
        self.event_queue.put(event)
        self.event_log.append(event)

    def worker(self):
        """Worker для обробки подій"""
        print("🚀 EventBus Worker запущено")

        while self.running:
            try:
                event = self.event_queue.get(timeout=1)
                event_name = event["event"]
                data = event["data"]

                print(f"\n🔔 Обробка: {event_name} | {data}")

                # Викликаємо listener-и
                if event_name in self.listeners:
                    for callback in self.listeners[event_name]:
                        try:
                            callback(data)
                        except Exception as e:
                            print(f"❗ Помилка в {callback.__name__}: {e}")

                self.event_queue.task_done()

            except:
                continue

    def start_worker(self):
        """Запустити worker в окремому потоці"""
        worker_thread = threading.Thread(target=self.worker, daemon=True)
        worker_thread.start()


# ====================================
# LISTENERS (обробники подій)
# ====================================

def send_email(data):
    """Відправити email"""
    order_id = data.get("order_id")
    print(f"  📧 Email: Ваше замовлення #{order_id} прийнято!")


def log_to_database(data):
    """Логування в БД"""
    print(f"  💾 Database: Збережено подію {data}")
    time.sleep(0.2)  # Імітація запису в БД


def send_to_analytics(data):
    """Відправити в аналітику"""
    print(f"  📊 Analytics: Відправлено метрику")


def send_notification(data):
    """Сповіщення в Slack/Telegram"""
    order_id = data.get("order_id")
    print(f"  💬 Slack: Нове замовлення #{order_id} створено!")


# ====================================
# FLASK WEBHOOK SERVER
# ====================================

# Створюємо EventBus
event_bus = EventBus()

# Підписуємо listener-ів
event_bus.subscribe("order.created", send_email)
event_bus.subscribe("order.created", log_to_database)
event_bus.subscribe("order.created", send_to_analytics)
event_bus.subscribe("order.created", send_notification)

# Запускаємо worker
event_bus.start_worker()

# Створюємо Flask додаток
app = Flask(__name__)


@app.route('/')
def home():
    """Головна сторінка"""
    return """
    <h1>🎣 Webhook Server</h1>
    <p>Сервер працює і чекає на webhook-и!</p>

    <h2>Як відправити webhook:</h2>
    <pre>
curl -X POST http://localhost:5000/webhook/order \\
  -H "Content-Type: application/json" \\
  -d '{"order_id": 777, "status": "created"}'
    </pre>

    <p><a href="/logs">📋 Переглянути логи</a></p>
    """


@app.route('/webhook/order', methods=['POST'])
def webhook_order():
    """
    Ендпоінт для отримання webhook-ів про замовлення
    Приклад: {"order_id": 777, "status": "created"}
    """
    try:
        # Отримуємо JSON з запиту
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        order_id = data.get("order_id")
        status = data.get("status")

        print(f"\n{'=' * 50}")
        print(f"📥 WEBHOOK ОТРИМАНО")
        print(f"{'=' * 50}")
        print(f"Order ID: {order_id}")
        print(f"Status: {status}")
        print(f"Full data: {data}")

        # Генеруємо подію в EventBus
        event_bus.emit("order.created", data)

        # Повертаємо успішну відповідь
        return jsonify({
            "status": "success",
            "message": f"Webhook для замовлення #{order_id} прийнято",
            "received_at": datetime.now().isoformat()
        }), 200

    except Exception as e:
        print(f"❌ Помилка обробки webhook: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/logs', methods=['GET'])
def get_logs():
    """Переглянути всі отримані події"""
    return jsonify({
        "total_events": len(event_bus.event_log),
        "events": event_bus.event_log
    })


@app.route('/health', methods=['GET'])
def health():
    """Перевірка здоров'я сервера"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


# ====================================
# ЗАПУСК СЕРВЕРА
# ====================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🎣 WEBHOOK SERVER")
    print("=" * 60)
    print("✅ EventBus worker запущено")
    print("✅ Flask сервер запускається...")
    print("\n📌 Відкрий в браузері: http://localhost:5000")
    print("📌 Для тестування використовуй curl або Postman")
    print("\n" + "=" * 60 + "\n")

    # Запускаємо Flask сервер
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False  # Щоб worker не запустився двічі
    )

# ====================================
# ПРИКЛАДИ ТЕСТУВАННЯ
# ====================================

"""
# 1. Простий webhook:
curl -X POST http://localhost:5000/webhook/order \
  -H "Content-Type: application/json" \
  -d '{"order_id": 777, "status": "created"}'

# 2. З додатковими даними:
curl -X POST http://localhost:5000/webhook/order \
  -H "Content-Type: application/json" \
  -d '{"order_id": 888, "status": "created", "amount": 1500, "customer": "John"}'

# 3. Переглянути логи:
curl http://localhost:5000/logs

# 4. Health check:
curl http://localhost:5000/health

# РЕАЛЬНІ ПРИКЛАДИ WEBHOOK-ІВ:
# - GitHub: коли хтось робить push в репозиторій
# - Stripe: коли користувач оплачує
# - LiqPay: підтвердження платежу
# - Telegram Bot: нове повідомлення
"""