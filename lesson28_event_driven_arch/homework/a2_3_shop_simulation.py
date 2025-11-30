import time
from typing import Dict

from a1_eventbus_basic import EventBus


# Використовуємо EventBus з попереднього завдання

# ====================================
# МОДУЛЬ 1: Order Service
# ====================================
class OrderService:
    """Сервіс управління замовленнями"""

    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.orders = {}

    def create_order(self, order_id: int, user_id: int, amount: float):
        """Створити замовлення"""
        order = {
            "order_id": order_id,
            "user_id": user_id,
            "amount": amount,
            "status": "created"
        }
        self.orders[order_id] = order

        # Генеруємо подію
        self.bus.emit("order.created", order)
        print(f"✅ Замовлення #{order_id} створено на суму {amount} грн")
        return order

    def pay_order(self, order_id: int):
        """Оплатити замовлення"""
        if order_id in self.orders:
            self.orders[order_id]["status"] = "paid"

            # Генеруємо подію
            self.bus.emit("order.paid", self.orders[order_id])
            print(f"💳 Замовлення #{order_id} оплачено")
        else:
            print(f"❌ Замовлення #{order_id} не знайдено")


# ====================================
# МОДУЛЬ 2: Notification Service
# ====================================
class NotificationService:
    """Сервіс сповіщень"""

    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        # Підписуємося на події
        self.bus.subscribe("order.created", self.send_email)
        self.bus.subscribe("order.paid", self.send_sms)

    def send_email(self, data: Dict):
        """Відправити email при створенні замовлення"""
        print(f"  📧 Email відправлено користувачу {data['user_id']}: Ваше замовлення #{data['order_id']} прийнято!")

    def send_sms(self, data: Dict):
        """Відправити SMS при оплаті"""
        print(f"  📱 SMS відправлено: Замовлення #{data['order_id']} оплачено. Дякуємо!")


# ====================================
# МОДУЛЬ 3: Analytics Service
# ====================================
class AnalyticsService:
    """Сервіс аналітики"""

    def __init__(self, event_bus: EventBus):
        self.bus = event_bus
        self.total_orders = 0
        self.total_paid = 0
        self.total_revenue = 0.0

        # Підписуємося на події
        self.bus.subscribe("order.created", self.count_order)
        self.bus.subscribe("order.paid", self.count_payment)

    def count_order(self, data: Dict):
        """Рахуємо створені замовлення"""
        self.total_orders += 1
        print(f"  📊 Analytics: Всього замовлень = {self.total_orders}")

    def count_payment(self, data: Dict):
        """Рахуємо оплачені замовлення"""
        self.total_paid += 1
        self.total_revenue += data['amount']
        print(f"  📊 Analytics: Оплачено = {self.total_paid}, Виручка = {self.total_revenue} грн")

    def print_stats(self):
        """Вивести статистику"""
        print("\n" + "=" * 50)
        print("📈 СТАТИСТИКА МАГАЗИНУ")
        print("=" * 50)
        print(f"Створено замовлень: {self.total_orders}")
        print(f"Оплачено: {self.total_paid}")
        print(f"Загальна виручка: {self.total_revenue} грн")
        print(
            f"Конверсія в оплату: {self.total_paid / self.total_orders * 100:.1f}%" if self.total_orders > 0 else "0%")


# ====================================
# ЗАПУСК СИМУЛЯЦІЇ
# ====================================
if __name__ == "__main__":
    print("🏪 СИМУЛЯЦІЯ ІНТЕРНЕТ-МАГАЗИНУ")
    print("=" * 50 + "\n")

    # Створюємо EventBus
    bus = EventBus()

    # Ініціалізуємо сервіси
    order_service = OrderService(bus)
    notification_service = NotificationService(bus)
    analytics_service = AnalyticsService(bus)

    # Симулюємо роботу магазину
    print("\n🛒 День 1: Створення замовлень\n")
    order_service.create_order(101, user_id=1, amount=1500.0)
    time.sleep(0.5)

    order_service.create_order(102, user_id=2, amount=2300.0)
    time.sleep(0.5)

    order_service.create_order(103, user_id=1, amount=750.0)

    print("\n\n💰 День 2: Оплата замовлень\n")
    order_service.pay_order(101)
    time.sleep(0.5)

    order_service.pay_order(103)
    time.sleep(0.5)

    # Виводимо статистику
    analytics_service.print_stats()

    # Виводимо історію подій
    print("\n" + "=" * 50)
    print("📜 ІСТОРІЯ ПОДІЙ")
    print("=" * 50)
    for log in bus.event_log:
        print(f"{log['timestamp']} | {log['event']}")