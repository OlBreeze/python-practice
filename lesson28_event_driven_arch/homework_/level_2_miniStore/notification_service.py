from typing import Dict

from ..level_1.eventbus import EventBus


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
