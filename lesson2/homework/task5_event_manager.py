# Завдання 5: Розробити простий календар подій
# Використовуючи замикання, створити функції для додавання подій, видалення подій та перегляду майбутніх подій.
# Зберігати події у списку за допомогою глобальної змінної.

from datetime import datetime, date
from typing import List, Dict

events = []


def create_event_manager():
    """
    Створює менеджер подій.
    Повертає словник з функціями для роботи з подіями.
    """

    def add_event(name: str, event_date: str, description: str = "") -> str:
        """Додавання події."""
        try:
            parsed_date = datetime.strptime(event_date, "%Y-%m-%d").date()

            event = {
                "name": name,
                "date": parsed_date,
                "description": description,
                "created_at": datetime.now()
            }

            events.append(event)
            return f"Подія '{name}' додана на {event_date}"

        except ValueError:
            return "Помилка: неправильний формат дати. Використовуйте YYYY-MM-DD"

    def remove_event(name: str) -> str:
        """Видалення події за назвою."""
        for i, event in enumerate(events):
            if event["name"].lower() == name.lower():
                removed_event = events.pop(i)
                return f"Подія '{removed_event['name']}' видалена"

        return f"Подія '{name}' не знайдена"

    def get_upcoming_events(days_ahead: int = 30) -> List[Dict]:
        """Майбутні події."""
        today = date.today()
        upcoming = []

        for event in events:
            days_until = (event["date"] - today).days
            if 0 <= days_until <= days_ahead:
                event_copy = event.copy()
                event_copy["days_until"] = days_until
                upcoming.append(event_copy)

        # Сортуємо за датою
        upcoming.sort(key=lambda x: x["date"])
        # sort() → меняет список на месте (возвращает None).
        # sorted() → создаёт новый список, не трогая исходный.

        return upcoming

    def show_upcoming_events(days_ahead: int = 30) -> str:
        """Відображення майбутніх подій."""
        upcoming = get_upcoming_events(days_ahead)

        if not upcoming:
            return f"Немає майбутніх подій на найближчі {days_ahead} днів"

        result = f"Майбутні події (найближчі {days_ahead} днів):\n"
        result += "-" * 50 + "\n"

        for event in upcoming:
            days_text = "сьогодні" if event["days_until"] == 0 else f"через {event['days_until']} дн."
            result += f"📅 {event['name']} - {event['date']} ({days_text})\n"
            if event["description"]:
                result += f"   📝 {event['description']}\n"

        return result

    # Повертаємо словник з методами
    return {
        "add": add_event,
        "remove": remove_event,
        "upcoming": show_upcoming_events,
    }


# Створюємо менеджер подій
calendar = create_event_manager()

# Додаємо події
print("1. Додавання подій:")
print(calendar["add"]("День народження", "2025-09-15", "Святкування 25-річчя"))
print(calendar["add"]("Зустріч", "2025-09-05", "Презентація проекту"))
print(calendar["add"]("Відпустка", "2025-10-01", "Поїздка до Карпат"))
print(calendar["add"]("Конференція", "2025-09-20"))

print("\n2. Майбутні події (30 днів):")
print(calendar["upcoming"](30))

print("\n3. Видалення події:")
print(calendar["remove"]("Зустріч"))
print(calendar["upcoming"](30))

print("\n5. Спроба видалити неіснуючу подію:")
print(calendar["remove"]("Неіснуюча подія"))

print("Створюємо ще один менеджер подій:")
# Створюємо другий менеджер (з тими ж замиканнями)
calendar2 = create_event_manager()

print("Другий менеджер має доступ до тих же подій:")
print(calendar2["upcoming"](30))
