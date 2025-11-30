from ..level_1.eventbus import EventBus


# Використовуємо EventBus з попереднього файлу

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


