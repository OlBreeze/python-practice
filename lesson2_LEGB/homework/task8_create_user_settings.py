# Завдання 8: Реалізувати систему зберігання налаштувань користувача за допомогою замикань.
# Налаштування можуть включати такі параметри, як theme, language і notifications.

def create_user_settings():
    """ Налаштування, ініціалізується один раз.
    Повертає:
        Функцію manage_settings(key, value=None),"""
    settings: dict[str, str] = {
        "theme": "dark",
        "language": "UK",
        "notifications": "sms"
    }

    def manage_settings(key: str, value=None):
        """
        Керує доступом до налаштувань.

        Параметри:
            key (str): Назва параметру налаштувань.
            value (Optional[str]): Нове значення для параметру. Якщо не вказано – буде повернуто поточне значення.

        Повертає:
            str: Поточне або оновлене значення параметру,
                або повідомлення про помилку, якщо параметр не знайдено.
        """
        if key not in settings:
            return f"Помилка: Налаштування '{key}' не існує."

        if value is None or value == settings[key]:
            return settings[key]
        else:
            settings[key] = value
            return f"Налаштування '{key}' оновлено до '{value}'."

    return manage_settings


# Check
user_settings = create_user_settings()

print("Поточні налаштування:")
print(f"Тема: {user_settings('theme')}")
print(f"Мова: {user_settings('language')}")
print(f"Сповіщення: {user_settings('notifications')}")

print("---")
print(user_settings('theme', 'light'))
print(user_settings('language', 'ENG'))

print("---")
print("Оновлені налаштування:")
print(f"Тема: {user_settings('theme')}")
print(f"Мова: {user_settings('language')}")
