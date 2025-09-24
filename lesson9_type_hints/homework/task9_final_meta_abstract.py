# Завдання 9: Final, метакласи та абстрактні класи.
#
# Створіть Final клас Config, щоб заборонити його наслідування.
# Реалізуйте абстрактний клас BaseRepository, який має метод save(data: Dict[str, Any]) -> None.
# Реалізуйте SQLRepository, який наслідує BaseRepository та перевизначає save().
#
# Приклад використання:
#     repo = SQLRepository()
#     repo.save({"name": "Product1", "price": 10.5})
#
# Якщо спробувати створити підклас від Config — згенерується TypeError.

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class FinalMeta(type):
    """
    Метаклас, що забороняє наслідування.

    Якщо клас використовує цей метаклас, будь-яка спроба оголосити підклас призведе до TypeError.
    Це дає runtime-гарантію (не тільки статичну через typing.final) що клас не можна наслідувати.
    """

    def __new__(mcls, name, bases, namespace, **kwargs):
        # Створюємо клас як зазвичай
        cls = super().__new__(mcls, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace, **kwargs):
        # Якщо серед батьків є клас, що уже оголошений з FinalMeta — забороняємо
        for base in bases:
            if isinstance(base, FinalMeta):
                raise TypeError(f"Cannot inherit from final class {base.__name__!r}")
        super().__init__(name, bases, namespace)


class Config(metaclass=FinalMeta):
    """
    Final клас для конфігурації програми.

    Цей клас не можна наслідувати (спроба створити підклас призведе до TypeError).

    Атрибути:
        db_url (str): URL до бази даних.
        debug (bool): режим відладки.
    """

    def __init__(self, db_url: str, debug: bool = False) -> None:
        self.db_url: str = db_url
        self.debug: bool = debug

    def __repr__(self) -> str:
        return f"Config(db_url={self.db_url!r}, debug={self.debug!r})"


class BaseRepository(ABC):
    """
    Абстрактний базовий клас репозиторію.

    Підкласи повинні реалізувати метод save, який зберігає словник даних.
    """

    @abstractmethod
    def save(self, data: Dict[str, Any]) -> None:
        """
        Зберегти дані.

        Args:
            data: словник з даними для збереження.
        """
        raise NotImplementedError


class SQLRepository(BaseRepository):
    """
    Конкретна реалізація репозиторію, що зберігає дані в "SQL-базі"(симулюємо збереження в пам'яті (list)).
    """

    def __init__(self) -> None:
        # Симульована "таблиця" у вигляді списку рядків (dict)
        self._storage: List[Dict[str, Any]] = []

    def save(self, data: Dict[str, Any]) -> None:
        """
        Зберігає запис у "таблицю".

        Args:
            data: словник із записом для збереження.

        Raises:
            ValueError: якщо data не є словником або порожній.
        """
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        if not data:
            raise ValueError("data cannot be empty")

        # Тут могла б бути валідація полів, підготовка SQL та виконання.
        # Для прикладу — просто додаємо до внутрішнього списку.
        self._storage.append(data.copy())

    def all(self) -> List[Dict[str, Any]]:
        """
        Повертає всі збережені записи (копія списку).
        """
        return [item.copy() for item in self._storage]

    def __repr__(self) -> str:
        return f"SQLRepository(storage_size={len(self._storage)})"


# ---------------------------
# Приклад використання:
# ---------------------------
if __name__ == "__main__":
    # Створюємо final-конфіг
    cfg = Config(db_url="postgresql://localhost/mydb", debug=True)
    print(cfg)  # Config(db_url='postgresql://localhost/mydb', debug=True)

    # Демонстрація роботи репозиторію
    repo = SQLRepository()
    repo.save({"name": "Product1", "price": 10.5})
    repo.save({"name": "Product2", "price": 20.0})
    print("Saved items:", repo.all())  # список словників

    # Спроба наслідувати Config призведе до помилки:
    try:
        class Bad(Config):  # type: ignore
            pass
    except TypeError as e:
        print("Expected error when inheriting from Config:", e)
