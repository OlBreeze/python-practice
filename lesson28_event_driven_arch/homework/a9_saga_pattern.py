"""
SAGA PATTERN - Розподілені транзакції

Проблема: В мікросервісах немає єдиної БД для транзакцій
Рішення: Saga - послідовність локальних транзакцій з компенсуючими діями

Приклад: Оформлення замовлення
1. Резервуємо товар
2. Списуємо гроші
3. Створюємо доставку
4. Якщо щось падає - робимо КОМПЕНСАЦІЮ (відкат)
"""

import time
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional


# ====================================
# SAGA STATUS
# ====================================

class SagaStatus(Enum):
    STARTED = "STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"


# ====================================
# SAGA ORCHESTRATOR
# ====================================

class SagaOrchestrator:
    """Координатор Saga - керує послідовністю кроків"""

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.status = SagaStatus.STARTED
        self.steps_executed = []
        self.event_log = []

    def log_event(self, event: str, data: dict):
        """Логування подій"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "data": data
        }
        self.event_log.append(entry)
        print(f"  📝 [{self.saga_id}] {event}: {data}")

    def execute_step(self, step_name: str, action, rollback_action):
        """
        Виконати крок Saga

        Args:
            step_name: назва кроку
            action: функція що виконує дію
            rollback_action: функція компенсації
        """
        try:
            print(f"\n▶️  Крок: {step_name}")
            result = action()

            # Зберігаємо успішний крок
            self.steps_executed.append({
                "name": step_name,
                "rollback": rollback_action,
                "result": result
            })

            self.log_event(f"STEP_COMPLETED", {"step": step_name, "result": result})
            return result

        except Exception as e:
            print(f"❌ Помилка в кроці '{step_name}': {e}")
            self.log_event(f"STEP_FAILED", {"step": step_name, "error": str(e)})
            raise

    def compensate(self):
        """Компенсувати всі виконані кроки (відкат)"""
        print(f"\n{'=' * 60}")
        print(f"🔄 КОМПЕНСАЦІЯ: Відкатуємо виконані кроки")
        print(f"{'=' * 60}")

        self.status = SagaStatus.COMPENSATING

        # Відкочуємо кроки у зворотному порядку
        for step in reversed(self.steps_executed):
            step_name = step["name"]
            rollback = step["rollback"]

            print(f"\n◀️  Компенсація: {step_name}")
            try:
                rollback()
                self.log_event("STEP_COMPENSATED", {"step": step_name})
            except Exception as e:
                print(f"❗ Помилка компенсації '{step_name}': {e}")
                self.log_event("COMPENSATION_FAILED", {"step": step_name, "error": str(e)})

        self.status = SagaStatus.COMPENSATED
        print(f"\n✅ Всі кроки компенсовано")


# ====================================
# СЕРВІСИ (мікросервіси)
# ====================================

class InventoryService:
    """Сервіс управління складом"""

    def __init__(self):
        self.reserved = {}

    def reserve_product(self, product_id: int, quantity: int):
        """Резервувати товар"""
        print(f"  📦 Inventory: Резервуємо товар {product_id} (кількість: {quantity})")
        time.sleep(0.5)

        # Імітація перевірки наявності
        if product_id == 999:  # спеціальний товар що завжди недоступний
            raise Exception(f"Товар {product_id} відсутній на складі")

        self.reserved[product_id] = quantity
        print(f"  ✅ Товар {product_id} зарезервовано")
        return {"reserved": True, "product_id": product_id}

    def cancel_reservation(self, product_id: int):
        """КОМПЕНСАЦІЯ: Скасувати резервування"""
        print(f"  ↩️  Inventory: Скасовуємо резервування товару {product_id}")
        if product_id in self.reserved:
            del self.reserved[product_id]
        print(f"  ✅ Резервування скасовано")


class PaymentService:
    """Сервіс оплати"""

    def __init__(self):
        self.transactions = {}

    def charge_customer(self, customer_id: int, amount: float):
        """Списати гроші"""
        print(f"  💳 Payment: Списуємо {amount} грн з рахунку {customer_id}")
        time.sleep(0.5)

        # Імітація недостатньо коштів
        if amount > 10000:
            raise Exception(f"Недостатньо коштів для суми {amount}")

        transaction_id = f"TXN_{customer_id}_{int(time.time())}"
        self.transactions[transaction_id] = amount
        print(f"  ✅ Списано {amount} грн (транзакція: {transaction_id})")
        return {"transaction_id": transaction_id, "amount": amount}

    def refund(self, transaction_id: str):
        """КОМПЕНСАЦІЯ: Повернути гроші"""
        print(f"  ↩️  Payment: Повертаємо гроші (транзакція: {transaction_id})")
        if transaction_id in self.transactions:
            amount = self.transactions[transaction_id]
            del self.transactions[transaction_id]
            print(f"  ✅ Повернено {amount} грн")


class DeliveryService:
    """Сервіс доставки"""

    def __init__(self):
        self.deliveries = {}

    def create_delivery(self, order_id: int, address: str):
        """Створити доставку"""
        print(f"  🚚 Delivery: Створюємо доставку для замовлення {order_id}")
        time.sleep(0.5)

        delivery_id = f"DEL_{order_id}"
        self.deliveries[delivery_id] = address
        print(f"  ✅ Доставку створено (ID: {delivery_id})")
        return {"delivery_id": delivery_id}

    def cancel_delivery(self, delivery_id: str):
        """КОМПЕНСАЦІЯ: Скасувати доставку"""
        print(f"  ↩️  Delivery: Скасовуємо доставку {delivery_id}")
        if delivery_id in self.deliveries:
            del self.deliveries[delivery_id]
        print(f"  ✅ Доставку скасовано")


# ====================================
# ORDER SAGA - оркестрація замовлення
# ====================================

def create_order_saga(order_id: int, product_id: int, customer_id: int, amount: float, address: str):
    """
    SAGA для створення замовлення:
    1. Резервуємо товар
    2. Списуємо гроші
    3. Створюємо доставку
    """

    # Створюємо сервіси
    inventory = InventoryService()
    payment = PaymentService()
    delivery = DeliveryService()

    # Створюємо оркестратор
    saga = SagaOrchestrator(f"ORDER_SAGA_{order_id}")

    print("=" * 60)
    print(f"🎬 SAGA ПОЧАЛАСЯ: Замовлення #{order_id}")
    print("=" * 60)

    try:
        # Крок 1: Резервування товару
        product_result = saga.execute_step(
            "Reserve Product",
            action=lambda: inventory.reserve_product(product_id, 1),
            rollback_action=lambda: inventory.cancel_reservation(product_id)
        )

        # Крок 2: Списання коштів
        payment_result = saga.execute_step(
            "Charge Payment",
            action=lambda: payment.charge_customer(customer_id, amount),
            rollback_action=lambda: payment.refund(payment_result["transaction_id"])
        )

        # Крок 3: Створення доставки
        delivery_result = saga.execute_step(
            "Create Delivery",
            action=lambda: delivery.create_delivery(order_id, address),
            rollback_action=lambda: delivery.cancel_delivery(delivery_result["delivery_id"])
        )

        # Успіх!
        saga.status = SagaStatus.COMPLETED
        print(f"\n{'=' * 60}")
        print(f"✅ SAGA ЗАВЕРШЕНА УСПІШНО")
        print(f"{'=' * 60}")

    except Exception as e:
        # Якась помилка - запускаємо компенсацію
        saga.status = SagaStatus.FAILED
        print(f"\n{'=' * 60}")
        print(f"❌ SAGA ПРОВАЛИЛАСЯ: {e}")
        print(f"{'=' * 60}")
        saga.compensate()

    # Виводимо логи
    print(f"\n{'=' * 60}")
    print(f"📋 ЛОГИ SAGA")
    print(f"{'=' * 60}")
    for log in saga.event_log:
        print(f"{log['timestamp']} | {log['event']}")

    return saga


# ====================================
# ДЕМОНСТРАЦІЯ
# ====================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SAGA PATTERN DEMO")
    print("=" * 60 + "\n")

    # Тест 1: Успішна Saga
    print("\n🟢 ТЕСТ 1: Успішне замовлення\n")
    saga1 = create_order_saga(
        order_id=1001,
        product_id=123,
        customer_id=555,
        amount=1500,
        address="вул. Хрещатик, 1"
    )

    time.sleep(2)

    # Тест 2: Провал на етапі оплати (сума занадто велика)
    print("\n" + "=" * 60)
    print("🔴 ТЕСТ 2: Провал через недостатньо коштів")
    print("=" * 60 + "\n")
    saga2 = create_order_saga(
        order_id=1002,
        product_id=456,
        customer_id=666,
        amount=15000,  # Занадто велика сума
        address="вул. Дерибасівська, 10"
    )

    time.sleep(2)

    # Тест 3: Провал на етапі резервування
    print("\n" + "=" * 60)
    print("🔴 ТЕСТ 3: Провал через відсутність товару")
    print("=" * 60 + "\n")
    saga3 = create_order_saga(
        order_id=1003,
        product_id=999,  # Спеціальний ID що викликає помилку
        customer_id=777,
        amount=2000,
        address="пр. Перемоги, 50"
    )

    # Висновки
    # print("\n" + "=" * 60)
    # print("💡 ВИСНОВКИ ПРО SAGA PATTERN")
    # print("=" * 60)
    # print("1️⃣  Saga = послідовність локальних транзакцій")
    # print("2️⃣  Кожен крок має компенсуючу дію (rollback)")
    # print("3️⃣  При помилці відкочуються ВСІ попередні кроки")
    # print("4️⃣  Логується вся послідовність подій")
    # print("5️⃣  Використовується в мікросервісах (Uber, Netflix)")
    #
    # print("\n📌 ДЕ ВИКОРИСТОВУЄТЬСЯ:")
    # print("   - E-commerce: оформлення замовлень")
    # print("   - Банки: переказ між рахунками")
    # print("   - Бронювання: готель + авіаквитки + прокат авто")
    # print("   - Будь-які розподілені транзакції")
    #
    # print("\n🔥 Альтернативи: 2-Phase Commit (2PC), але Saga простіша і надійніша")