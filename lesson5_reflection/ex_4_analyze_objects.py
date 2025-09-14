from typing import Any, Dict, List, Tuple
import inspect
from collections import defaultdict


def analyze_object(obj: Any) -> None:
    """
    Аналізує будь-який об'єкт та виводить детальну інформацію про нього.

    Args:
        obj (Any): Об'єкт для аналізу.
    """
    print("=" * 80)
    print(f"АНАЛІЗ ОБ'ЄКТА: {repr(obj)}")
    print("=" * 80)

    # 1. Тип об'єкта
    _analyze_object_type(obj)

    # 2. Список всіх методів та атрибутів
    _analyze_attributes_and_methods(obj)

    # 3. Тип кожного атрибута
    _analyze_attribute_types(obj)

    # 4. Додаткова інформація
    _analyze_additional_info(obj)


def _analyze_object_type(obj: Any) -> None:
    """Аналізує тип об'єкта."""
    print("\n1. ТИП ОБ'ЄКТА:")
    print("-" * 40)

    obj_type = type(obj)
    print(f"   Тип: {obj_type}")
    print(f"   Ім'я класу: {obj_type.__name__}")
    print(f"   Модуль: {obj_type.__module__}")
    print(f"   Повне ім'я: {obj_type.__module__}.{obj_type.__qualname__}")

    # MRO (Method Resolution Order)
    mro = [cls.__name__ for cls in obj_type.__mro__]
    print(f"   MRO: {' -> '.join(mro)}")

    # Базові класи
    if obj_type.__bases__:
        bases = [base.__name__ for base in obj_type.__bases__]
        print(f"   Базові класи: {', '.join(bases)}")
    else:
        print("   Базові класи: немає")


def _analyze_attributes_and_methods(obj: Any) -> None:
    """Аналізує атрибути та методи об'єкта."""
    print("\n2. АТРИБУТИ ТА МЕТОДИ:")
    print("-" * 40)

    # Отримуємо всі атрибути
    all_attrs = dir(obj)

    # Категоризуємо атрибути
    categories = {
        'Магічні методи': [],
        'Публічні методи': [],
        'Приватні методи': [],
        'Властивості (properties)': [],
        'Атрибути даних': [],
        'Модулі/класи': []
    }

    for attr_name in all_attrs:
        try:
            attr_value = getattr(obj, attr_name)
        except (AttributeError, Exception):
            continue

        # Категоризація
        if attr_name.startswith('__') and attr_name.endswith('__'):
            categories['Магічні методи'].append(attr_name)
        elif attr_name.startswith('_'):
            if callable(attr_value):
                categories['Приватні методи'].append(attr_name)
            else:
                categories['Атрибути даних'].append(attr_name)
        elif isinstance(attr_value, property):
            categories['Властивості (properties)'].append(attr_name)
        elif callable(attr_value):
            categories['Публічні методи'].append(attr_name)
        elif inspect.ismodule(attr_value) or inspect.isclass(attr_value):
            categories['Модулі/класи'].append(attr_name)
        else:
            categories['Атрибути даних'].append(attr_name)

    # Виводимо категорії
    for category, attrs in categories.items():
        if attrs:
            print(f"\n   {category} ({len(attrs)}):")
            for attr in attrs[:10]:  # Обмежуємо до 10 для читабельності
                print(f"     • {attr}")
            if len(attrs) > 10:
                print(f"     ... та ще {len(attrs) - 10}")


def _analyze_attribute_types(obj: Any) -> None:
    """Аналізує типи атрибутів об'єкта."""
    print("\n3. ТИПИ АТРИБУТІВ:")
    print("-" * 40)

    # Групуємо атрибути за типами
    type_groups = defaultdict(list)

    # Отримуємо лише не-магічні атрибути для кращої читабельності
    attrs_to_check = [attr for attr in dir(obj)
                      if not (attr.startswith('__') and attr.endswith('__'))]

    for attr_name in attrs_to_check:
        try:
            attr_value = getattr(obj, attr_name)
            attr_type = type(attr_value).__name__

            # Додаткова інформація про тип
            type_info = attr_type

            if callable(attr_value):
                if inspect.ismethod(attr_value):
                    type_info += " (метод)"
                elif inspect.isfunction(attr_value):
                    type_info += " (функція)"
                elif inspect.isbuiltin(attr_value):
                    type_info += " (вбудована функція)"
                else:
                    type_info += " (callable)"

            type_groups[type_info].append(attr_name)

        except (AttributeError, Exception) as e:
            type_groups[f"ERROR: {type(e).__name__}"].append(attr_name)

    # Виводимо групи типів
    for type_name, attrs in sorted(type_groups.items()):
        print(f"\n   {type_name} ({len(attrs)}):")
        for attr in attrs[:8]:  # Обмежуємо для читабельності
            try:
                attr_value = getattr(obj, attr)
                if not callable(attr_value):
                    print(f"     • {attr} = {repr(attr_value)}")
                else:
                    print(f"     • {attr}")
            except:
                print(f"     • {attr} (недоступний)")
        if len(attrs) > 8:
            print(f"     ... та ще {len(attrs) - 8}")


def _analyze_additional_info(obj: Any) -> None:
    """Додаткова інформація про об'єкт."""
    print("\n4. ДОДАТКОВА ІНФОРМАЦІЯ:")
    print("-" * 40)

    # Розмір об'єкта
    try:
        size = obj.__sizeof__()
        print(f"   Розмір в пам'яті: {size} байт")
    except:
        print("   Розмір в пам'яті: недоступний")

    # ID об'єкта
    print(f"   ID об'єкта: {id(obj)}")

    # Хеш (якщо можливо)
    try:
        hash_value = hash(obj)
        print(f"   Хеш: {hash_value}")
    except TypeError:
        print("   Хеш: об'єкт не хешується")

    # __dict__ якщо існує
    if hasattr(obj, '__dict__'):
        instance_attrs = obj.__dict__
        print(f"   Атрибути екземпляра (__dict__): {len(instance_attrs)}")
        if instance_attrs:
            for key, value in list(instance_attrs.items())[:5]:
                print(f"     • {key}: {type(value).__name__} = {repr(value)}")
            if len(instance_attrs) > 5:
                print(f"     ... та ще {len(instance_attrs) - 5}")

    # __slots__ якщо існує
    if hasattr(obj.__class__, '__slots__'):
        slots = obj.__class__.__slots__
        print(f"   Слоти (__slots__): {slots}")

    # Документація
    if hasattr(obj, '__doc__') and obj.__doc__:
        doc = obj.__doc__.strip()
        if doc:
            print(f"   Документація: {doc[:100]}{'...' if len(doc) > 100 else ''}")


# Демонстрація роботи функції
if __name__ == "__main__":
    # Тестові класи та об'єкти
    class Person:
        """Клас для представлення особи."""

        species = "Homo sapiens"  # Атрибут класу

        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age
            self._private_data = "секретні дані"

        def greet(self) -> str:
            """Привітання."""
            return f"Привіт, я {self.name}!"

        def _private_method(self) -> str:
            """Приватний метод."""
            return self._private_data

        @property
        def info(self) -> str:
            """Інформація про особу."""
            return f"{self.name}, {self.age} років"

        @staticmethod
        def get_species() -> str:
            """Статичний метод."""
            return Person.species

        @classmethod
        def create_adult(cls, name: str) -> 'Person':
            """Класовий метод."""
            return cls(name, 18)


    class Student(Person):
        """Студент - наслідник Person."""

        def __init__(self, name: str, age: int, university: str):
            super().__init__(name, age)
            self.university = university

        def study(self) -> str:
            """Навчання."""
            return f"{self.name} навчається в {self.university}"


    # Тестування з різними об'єктами
    print("🔍 ТЕСТУВАННЯ ФУНКЦІЇ АНАЛІЗУ ОБ'ЄКТІВ")
    print("\n" + "🟢 ТЕСТ 1: Простий об'єкт Person")
    person = Person("Іван", 25)
    analyze_object(person)

    print("\n" + "🟡 ТЕСТ 2: Об'єкт-наслідник Student")
    student = Student("Марія", 20, "КПІ")
    analyze_object(student)

    print("\n" + "🔵 ТЕСТ 3: Вбудований тип - список")
    test_list = [1, 2, 3, "hello", {"key": "value"}]
    analyze_object(test_list)

    print("\n" + "🟠 ТЕСТ 4: Словник")
    test_dict = {"name": "Петро", "age": 30, "scores": [85, 90, 78]}
    analyze_object(test_dict)

    print("\n" + "🟣 ТЕСТ 5: Функція")


    def sample_function(x: int, y: str = "default") -> str:
        """Зразкова функція для тестування."""
        return f"{x}: {y}"


    analyze_object(sample_function)

    print("\n" + "⚫ ТЕСТ 6: Клас (не екземпляр)")
    analyze_object(Person)

    print("\n" + "=" * 80)
    print("✅ ТЕСТУВАННЯ ЗАВЕРШЕНО")
    print("=" * 80)