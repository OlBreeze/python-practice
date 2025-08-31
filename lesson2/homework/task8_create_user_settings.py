# Завдання 8: Реалізувати систему зберігання налаштувань користувача за допомогою замикань.
# Налаштування можуть включати такі параметри, як theme, language і notifications.

def create_user_settings():
    """ Налаштування, ініціалізується один раз."""
    settings = {
        "theme": "dark",
        "language": "UK",
        "notifications": "sms"
    }

    def manage_settings(key, value=None):
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
