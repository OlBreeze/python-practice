# __mro__ (Method Resolution Order) — это порядок разрешения методов в Python.
# Он определяет, в какой последовательности Python ищет методы и атрибуты при наследовании классов.

from typing import List, Type


def demonstrate_simple_mro():
    """Демонстрация простого MRO с одиночным наследованием."""
    print("=" * 60)
    print("1. ПРОСТОЕ НАСЛЕДОВАНИЕ (MRO)")
    print("=" * 60)

    class Animal:
        def speak(self):
            return "Животное издает звук"

        def info(self):
            return "Я животное"

    class Dog(Animal):
        def speak(self):
            return "Гав!"

        def bark(self):
            return "Лай!"

    class Puppy(Dog):
        def speak(self):
            return "Тяв-тяв!"

        def play(self):
            return "Играю!"

    # Создаем экземпляр
    puppy = Puppy()

    print("Иерархия классов:")
    print("Animal -> Dog -> Puppy")

    print(f"\nMRO для класса Puppy:")
    for i, cls in enumerate(Puppy.__mro__):
        print(f"   {i + 1}. {cls.__name__} ({cls})")

    print(f"\nПоиск метода speak():")
    print(f"   puppy.speak() = '{puppy.speak()}'")
    print("   ↳ Найден в классе Puppy (первый в MRO)")

    print(f"\nПоиск метода info() (не переопределен в Puppy/Dog):")
    print(f"   puppy.info() = '{puppy.info()}'")
    print("   ↳ Найден в классе Animal (третий в MRO)")


def demonstrate_multiple_inheritance():
    """Демонстрация множественного наследования и алгоритма C3."""
    print("\n" + "=" * 60)
    print("2. МНОЖЕСТВЕННОЕ НАСЛЕДОВАНИЕ")
    print("=" * 60)

    class A:
        def method(self):
            return "Метод из A"

        def a_method(self):
            return "Только в A"

    class B(A):
        def method(self):
            return "Метод из B"

        def b_method(self):
            return "Только в B"

    class C(A):
        def method(self):
            return "Метод из C"

        def c_method(self):
            return "Только в C"

    class D(B, C):  # Множественное наследование
        def d_method(self):
            return "Только в D"

    print("Иерархия наследования:")
    print("     A")
    print("    / \\")
    print("   B   C")
    print("    \\ /")
    print("     D")

    print(f"\nMRO для класса D:")
    for i, cls in enumerate(D.__mro__):
        print(f"   {i + 1}. {cls.__name__}")

    # Создаем экземпляр
    d = D()

    print(f"\nПоиск методов:")
    print(f"   d.method() = '{d.method()}'")
    print("   ↳ Найден в B (второй в MRO, раньше чем C)")
    print(f"   d.a_method() = '{d.a_method()}'")
    print("   ↳ Найден в A (последний в MRO)")


def demonstrate_diamond_problem():
    """Демонстрация проблемы ромба и ее решения через C3."""
    print("\n" + "=" * 60)
    print("3. ПРОБЛЕМА РОМБА (Diamond Problem)")
    print("=" * 60)

    class Vehicle:
        def __init__(self):
            print("Инициализация Vehicle")
            self.engine = "базовый двигатель"

        def start(self):
            return f"Запуск {self.engine}"

    class Car(Vehicle):
        def __init__(self):
            print("Инициализация Car")
            super().__init__()  # Правильное использование super()
            self.wheels = 4

        def drive(self):
            return "Едем по дороге"

    class Boat(Vehicle):
        def __init__(self):
            print("Инициализация Boat")
            super().__init__()
            self.propeller = True

        def sail(self):
            return "Плывем по воде"

    class AmphibiousVehicle(Car, Boat):
        def __init__(self):
            print("Инициализация AmphibiousVehicle")
            super().__init__()  # super() использует MRO!

        def go_anywhere(self):
            return f"{self.drive()} или {self.sail()}"

    print("Проблема ромба:")
    print("      Vehicle")
    print("      /    \\")
    print("    Car    Boat")
    print("      \\    /")
    print("   AmphibiousVehicle")

    print(f"\nMRO для AmphibiousVehicle:")
    for i, cls in enumerate(AmphibiousVehicle.__mro__):
        print(f"   {i + 1}. {cls.__name__}")

    print(f"\nСоздание экземпляра AmphibiousVehicle:")
    amphibious = AmphibiousVehicle()

    print(f"\nРезультат:")
    print(f"   amphibious.start() = '{amphibious.start()}'")
    print(f"   amphibious.go_anywhere() = '{amphibious.go_anywhere()}'")
    print(f"   amphibious.wheels = {amphibious.wheels}")
    print(f"   amphibious.propeller = {amphibious.propeller}")


def demonstrate_mro_methods():
    """Демонстрация методов для работы с MRO."""
    print("\n" + "=" * 60)
    print("4. МЕТОДЫ РАБОТЫ С MRO")
    print("=" * 60)

    class Base:
        def method(self):
            return "Base"

    class Mixin1:
        def method(self):
            return "Mixin1"

        def mixin1_method(self):
            return "Только Mixin1"

    class Mixin2:
        def method(self):
            return "Mixin2"

        def mixin2_method(self):
            return "Только Mixin2"

    class Final(Mixin1, Mixin2, Base):
        pass

    print("1. Получение MRO разными способами:")
    print(f"   Final.__mro__:")
    for cls in Final.__mro__:
        print(f"     {cls.__name__}")

    print(f"\n   Final.mro() (то же самое):")
    for cls in Final.mro():
        print(f"     {cls.__name__}")

    print(f"\n2. Проверка порядка наследования:")
    print(f"   issubclass(Final, Mixin1): {issubclass(Final, Mixin1)}")
    print(f"   issubclass(Final, Base): {issubclass(Final, Base)}")

    obj = Final()
    print(f"\n3. Вызов методов:")
    print(f"   obj.method() = '{obj.method()}'")
    print("   ↳ Найден в Mixin1 (первый в MRO после Final)")


def demonstrate_super_with_mro():
    """Демонстрация работы super() с MRO."""
    print("\n" + "=" * 60)
    print("5. SUPER() И MRO")
    print("=" * 60)

    class A:
        def method(self):
            print("A.method()")
            return "A"

    class B(A):
        def method(self):
            print("B.method() - вызываем super()")
            result = super().method()  # Вызывает следующий в MRO
            return f"B -> {result}"

    class C(A):
        def method(self):
            print("C.method() - вызываем super()")
            result = super().method()
            return f"C -> {result}"

    class D(B, C):
        def method(self):
            print("D.method() - вызываем super()")
            result = super().method()
            return f"D -> {result}"

    print(f"MRO для D: {[cls.__name__ for cls in D.__mro__]}")

    print(f"\nВызов d.method():")
    d = D()
    result = d.method()
    print(f"Результат: {result}")

    print(f"\nОбъяснение цепочки вызовов:")
    print("1. D.method() вызывает super() -> B.method()")
    print("2. B.method() вызывает super() -> C.method()")
    print("3. C.method() вызывает super() -> A.method()")
    print("4. A.method() - конец цепочки")


def analyze_mro_conflicts():
    """Анализ конфликтов в MRO."""
    print("\n" + "=" * 60)
    print("6. КОНФЛИКТЫ В MRO")
    print("=" * 60)

    print("Попытка создать невозможный MRO:")

    class X:
        pass

    class Y:
        pass

    class A(X, Y):
        pass

    class B(Y, X):
        pass  # Обратный порядок!

    try:
        # Это должно вызвать ошибку
        class C(A, B):
            pass

        print("Класс C создан успешно")
        print(f"MRO: {[cls.__name__ for cls in C.__mro__]}")
    except TypeError as e:
        print(f"❌ Ошибка: {e}")
        print("Причина: невозможно создать линейный порядок,")
        print("который бы удовлетворял всем ограничениям наследования")

    print(f"\nПояснение:")
    print(f"A требует порядок: X, затем Y")
    print(f"B требует порядок: Y, затем X")
    print(f"Эти требования противоречат друг другу!")


def practical_mro_usage():
    """Практические примеры использования MRO."""
    print("\n" + "=" * 60)
    print("7. ПРАКТИЧЕСКОЕ ИСПОЛЬЗОВАНИЕ MRO")
    print("=" * 60)

    # Миксины в правильном порядке
    class LogMixin:
        def save(self):
            print(f"[LOG] Сохранение {self.__class__.__name__}")
            return super().save()

    class ValidationMixin:
        def save(self):
            print(f"[VALIDATION] Валидация {self.__class__.__name__}")
            if hasattr(self, 'validate') and not self.validate():
                raise ValueError("Валидация не прошла")
            return super().save()

    class Model:
        def save(self):
            print(f"[MODEL] Сохранение в базу данных")
            return True

        def validate(self):
            return True

    # Правильный порядок миксинов: Log -> Validation -> Model
    class User(LogMixin, ValidationMixin, Model):
        def __init__(self, name):
            self.name = name

    print("Правильный порядок миксинов:")
    print(f"MRO: {[cls.__name__ for cls in User.__mro__]}")

    user = User("Иван")
    print(f"\nВызов user.save():")
    result = user.save()
    print(f"Результат: {result}")


def mro_debugging_tools():
    """Инструменты для отладки MRO."""
    print("\n" + "=" * 60)
    print("8. ИНСТРУМЕНТЫ ОТЛАДКИ MRO")
    print("=" * 60)

    def print_mro_tree(cls: Type, indent: int = 0) -> None:
        """Выводит дерево MRO в удобном формате."""
        print("  " * indent + f"├─ {cls.__name__}")
        for base in cls.__bases__:
            print_mro_tree(base, indent + 1)

    def analyze_method_source(cls: Type, method_name: str) -> None:
        """Анализирует, где определен метод в иерархии MRO."""
        print(f"\nПоиск метода '{method_name}' в MRO:")
        for i, mro_cls in enumerate(cls.__mro__):
            if hasattr(mro_cls, method_name):
                method = getattr(mro_cls, method_name)
                if method_name in mro_cls.__dict__:
                    print(f"   ✅ {i + 1}. {mro_cls.__name__} - ОПРЕДЕЛЕН ЗДЕСЬ")
                    break
                else:
                    print(f"   ↪ {i + 1}. {mro_cls.__name__} - наследует")
            else:
                print(f"   ❌ {i + 1}. {mro_cls.__name__} - нет метода")

    # Пример сложной иерархии
    class A:
        def method(self): pass

    class B(A):
        def method(self): pass

    class C(A):
        pass

    class D(B, C):
        pass

    print("Дерево наследования для класса D:")
    print_mro_tree(D)

    analyze_method_source(D, 'method')


if __name__ == "__main__":
    demonstrate_simple_mro()
    demonstrate_multiple_inheritance()
    demonstrate_diamond_problem()
    demonstrate_mro_methods()
    demonstrate_super_with_mro()
    analyze_mro_conflicts()
    practical_mro_usage()
    mro_debugging_tools()

    print("\n" + "=" * 60)
    print("ЗАКЛЮЧЕНИЕ О MRO")
    print("=" * 60)
    print("MRO (Method Resolution Order) определяет:")
    print("• В каком порядке Python ищет методы и атрибуты")
    print("• Как работает super() в множественном наследовании")
    print("• Решает проблему ромба (diamond problem)")
    print("• Использует алгоритм C3 linearization")
    print("\nКлючевые правила:")
    print("• Дочерние классы идут перед родительскими")
    print("• При множественном наследовании - слева направо")
    print("• Каждый класс появляется в MRO только один раз")
    print("• object всегда последний в MRO")