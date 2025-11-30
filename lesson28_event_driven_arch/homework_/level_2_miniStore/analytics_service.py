from typing import Dict

from ..level_1.eventbus import EventBus


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

