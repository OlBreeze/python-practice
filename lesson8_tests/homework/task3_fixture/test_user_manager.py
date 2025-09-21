#   Напишіть програму для керування користувачами та напишіть тести з використанням фікстур у pytest.

import pytest

from lesson8_tests.homework.task3_fixture.user_manager import User, UserManager


@pytest.fixture
def user_manager() -> UserManager:
    """
    Фікстура для створення UserManager з попередньо встановленими користувачами.

    Returns:
        UserManager: Менеджер з Alice (30 років) та Bob (25 років).
    """
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


class TestUserManager:
    """Тести для класу UserManager."""

    def test_add_user_success(self, user_manager: UserManager) -> None:
        """
        Тестує успішне додавання нового користувача.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        initial_count = user_manager.get_users_count()
        result = user_manager.add_user("Charlie", 35)

        assert result is True
        assert user_manager.get_users_count() == initial_count + 1

        charlie = user_manager.get_user("Charlie")
        assert charlie is not None
        assert charlie.name == "Charlie"
        assert charlie.age == 35

    def test_add_user_duplicate(self, user_manager: UserManager) -> None:
        """
        Тестує спробу додавання користувача з існуючим іменем.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        initial_count = user_manager.get_users_count()
        result = user_manager.add_user("Alice", 40)

        assert result is False
        assert user_manager.get_users_count() == initial_count

        # Перевіряємо, що початковий користувач не змінився
        alice = user_manager.get_user("Alice")
        assert alice.age == 30

    def test_add_user_invalid_data(self, user_manager: UserManager) -> None:
        """
        Тестує додавання користувача з недійсними даними.
        """
        with pytest.raises(ValueError, match="Ім'я не може бути порожнім, а вік — негативним."):
            user_manager.add_user("", 25)

        with pytest.raises(ValueError, match="Ім'я не може бути порожнім, а вік — негативним."):
            user_manager.add_user("   ", 25)

        with pytest.raises(ValueError, match="Ім'я не може бути порожнім, а вік — негативним."):
            user_manager.add_user("John", -1)

    def test_remove_user_success(self, user_manager: UserManager) -> None:
        """
        Тестує успішне видалення користувача.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        initial_count = user_manager.get_users_count()
        result = user_manager.remove_user("Alice")

        assert result is True
        assert user_manager.get_users_count() == initial_count - 1
        assert user_manager.get_user("Alice") is None

    def test_remove_user_not_found(self, user_manager: UserManager) -> None:
        """
        Тестує спробу видалення неіснуючого користувача.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        initial_count = user_manager.get_users_count()
        result = user_manager.remove_user("NonExistent")

        assert result is False
        assert user_manager.get_users_count() == initial_count

    def test_remove_user_empty_name(self, user_manager: UserManager) -> None:
        """
        Тестує видалення користувача з порожнім іменем.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        assert user_manager.remove_user("") is False
        assert user_manager.remove_user("   ") is False

    def test_get_all_users(self, user_manager: UserManager) -> None:
        """
        Тестує отримання списку всіх користувачів.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        users = user_manager.get_all_users()

        assert len(users) == 2
        assert isinstance(users, list)

        # Перевіряємо, що список відсортований за іменем
        names = [user.name for user in users]
        assert names == sorted(names)

        # Перевіряємо вміст
        user_dict = {user.name: user.age for user in users}
        assert user_dict["Alice"] == 30
        assert user_dict["Bob"] == 25

    def test_get_user(self, user_manager: UserManager) -> None:
        """
        Тестує отримання користувача за іменем.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        alice = user_manager.get_user("Alice")
        assert alice is not None
        assert alice.name == "Alice"
        assert alice.age == 30

        # Тестуємо неіснуючого користувача
        nonexistent = user_manager.get_user("NonExistent")
        assert nonexistent is None

        # Тестуємо порожнє ім'я
        empty_result = user_manager.get_user("")
        assert empty_result is None

    @pytest.mark.skip(reason="Демонстрація умовного пропуску тесту")
    def test_always_skipped(self, user_manager: UserManager) -> None:
        """
        Тест, який завжди пропускається для демонстрації.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        # Цей тест ніколи не виконається
        assert False, "Цей тест не повинен виконуватися"

    def test_conditional_skip(self, user_manager: UserManager) -> None:
        """
        Тест, який пропускається за певних умов.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        users_count = user_manager.get_users_count()

        if users_count < 3:
            pytest.skip(f"Недостатньо користувачів для тесту: {users_count} < 3")

        # Цей код виконається тільки якщо користувачів >= 3
        assert len(user_manager.get_all_users()) >= 3

    def test_skip_with_fixture_condition(self, user_manager: UserManager) -> None:
        """
        Демонстрація пропуску тесту на основі стану фікстури.

        Args:
            user_manager: Фікстура з попередньо встановленими користувачами.
        """
        alice = user_manager.get_user("Alice")

        # Пропускаємо тест, якщо Alice молодша за 35 років
        if alice and alice.age < 35:
            pytest.skip(f"Alice занадто молода для цього тесту: {alice.age} < 35")

        # Логіка тесту для випадку, коли Alice >= 35 років
        assert alice.age >= 35
