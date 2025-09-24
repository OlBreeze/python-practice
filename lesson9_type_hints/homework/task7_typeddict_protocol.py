# Створіть TypedDict для представлення користувача:
#
# class User(TypedDict):
#     id: int
#     name: str
#     is_admin: bool
# 2 .Створіть Protocol UserDatabase, який має методи:
#
# get_user(user_id: int) -> Optional[User]
# save_user(user: User) -> None
# 3. Реалізуйте клас InMemoryUserDB, який реалізує цей Protocol.

from typing import TypedDict, Protocol, Optional, List, Dict
from abc import abstractmethod


class User(TypedDict):
    """TypedDict для представлення користувача в системі"""
    id: int
    name: str
    is_admin: bool


# 2. Protocol для бази даних користувачів
class UserDatabase(Protocol):
    """Protocol, який визначає інтерфейс для роботи з базою даних користувачів"""

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        """
        Отримати користувача за ID

        Args:
            user_id: Унікальний ідентифікатор користувача

        Returns:
            User або None, якщо користувача не знайдено
        """
        pass

    @abstractmethod
    def save_user(self, user: User) -> None:
        """
        Зберегти користувача в базі даних

        Args:
            user: Дані користувача для збереження
        """
        ...


# 3. Реалізація InMemoryUserDB
class InMemoryUserDB: # (UserDatabase):  # Можно, но не обязательно
    """In-memory реалізація бази даних користувачів"""

    def __init__(self) -> None:
        """Ініціалізація порожньої бази даних"""
        self._users: Dict[int, User] = {}

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Отримати користувача за ID

        Args:
            user_id: ID користувача

        Returns:
            User або None
        """
        return self._users.get(user_id)

    def save_user(self, user: User) -> None:
        """
        Зберегти користувача в базі даних

        Args:
            user: Дані користувача
        """
        if not isinstance(user.get("id"), int) or user["id"] <= 0:
            raise ValueError("ID користувача повинен бути позитивним цілим числом")
        self._users[user["id"]] = user.copy()  # Створюємо копію для безпеки


# Функція для перевірки відповідності Protocol
def process_users(db: UserDatabase) -> None:
    """
    Функція, яка приймає будь-який об'єкт, що реалізує UserDatabase Protocol

    Args:
        db: База даних користувачів
    """
    # Створюємо тестових користувачів
    users: List[User] = [       # !!!
        {"id": 1, "name": "Alice", "is_admin": False},
        {"id": 2, "name": "Bob", "is_admin": True},
        {"id": 3, "name": "Charlie", "is_admin": False}
    ]

    # Зберігаємо користувачів
    for user in users:
        db.save_user(user)

    # Отримуємо користувачів
    for user_id in [1, 2, 3, 999]:
        user = db.get_user(user_id)
        if user:
            admin_status = "адміністратор" if user["is_admin"] else "користувач"
            print(f"ID {user_id}: {user['name']} ({admin_status})")
        else:
            print(f"ID {user_id}: користувача не знайдено")


# Демонстрація використання
def main():

    # 1. Базове використання
    print("1. Базове використання InMemoryUserDB:")
    db = InMemoryUserDB()

    # Зберігаємо користувачів
    db.save_user({"id": 1, "name": "Alice", "is_admin": False})
    db.save_user({"id": 2, "name": "Bob", "is_admin": True})

    # Отримуємо користувачів
    print(db.get_user(1))  # {"id": 1, "name": "Alice", "is_admin": False}
    print(db.get_user(2))  # {"id": 2, "name": "Bob", "is_admin": True}
    print(db.get_user(999))  # None
    print()

    # 5. Використання з Protocol
    print("5. Використання через Protocol:")
    fresh_db = InMemoryUserDB()
    process_users(fresh_db)  # Функція приймає UserDatabase Protocol
    print()


# Приклади створення користувачів з type hints
def create_user(user_id: int, name: str, is_admin: bool) -> User:
    """Функція-помічник для створення користувача"""
    return {"id": user_id, "name": name, "is_admin": is_admin}


if __name__ == "__main__":
    main()