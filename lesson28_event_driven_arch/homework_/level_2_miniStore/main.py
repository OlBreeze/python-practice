import time

from ..level_1.eventbus import EventBus
from .analytics_service import AnalyticsService
from .notification_service import NotificationService
from .order_service import OrderService

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