import json
from datetime import datetime


# ====================================
# EVENTBUS З EVENT REPLAY
# ====================================
class EventBusWithReplay:
    """EventBus з можливістю запису та відтворення подій"""

    def __init__(self, log_file="events.log"):
        self.listeners = {}
        self.event_log = []
        self.log_file = log_file

    def subscribe(self, event_name, callback):
        """Підписатися на подію"""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data=None):
        """Випустити подію"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": event_name,
            "data": data
        }

        # Додаємо в лог
        self.event_log.append(event)

        # Записуємо в файл
        self._save_to_file(event)

        print(f"🔔 Подія: {event_name}")

        # Викликаємо listener-и
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    print(f"❗ Помилка в {callback.__name__}: {e}")

    def _save_to_file(self, event):
        """Записати подію в файл"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')

    def replay_from_file(self, filename=None):
        """Перезапустити події з файлу"""
        filename = filename or self.log_file

        print(f"\n{'=' * 50}")
        print(f"🔄 REPLAY: Відтворення подій з {filename}")
        print('=' * 50)

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        event = json.loads(line.strip())
                        event_name = event['event']
                        data = event['data']

                        print(f"\n[{line_num}] Replay: {event_name} | {event['timestamp']}")

                        # Викликаємо listener-и (БЕЗ повторного збереження)
                        if event_name in self.listeners:
                            for callback in self.listeners[event_name]:
                                try:
                                    callback(data)
                                except Exception as e:
                                    print(f"❗ Помилка: {e}")

                    except json.JSONDecodeError as e:
                        print(f"⚠️ Помилка парсингу рядка {line_num}: {e}")

            print(f"\n✅ Replay завершено")

        except FileNotFoundError:
            print(f"❌ Файл {filename} не знайдено")

    def clear_log_file(self):
        """Очистити файл логів"""
        with open(self.log_file, 'w') as f:
            f.write('')
        print(f"🗑️ Файл {self.log_file} очищено")


# ====================================
# СИМУЛЯЦІЯ БАНКІВСЬКИХ ОПЕРАЦІЙ
# ====================================

class BankAccount:
    """Простий банківський рахунок"""

    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance
        print(f"💰 Рахунок #{account_id} створено. Баланс: {self.balance} грн")

    def deposit(self, data):
        """Поповнення"""
        amount = data['amount']
        self.balance += amount
        print(f"  ➕ Рахунок #{self.account_id}: +{amount} грн. Баланс: {self.balance} грн")

    def withdraw(self, data):
        """Зняття"""
        amount = data['amount']
        if self.balance >= amount:
            self.balance -= amount
            print(f"  ➖ Рахунок #{self.account_id}: -{amount} грн. Баланс: {self.balance} грн")
        else:
            print(f"  ❌ Недостатньо коштів! Баланс: {self.balance} грн")

    def show_balance(self):
        print(f"\n💵 Поточний баланс рахунку #{self.account_id}: {self.balance} грн")


# ====================================
# ДЕМОНСТРАЦІЯ
# ====================================

if __name__ == "__main__":
    # Очищаємо старий лог
    bus = EventBusWithReplay("events.log")
    bus.clear_log_file()

    print("\n" + "=" * 50)
    print("СЦЕНАРІЙ 1: Виконуємо операції")
    print("=" * 50 + "\n")

    # Створюємо рахунок
    account = BankAccount(account_id=12345, initial_balance=1000)

    # Підписуємося на події
    bus.subscribe("account.deposit", account.deposit)
    bus.subscribe("account.withdraw", account.withdraw)

    # Генеруємо події
    bus.emit("account.deposit", {"amount": 500})
    bus.emit("account.withdraw", {"amount": 200})
    bus.emit("account.deposit", {"amount": 1000})
    bus.emit("account.withdraw", {"amount": 300})

    account.show_balance()

    # ====================================
    # ТЕПЕР РОБИМО REPLAY
    # ====================================

    print("\n\n" + "=" * 50)
    print("СЦЕНАРІЙ 2: Створюємо НОВИЙ рахунок і відтворюємо історію")
    print("=" * 50 + "\n")

    # Створюємо новий EventBus та рахунок
    bus2 = EventBusWithReplay("events.log")
    account2 = BankAccount(account_id=99999, initial_balance=1000)

    # Підписуємося
    bus2.subscribe("account.deposit", account2.deposit)
    bus2.subscribe("account.withdraw", account2.withdraw)

    # REPLAY - відтворюємо всі події з файлу
    bus2.replay_from_file()

    account2.show_balance()

    # print("\n" + "=" * 50)
    # print("📝 ВИСНОВОК:")
    # print("=" * 50)
    # print("✅ Обидва рахунки мають однаковий баланс!")
    # print("✅ Це Event Sourcing - відновлення стану з історії подій")
    # print("✅ Використовується в Kafka, банківських системах, аудиті")
    # print("\n💡 Переваги:")
    # print("   - Можна відновити стан на будь-який момент часу")
    # print("   - Повна історія всіх змін")
    # print("   - Легко знайти помилки та відкотити зміни")