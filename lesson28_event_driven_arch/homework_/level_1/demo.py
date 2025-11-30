from eventbus import EventBus

# ==============================================
# ПРИКЛАД ВИКОРИСТАННЯ (Рівень 1, завдання 2)
# ==============================================

# Створюємо EventBus
bus = EventBus()


# Listener 1: Email Sender
def email_sender(data):
    print(f"  📧 Email: Вітаємо користувача {data.get('user_id')}!")


# Listener 2: Logger
def logger(data):
    print(f"  📝 Logger: Збережено подію з даними {data}")


# Listener 3: Analytics
def analytics(data):
    print(f"  📊 Analytics: Оброблено метрику для {data}")


# Wildcard listener для всіх user подій
def log_all_user_events(data):
    print(f"  🔍 Wildcard Logger: Виявлено user подію: {data}")


# Підписуємося на події
bus.subscribe("user.registered", email_sender)
bus.subscribe("user.registered", logger)
bus.subscribe("user.registered", analytics)
bus.subscribe("user.deleted", logger)
bus.subscribe("order.created", logger)
bus.subscribe("order.created", analytics)

# Підписка на wildcard
bus.subscribe("user.*", log_all_user_events)

# Генеруємо події
print("\n" + "=" * 50)
print("ТЕСТУВАННЯ EVENTBUS")
print("=" * 50)

bus.emit("user.registered", {"user_id": 123, "email": "user@example.com"})
bus.emit("user.deleted", {"user_id": 456})
bus.emit("order.created", {"order_id": 789, "amount": 1500})

# Виводимо логи
bus.print_logs()