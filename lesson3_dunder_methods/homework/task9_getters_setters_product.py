""" 9. Порівняння сеттерів/геттерів, декоратора @property та дескрипторів
Демонструє різні способи валідації атрибута price у класі Product.
"""

from typing import Union


# 1. ГЕТТЕРИ/СЕТТЕРИ
class ProductWithGetSet:
    """Клас Product з використанням геттерів/сеттерів для атрибута price."""

    def __init__(self, name: str, price: float) -> None:
        """Ініціалізує товар з назвою та ціною."""
        self.name = name
        self._price = 0.0  # Приватний атрибут
        self.set_price(price)

    def get_price(self) -> float:
        """Повертає поточну ціну товару."""
        return self._price

    def set_price(self, value: float) -> None:
        """Встановлює ціну товару з валідацією."""
        if not isinstance(value, (int, float)):
            raise TypeError("Ціна повинна бути числом")
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = float(value)

    def __str__(self) -> str:
        return f"ProductWithGetSet(name='{self.name}', price={self._price})"

    def __repr__(self) -> str:
        return self.__str__()


# 2. ПІДХІД З ДЕКОРАТОРОМ @property
class ProductWithProperty:
    """Клас Product з використанням декоратора @property для атрибута price."""

    def __init__(self, name: str, price: float) -> None:
        """Ініціалізує товар з назвою та ціною."""
        self.name = name
        self._price = 0.0  # Приватний атрибут
        self.price = price  # Використовуємо property setter для валідації

    @property
    def price(self) -> float:
        """Getter для атрибута price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Setter для атрибута price з валідацією."""
        if not isinstance(value, (int, float)):
            raise TypeError("Ціна повинна бути числом")
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        self._price = float(value)

    @price.deleter
    def price(self) -> None:
        """Deleter для атрибута price."""
        print("Видалення ціни товару")
        self._price = 0.0

    def __str__(self) -> str:
        return f"ProductWithProperty(name='{self.name}', price={self._price})"

    def __repr__(self) -> str:
        return self.__str__()


# 3. ПІДХІД З ДЕСКРИПТОРАМИ
class PriceDescriptor:
    """Дескриптор для контролю доступу до атрибута price."""

    def __init__(self, default_value: float = 0.0) -> None:
        """Ініціалізує дескриптор з значенням за замовчуванням."""
        self.default_value = default_value
        self.name = None  # Буде встановлено через __set_name__

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Автоматично встановлює ім'я атрибута (Python 3.6+).

        Args:
            owner: Клас-власник дескриптора
            name: Ім'я атрибута
        """
        self.name = f'_{name}'  # price

    def __get__(self, obj: object, objtype: type = None) -> Union[float, 'PriceDescriptor']:
        """
        Getter дескриптора.

        Args:
            obj: Екземпляр об'єкта
            objtype: Тип об'єкта

        Returns:
            Union[float, PriceDescriptor]: Значення ціни або сам дескриптор
        """
        if obj is None:
            return self
        return getattr(obj, self.name, self.default_value)  # getattr(object, name[, default])

    def __set__(self, obj: object, value: float) -> None:
        """
        Setter дескриптора з валідацією.

        Args:
            obj: Екземпляр об'єкта
            value: Нове значення ціни

        Raises:
            ValueError: Якщо ціна від'ємна
            TypeError: Якщо значення не є числом
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Ціна повинна бути числом")
        if value < 0:
            raise ValueError("Ціна не може бути від'ємною")
        setattr(obj, self.name, float(value))

    def __delete__(self, obj: object) -> None:
        """
        Deleter дескриптора.

        Args:
            obj: Екземпляр об'єкта
        """
        print("Видалення ціни через дескриптор")
        setattr(obj, self.name, self.default_value)


class ProductWithDescriptor:
    """Клас Product з використанням дескриптора для атрибута price."""
    price = PriceDescriptor()

    def __init__(self, name: str, price: float) -> None:
        """
        Ініціалізує товар з назвою та ціною.

        Args:
            name: Назва товару
            price: Ціна товару (повинна бути >= 0)

        Raises:
            ValueError: Якщо ціна від'ємна
        """
        self.name = name
        self.price = price  # Використовується дескриптор для валідації

    def __str__(self) -> str:
        return f"ProductWithDescriptor(name='{self.name}', price={self.price})"

    def __repr__(self) -> str:
        return self.__str__()


# -----------------------------------------------------------------------
def test_product_class(product_class: type, class_name: str) -> None:
    """
    Тестує клас Product з різними реалізаціями.

    Args:
        product_class: Клас для тестування
        class_name: Назва класу для виводу
    """
    print(f"\n{'=' * 50}")
    print(f"ТЕСТУВАННЯ: {class_name}")
    print('=' * 50)

    try:
        # Створення об'єкта з валідною ціною
        print("1. Створення товару з валідною ціною:")
        product = product_class("Laptop", 1500.0)
        print(f"   Створено: {product}")

        # Отримання ціни (різні способи для різних класів)
        print("\n2. Отримання ціни:")
        if hasattr(product, 'get_price'):
            # Для класу з геттерами/сеттерами
            price = product.get_price()
            print(f"   product.get_price() = {price}")
        else:
            # Для класів з property та дескрипторами
            price = product.price
            print(f"   product.price = {price}")

        # Зміна ціни на валідне значення
        print("\n3. Зміна ціни на валідне значення:")
        if hasattr(product, 'set_price'):
            # Для класу з геттерами/сеттерами
            product.set_price(2000.0)
            print(f"   product.set_price(2000.0)")
            print(f"   Нова ціна: {product.get_price()}")
        else:
            # Для класів з property та дескрипторами
            product.price = 2000.0
            print(f"   product.price = 2000.0")
            print(f"   Нова ціна: {product.price}")

        # Спроба встановити від'ємну ціну
        print("\n4. Спроба встановити від'ємну ціну:")
        try:
            if hasattr(product, 'set_price'):
                product.set_price(-100.0)
            else:
                product.price = -100.0
            print("   ПОМИЛКА: Від'ємна ціна!")
        except ValueError as e:
            print(f"  Правильно спрацювала валідація: {e}")
        except Exception as e:
            print(f"  Неочікувана помилка: {e}")

        # Спроба встановити неправильний тип
        print("\n5. Спроба встановити неправильний тип:")
        try:
            if hasattr(product, 'set_price'):
                product.set_price("invalid")
            else:
                product.price = "invalid"
            print("   ПОМИЛКА: Неправильний тип!")
        except TypeError as e:
            print(f"   Правильно спрацювала валідація типу: {e}")
        except Exception as e:
            print(f"   Неочікувана помилка: {e}")

    except Exception as e:
        print(f" Критична помилка при тестуванні {class_name}: {e}")


def performance_comparison() -> None:
    """Порівняння продуктивності різних підходів."""
    import time

    print(f"\n{'=' * 50}")
    print("ПОРІВНЯННЯ ПРОДУКТИВНОСТІ")
    print('=' * 50)

    iterations = 100000

    # Тест геттерів/сеттерів
    start_time = time.time()
    product1 = ProductWithGetSet("Test", 100.0)
    for _ in range(iterations):
        product1.set_price(150.0)
        _ = product1.get_price()
    getset_time = time.time() - start_time

    # Тест property
    start_time = time.time()
    product2 = ProductWithProperty("Test", 100.0)
    for _ in range(iterations):
        product2.price = 150.0
        _ = product2.price
    property_time = time.time() - start_time

    # Тест дескрипторів
    start_time = time.time()
    product3 = ProductWithDescriptor("Test", 100.0)
    for _ in range(iterations):
        product3.price = 150.0
        _ = product3.price
    descriptor_time = time.time() - start_time

    print(f"Геттери/Сеттери:  {getset_time:.4f}s")
    print(f"Property:         {property_time:.4f}s")
    print(f"Дескриптори:      {descriptor_time:.4f}s")


if True:
    """Основна функція для демонстрації всіх підходів."""
    print("ДЕМОНСТРАЦІЯ РІЗНИХ ПІДХОДІВ ДО РОБОТИ З АТРИБУТАМИ")

    # Тестування всіх класів
    test_product_class(ProductWithGetSet, "ProductWithGetSet (Геттери/Сеттери)")
    test_product_class(ProductWithProperty, "ProductWithProperty (@property)")
    test_product_class(ProductWithDescriptor, "ProductWithDescriptor (Дескриптори)")

    # Порівняння продуктивності
    performance_comparison()
