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


# 1. TypedDict для представлення користувача
class User(TypedDict):
    """TypedDict для представлення користувача в системі"""
    id: int
    name: str
    is_admin: bool


# Додатковий TypedDict з опціональними полями
class ExtendedUser(TypedDict, total=False):
    """Розширений користувач з опціональними полями"""
    id: int
    name: str
    is_admin: bool
    email: Optional[str]
    age: Optional[int]
    created_at: Optional[str]


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
        ...

    @abstractmethod
    def save_user(self, user: User) -> None:
        """
        Зберегти користувача в базі даних

        Args:
            user: Дані користувача для збереження
        """
        ...


# Розширений Protocol з додатковими методами
class ExtendedUserDatabase(Protocol):
    """Розширений Protocol з додатковими методами"""

    def get_user(self, user_id: int) -> Optional[User]:
        """Отримати користувача за ID"""
        ...

    def save_user(self, user: User) -> None:
        """Зберегти користувача"""
        ...

    def delete_user(self, user_id: int) -> bool:
        """Видалити користувача"""
        ...

    def get_all_users(self) -> List[User]:
        """Отримати всіх користувачів"""
        ...

    def get_admins(self) -> List[User]:
        """Отримати всіх адміністраторів"""
        ...


# 3. Реалізація InMemoryUserDB
class InMemoryUserDB:
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
        self._users[user["id"]] = user.copy()  # Створюємо копію для безпеки

    def delete_user(self, user_id: int) -> bool:
        """
        Видалити користувача за ID

        Args:
            user_id: ID користувача для видалення

        Returns:
            True, якщо користувача видалено, False якщо не знайдено
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def get_all_users(self) -> List[User]:
        """
        Отримати всіх користувачів

        Returns:
            Список всіх користувачів
        """
        return list(self._users.values())

    def get_admins(self) -> List[User]:
        """
        Отримати всіх адміністраторів

        Returns:
            Список користувачів з правами адміністратора
        """
        return [user for user in self._users.values() if user["is_admin"]]

    def update_user(self, user_id: int, updates: Dict[str, any]) -> bool:
        """
        Оновити дані користувача

        Args:
            user_id: ID користувача
            updates: Словник з оновленнями

        Returns:
            True якщо оновлено, False якщо користувача не знайдено
        """
        if user_id not in self._users:
            return False

        user = self._users[user_id]
        # Оновлюємо тільки валідні поля
        for key, value in updates.items():
            if key in ["name", "is_admin"]:  # id не можна змінювати
                user[key] = value

        return True

    def count_users(self) -> int:
        """Отримати кількість користувачів"""
        return len(self._users)

    def user_exists(self, user_id: int) -> bool:
        """Перевірити чи існує користувач"""
        return user_id in self._users

    def clear(self) -> None:
        """Очистити всю базу даних"""
        self._users.clear()


# Альтернативна реалізація з валідацією
class ValidatedInMemoryUserDB:
    """In-memory база даних з валідацією"""

    def __init__(self) -> None:
        self._users: Dict[int, User] = {}

    def _validate_user(self, user: User) -> None:
        """Валідація користувача"""
        if not isinstance(user.get("id"), int) or user["id"] <= 0:
            raise ValueError("ID користувача повинен бути позитивним цілим числом")

        if not isinstance(user.get("name"), str) or not user["name"].strip():
            raise ValueError("Ім'я користувача повинно бути непорожнім рядком")

        if not isinstance(user.get("is_admin"), bool):
            raise ValueError("is_admin повинен бути булевим значенням")

    def get_user(self, user_id: int) -> Optional[User]:
        """Отримати користувача за ID"""
        return self._users.get(user_id)

    def save_user(self, user: User) -> None:
        """Зберегти користувача з валідацією"""
        self._validate_user(user)
        self._users[user["id"]] = user.copy()

    def delete_user(self, user_id: int) -> bool:
        """Видалити користувача"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False

    def get_all_users(self) -> List[User]:
        """Отримати всіх користувачів"""
        return list(self._users.values())

    def get_admins(self) -> List[User]:
        """Отримати всіх адміністраторів"""
        return [user for user in self._users.values() if user["is_admin"]]


# Функція для перевірки відповідності Protocol
def process_users(db: UserDatabase) -> None:
    """
    Функція, яка приймає будь-який об'єкт, що реалізує UserDatabase Protocol

    Args:
        db: База даних користувачів
    """
    # Створюємо тестових користувачів
    users = [
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
    """Основна функція для демонстрації"""
    print("=== Демонстрація роботи з TypedDict та Protocol ===\n")

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

    # 2. Розширена функціональність
    print("2. Розширена функціональність:")
    db.save_user({"id": 3, "name": "Charlie", "is_admin": False})

    print(f"Всього користувачів: {db.count_users()}")
    print(f"Адміністратори: {db.get_admins()}")
    print(f"Всі користувачі: {db.get_all_users()}")
    print()

    # 3. Оновлення користувача
    print("3. Оновлення користувача:")
    print(f"До оновлення: {db.get_user(1)}")
    db.update_user(1, {"name": "Alice Johnson", "is_admin": True})
    print(f"Після оновлення: {db.get_user(1)}")
    print()

    # 4. Видалення користувача
    print("4. Видалення користувача:")
    print(f"Користувач існує: {db.user_exists(3)}")
    deleted = db.delete_user(3)
    print(f"Видалено: {deleted}")
    print(f"Користувач існує: {db.user_exists(3)}")
    print()

    # 5. Використання з Protocol
    print("5. Використання через Protocol:")
    fresh_db = InMemoryUserDB()
    process_users(fresh_db)  # Функція приймає UserDatabase Protocol
    print()

    # 6. Валідована база даних
    print("6. Валідована база даних:")
    validated_db = ValidatedInMemoryUserDB()

    try:
        # Валідний користувач
        validated_db.save_user({"id": 1, "name": "Valid User", "is_admin": True})
        print("Валідного користувача збережено успішно")

        # Невалідний користувач
        validated_db.save_user({"id": -1, "name": "", "is_admin": "not_bool"})
    except ValueError as e:
        print(f"Помилка валідації: {e}")

    print(f"Користувачі у валідованій БД: {validated_db.get_all_users()}")


# Приклади створення користувачів з type hints
def create_user(user_id: int, name: str, is_admin: bool) -> User:
    """Функція-помічник для створення користувача"""
    return {"id": user_id, "name": name, "is_admin": is_admin}


def create_extended_user(user_id: int, name: str, is_admin: bool,
                         email: Optional[str] = None,
                         age: Optional[int] = None) -> ExtendedUser:
    """Функція для створення розширеного користувача"""
    user: ExtendedUser = {"id": user_id, "name": name, "is_admin": is_admin}

    if email is not None:
        user["email"] = email
    if age is not None:
        user["age"] = age

    return user


if __name__ == "__main__":
    main()