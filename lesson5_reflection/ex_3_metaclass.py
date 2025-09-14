from typing import Any, Dict, Type, Callable
import inspect


def basic_metaclass_concept():
    """Основная концепция метаклассов."""
    print("=" * 60)
    print("ОСНОВНАЯ КОНЦЕПЦИЯ МЕТАКЛАССОВ")
    print("=" * 60)

    # В Python все является объектами, включая классы
    class MyClass:
        pass

    obj = MyClass()

    print("1. Иерархия типов:")
    print(f"   type(obj): {type(obj)}")  # <class '__main__.MyClass'>
    print(f"   type(MyClass): {type(MyClass)}")  # <class 'type'>
    print(f"   type(type): {type(type)}")  # <class 'type'>

    print(f"\n2. Проверка isinstance:")
    print(f"   isinstance(obj, MyClass): {isinstance(obj, MyClass)}")
    print(f"   isinstance(MyClass, type): {isinstance(MyClass, type)}")
    print(f"   isinstance(type, type): {isinstance(type, type)}")

    print(f"\n3. type() может создавать классы динамически:")
    # Синтаксис: type(name, bases, dict)
    DynamicClass = type('DynamicClass', (), {'attr': 'value'})
    dynamic_obj = DynamicClass()
    print(f"   DynamicClass.attr: {DynamicClass.attr}")
    print(f"   dynamic_obj.attr: {dynamic_obj.attr}")
    print(f"   type(DynamicClass): {type(DynamicClass)}")


def simple_metaclass_example():
    """Простой пример метакласса."""
    print("\n" + "=" * 60)
    print("ПРОСТОЙ ПРИМЕР МЕТАКЛАССА")
    print("=" * 60)

    class SimpleMeta(type):
        """Простой метакласс, который добавляет атрибут к создаваемым классам."""

        def __new__(cls, name: str, bases: tuple, attrs: dict) -> Type:
            """Создает новый класс."""
            print(f"   Создается класс: {name}")
            print(f"   Базовые классы: {bases}")
            print(f"   Атрибуты: {list(attrs.keys())}")

            # Добавляем атрибут ко всем создаваемым классам
            attrs['created_by_meta'] = True
            attrs['class_id'] = f"{name}_{id(cls)}"

            return super().__new__(cls, name, bases, attrs)

        def __init__(cls, name: str, bases: tuple, attrs: dict) -> None:
            """Инициализирует созданный класс."""
            print(f"   Инициализируется класс: {name}")
            super().__init__(name, bases, attrs)

    print("1. Создание класса с метаклассом:")

    class MyClass(metaclass=SimpleMeta):
        def __init__(self, value):
            self.value = value

        def get_value(self):
            return self.value

    print(f"\n2. Проверяем добавленные атрибуты:")
    print(f"   MyClass.created_by_meta: {MyClass.created_by_meta}")
    print(f"   MyClass.class_id: {MyClass.class_id}")

    print(f"\n3. Создаем объект:")
    obj = MyClass("test")
    print(f"   obj.value: {obj.value}")
    print(f"   obj.get_value(): {obj.get_value()}")
    print(f"   obj.created_by_meta: {obj.created_by_meta}")  # Наследуется от класса


def validation_metaclass():
    """Метакласс для валидации классов."""
    print("\n" + "=" * 60)
    print("МЕТАКЛАСС ДЛЯ ВАЛИДАЦИИ")
    print("=" * 60)

    class ValidatedMeta(type):
        """Метакласс, который валидирует структуру класса."""

        def __new__(cls, name: str, bases: tuple, attrs: dict) -> Type:
            # Проверяем, что все методы имеют документацию
            for attr_name, attr_value in attrs.items():
                if (callable(attr_value) and
                        not attr_name.startswith('_') and
                        not inspect.getdoc(attr_value)):
                    raise ValueError(f"Метод {attr_name} в классе {name} должен иметь документацию!")

            # Проверяем наличие обязательных методов
            required_methods = getattr(attrs.get('__required_methods__'), '__iter__', lambda: [])()
            for method_name in required_methods:
                if method_name not in attrs:
                    raise ValueError(f"Класс {name} должен содержать метод {method_name}")

            return super().__new__(cls, name, bases, attrs)

    print("1. Создание валидного класса:")

    class ValidClass(metaclass=ValidatedMeta):
        __required_methods__ = ['process']

        def process(self):
            """Обрабатывает данные."""
            return "processed"

        def helper_method(self):
            """Вспомогательный метод."""
            pass

    print("   ✅ Класс создан успешно")

    print("\n2. Попытка создать невалидный класс:")
    try:
        class InvalidClass(metaclass=ValidatedMeta):
            __required_methods__ = ['process']

            def undocumented_method(self):  # Нет документации
                pass

    except ValueError as e:
        print(f"   ❌ Ошибка: {e}")


def singleton_metaclass():
    """Метакласс для реализации паттерна Singleton."""
    print("\n" + "=" * 60)
    print("SINGLETON ЧЕРЕЗ МЕТАКЛАСС")
    print("=" * 60)

    class SingletonMeta(type):
        """Метакласс для создания singleton классов."""
        _instances: Dict[Type, Any] = {}

        def __call__(cls, *args, **kwargs):
            """Переопределяем создание экземпляров."""
            if cls not in cls._instances:
                print(f"   Создается первый экземпляр {cls.__name__}")
                cls._instances[cls] = super().__call__(*args, **kwargs)
            else:
                print(f"   Возвращается существующий экземпляр {cls.__name__}")
            return cls._instances[cls]

    class Database(metaclass=SingletonMeta):
        def __init__(self, connection_string: str = "default"):
            self.connection_string = connection_string
            self.connected = False

        def connect(self):
            self.connected = True
            print(f"Подключение к БД: {self.connection_string}")

    print("1. Создание экземпляров Singleton:")
    db1 = Database("postgresql://localhost")
    db2 = Database("mysql://localhost")  # Аргументы игнорируются

    print(f"\n2. Проверка identity:")
    print(f"   db1 is db2: {db1 is db2}")
    print(f"   id(db1): {id(db1)}")
    print(f"   id(db2): {id(db2)}")
    print(f"   db1.connection_string: {db1.connection_string}")


def attribute_transformation_metaclass():
    """Метакласс для преобразования атрибутов."""
    print("\n" + "=" * 60)
    print("ПРЕОБРАЗОВАНИЕ АТРИБУТОВ")
    print("=" * 60)

    class UppercaseMeta(type):
        """Метакласс, который преобразует имена атрибутов в верхний регистр."""

        def __new__(cls, name: str, bases: tuple, attrs: dict) -> Type:
            # Преобразуем только не-callable публичные атрибуты в верхний регистр
            uppercase_attrs = {}

            for attr_name, attr_value in attrs.items():
                if not attr_name.startswith('_') and not callable(attr_value):
                    # Преобразуем только данные (не функции) в верхний регистр
                    new_name = attr_name.upper()
                    uppercase_attrs[new_name] = attr_value

                    # Создаем property для обратной совместимости
                    uppercase_attrs[attr_name] = property(
                        lambda self, name=new_name: getattr(self, name)
                    )
                else:
                    # Методы и приватные атрибуты оставляем как есть
                    uppercase_attrs[attr_name] = attr_value

            return super().__new__(cls, name, bases, uppercase_attrs)

    class Config(metaclass=UppercaseMeta):
        debug = True
        port = 8080
        host = "localhost"

        def get_url(self):
            return f"http://{self.HOST}:{self.PORT}"

    print("1. Преобразованные атрибуты (только данные):")
    config = Config()
    print(f"   Config.DEBUG: {Config.DEBUG}")
    print(f"   Config.PORT: {Config.PORT}")
    print(f"   Config.HOST: {Config.HOST}")

    print(f"\n2. Обратная совместимость:")
    print(f"   config.debug: {config.debug}")  # Работает через property
    print(f"   config.port: {config.port}")

    print(f"\n3. Методы работают нормально:")
    print(f"   config.get_url(): {config.get_url()}")  # Теперь работает!

    print(f"\n4. Проверим что было преобразовано:")
    all_attrs = [attr for attr in dir(Config) if not attr.startswith('_')]
    print(f"   Все публичные атрибуты: {all_attrs}")


def registry_metaclass():
    """Метакласс для автоматической регистрации классов."""
    print("\n" + "=" * 60)
    print("АВТОМАТИЧЕСКАЯ РЕГИСТРАЦИЯ КЛАССОВ")
    print("=" * 60)

    class RegistryMeta(type):
        """Метакласс, который автоматически регистрирует классы."""
        registry: Dict[str, Type] = {}

        def __new__(cls, name: str, bases: tuple, attrs: dict) -> Type:
            new_class = super().__new__(cls, name, bases, attrs)

            # Регистрируем класс, если он не абстрактный
            if not attrs.get('__abstract__', False):
                cls.registry[name] = new_class
                print(f"   Зарегистрирован класс: {name}")

            return new_class

        @classmethod
        def get_registered_classes(cls) -> Dict[str, Type]:
            """Возвращает все зарегистрированные классы."""
            return cls.registry.copy()

        @classmethod
        def create_instance(cls, class_name: str, *args, **kwargs) -> Any:
            """Создает экземпляр по имени класса."""
            if class_name not in cls.registry:
                raise ValueError(f"Класс {class_name} не зарегистрирован")
            return cls.registry[class_name](*args, **kwargs)

    print("1. Создание классов с автоматической регистрацией:")

    class BaseHandler(metaclass=RegistryMeta):
        __abstract__ = True  # Не регистрируется

        def handle(self):
            raise NotImplementedError

    class EmailHandler(BaseHandler):
        def handle(self):
            return "Отправка email"

    class SMSHandler(BaseHandler):
        def handle(self):
            return "Отправка SMS"

    class PushHandler(BaseHandler):
        def handle(self):
            return "Push уведомление"

    print(f"\n2. Зарегистрированные классы:")
    for name, cls in RegistryMeta.get_registered_classes().items():
        print(f"   {name}: {cls}")

    print(f"\n3. Создание экземпляров по имени:")
    email_handler = RegistryMeta.create_instance('EmailHandler')
    print(f"   EmailHandler.handle(): {email_handler.handle()}")

    sms_handler = RegistryMeta.create_instance('SMSHandler')
    print(f"   SMSHandler.handle(): {sms_handler.handle()}")


def metaclass_vs_alternatives():
    """Сравнение метаклассов с альтернативами."""
    print("\n" + "=" * 60)
    print("МЕТАКЛАССЫ VS АЛЬТЕРНАТИВЫ")
    print("=" * 60)

    print("1. Метакласс для добавления методов:")

    class MethodAdderMeta(type):
        def __new__(cls, name, bases, attrs):
            def auto_str(self):
                return f"{name}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

            attrs['__str__'] = auto_str
            return super().__new__(cls, name, bases, attrs)

    class Person1(metaclass=MethodAdderMeta):
        def __init__(self, name, age):
            self.name = name
            self.age = age

    print("2. Альтернатива - декоратор класса:")

    def add_str_method(cls):
        def auto_str(self):
            return f"{cls.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

        cls.__str__ = auto_str
        return cls

    @add_str_method
    class Person2:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    print("3. Альтернатива - наследование:")

    class AutoStrMixin:
        def __str__(self):
            return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    class Person3(AutoStrMixin):
        def __init__(self, name, age):
            self.name = name
            self.age = age

    print("Сравнение результатов:")
    p1 = Person1("Анна", 25)
    p2 = Person2("Борис", 30)
    p3 = Person3("Виктор", 35)

    print(f"   Метакласс: {p1}")
    print(f"   Декоратор: {p2}")
    print(f"   Миксин: {p3}")


def when_to_use_metaclasses():
    """Когда использовать метаклассы."""
    print("\n" + "=" * 60)
    print("КОГДА ИСПОЛЬЗОВАТЬ МЕТАКЛАССЫ")
    print("=" * 60)

    print("✅ ИСПОЛЬЗУЙТЕ метаклассы для:")
    print("   • Модификации СОЗДАНИЯ класса (не экземпляров)")
    print("   • Валидации структуры классов")
    print("   • Автоматической регистрации классов")
    print("   • Реализации паттернов на уровне классов")
    print("   • Создания DSL (Domain Specific Languages)")

    print("\n❌ НЕ ИСПОЛЬЗУЙТЕ метаклассы для:")
    print("   • Простого добавления методов (используйте декораторы)")
    print("   • Модификации поведения экземпляров")
    print("   • Того, что можно сделать наследованием")
    print("   • Простых случаев (принцип KISS)")

    print("\n💡 ПРАВИЛО: \"Metaclasses are deeper magic than 99% of users")
    print("   should ever worry about\" - Tim Peters")

    print("\n🎯 АЛЬТЕРНАТИВЫ метаклассам:")
    print("   • Декораторы классов: @decorator")
    print("   • Миксины и множественное наследование")
    print("   • __init_subclass__() (Python 3.6+)")
    print("   • __new__() в обычных классах")


def init_subclass_alternative():
    """Альтернатива метаклассам - __init_subclass__."""
    print("\n" + "=" * 60)
    print("АЛЬТЕРНАТИВА: __init_subclass__")
    print("=" * 60)

    class ValidatedBase:
        """Базовый класс с валидацией подклассов."""

        def __init_subclass__(cls, **kwargs):
            """Вызывается при создании подкласса."""
            super().__init_subclass__(**kwargs)

            # Проверяем наличие обязательных атрибутов
            required_attrs = getattr(cls, '__required_attrs__', [])
            for attr in required_attrs:
                if not hasattr(cls, attr):
                    raise ValueError(f"Класс {cls.__name__} должен определить {attr}")

            print(f"Валидация подкласса {cls.__name__} прошла успешно")

    class APIClient(ValidatedBase):
        __required_attrs__ = ['BASE_URL', 'API_VERSION']

        BASE_URL = "https://api.example.com"
        API_VERSION = "v1"

        def make_request(self):
            return f"Request to {self.BASE_URL}/{self.API_VERSION}"

    print("__init_subclass__ - более простая альтернатива метаклассам!")
    client = APIClient()
    print(f"client.make_request(): {client.make_request()}")


if __name__ == "__main__":
    basic_metaclass_concept()
    simple_metaclass_example()
    validation_metaclass()
    singleton_metaclass()
    attribute_transformation_metaclass()
    registry_metaclass()
    metaclass_vs_alternatives()
    when_to_use_metaclasses()
    init_subclass_alternative()

    print("\n" + "=" * 60)
    print("ЗАКЛЮЧЕНИЕ")
    print("=" * 60)
    print("Метаклассы - это мощный, но сложный инструмент Python.")
    print("Используйте их только когда без них действительно не обойтись!")
    print("В 99% случаев есть более простые альтернативы.")