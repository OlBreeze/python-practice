"""
Модуль для керування користувачами.

Цей модуль містить клас UserManager для керування колекцією користувачів
та відповідні тести з використанням pytest фікстур.
"""

from typing import List, Dict, Optional


class User:
    """
        Клас користувача.

        Attributes:
            name (str): Ім'я користувача.
            age (int):  Вік користувача.
    """

    def __init__(self, name: str, age: int) -> None:
        """
        Ініціалізує об'єкт користувача.

        Args:
            name (str): Ім'я користувача.
            age (int):  Вік користувача.
        """
        if not name or not name.strip():
            raise ValueError("Ім'я користувача не може бути порожнім")
        if age < 0:
            raise ValueError("Вік не може бути негативним")

        self.name = name.strip()
        self.age = age

    def __str__(self) -> str:
        """Повертає строкове представлення користувача."""
        return f"User(name='{self.name}', age={self.age})"


class UserManager:
    """
    Клас для керування колекцією користувачів.

    Attributes:
        _users (Dict[str, User]): Словник користувачів з ім'ям як ключем.
    """

    def __init__(self) -> None:
        """Ініціалізує порожній менеджер користувачів."""
        self._users: Dict[str, User] = {}

    def add_user(self, name: str, age: int) -> bool:
        """
        Додає користувача до системи.

        Args:
            name (str): Ім'я користувача.
            age (int): Вік користувача.

        Returns:
            bool: True, якщо користувач успішно доданий, False якщо вже існує.

        Raises:
            ValueError: Якщо ім'я порожнє або вік негативний.
        """
        if not name.strip() or age < 0:
            raise ValueError("Ім'я не може бути порожнім, а вік — негативним.")

        if name.strip() in self._users:
            return False

        user = User(name, age)
        self._users[user.name] = user
        return True

    def remove_user(self, name: str) -> bool:
        """
        Видаляє користувача за ім'ям.

        Args:
            name (str): Ім'я користувача для видалення.

        Returns:
            bool: True, якщо користувач був вилучений, False якщо не знайден.
        """
        if not name or name.strip() not in self._users:
            return False

        del self._users[name.strip()]
        return True

    def get_all_users(self) -> List[User]:
        """
        Повертає список усіх користувачів.

        Returns:
            List[User]: Список всіх користувачів, відсортований на ім'я.
        """
        return sorted(self._users.values(), key=lambda user: user.name)

    def get_user(self, name: str) -> Optional[User]:
        """
        Повертає користувача за ім'ям.

        Args:
            name (str): ім'я  користувача.

        Returns:
            Optional[User]: Користувач, якщо знайдено, иначе None.
        """
        if not name:
            return None
        return self._users.get(name.strip())

    def get_users_count(self) -> int:
        """
        Повертає кількість користувачів у системі.

        Returns:
            int: Кількість користувачів.
        """
        return len(self._users)
