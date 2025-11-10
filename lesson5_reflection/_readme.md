# Конспект лекції: Метапрограмування та інтроспекція в Python

## 1. Повторення: Винятки (Exceptions)

### Основні концепції
- **Exception** - базовий клас для створення власних винятків
- **`raise`** - оператор для викидання винятків
- **`assert`** - використовується для тестування, не впливає на продакшн код

### Ієрархія винятків
```
object → BaseException → Exception → [Конкретні винятки]
```

**BaseException** розширює можливості `object` та додає:
- Службову інформацію
- Можливість додавати traceback
- Контекст для логування

## 2. Дослідження об'єктів (Introspection)

### Вбудовані функції

#### `type()`
```python
digit = 10
type(digit)  # <class 'int'>

# Для класів
type(MyClass)  # <class 'type'>
type(MyClass())  # <class '__main__.MyClass'>
```

**Важливо**: Якщо `type()` повертає `<class 'type'>` - це клас (шаблон), а не екземпляр.

#### `isinstance()`
```python
isinstance(obj, ClassName)  # True/False
isinstance(10, int)  # True
```

#### `issubclass()`
```python
issubclass(ChildClass, ParentClass)  # True/False
```

### Магічні атрибути

- **`__dict__`** - словник атрибутів об'єкта/класу
- **`__class__`** - посилання на клас об'єкта
- **`__doc__`** - документація
- **`__name__`** - ім'я класу/функції
- **`__module__`** - модуль, де визначено об'єкт

## 3. Метакласи (Metaclasses)

### Концепція
> **Метаклас** - це клас для класів. Якщо клас - це шаблон для створення об'єктів, то метаклас - це шаблон для створення класів.

### Структура створення об'єктів

```
1. __new__() - виділення пам'яті
2. __init__() - ініціалізація об'єкта
```

### Приклад метакласу

```python
class MetaPerson(type):
    def __repr__(cls):
        return 'Person'
    
    def __new__(mcs, name, bases, attrs):
        # Конвертуємо назви атрибутів у верхній регістр
        new_attrs = {}
        for key, value in attrs.items():
            if not key.startswith('__'):
                new_attrs[key.upper()] = value
            else:
                new_attrs[key] = value
        return super().__new__(mcs, name, bases, new_attrs)

class Person(metaclass=MetaPerson):
    count = 0
    
    def __init__(self, name):
        self.name = name
    
    def get_friends(self):
        return []
```

### Коли використовувати метакласи?

✅ **Валідація даних** перед створенням об'єкта
✅ **Модифікація поведінки** класу без зміни його коду
✅ **Патерн Singleton**
✅ **Логування**, кешування, додаткові перевірки

## 4. Динамічне створення класів

### Використання `type()`

```python
# Синтаксис: type(name, bases, dict)
MyType1 = type('MyType1', (), {'my_attr': 1})

# Еквівалентно:
class MyType1:
    my_attr = 1
```

### Параметри:
- **name** - ім'я класу
- **bases** - кортеж батьківських класів
- **dict** - словник атрибутів та методів

## 5. Робота з атрибутами

### Вбудовані функції

#### `hasattr(obj, name)`
```python
hasattr(instance, 'attribute')  # True/False
```

#### `getattr(obj, name, default=None)`
```python
value = getattr(instance, 'attribute', 'default_value')
```

#### `setattr(obj, name, value)`
```python
setattr(instance, 'new_attr', 100)
# Еквівалентно: instance.new_attr = 100
```

#### `delattr(obj, name)`
```python
delattr(instance, 'attribute')
# Еквівалентно: del instance.attribute
```

### Різниця між атрибутами класу та екземпляра

```python
class MyClass:
    class_attr = 1  # Атрибут класу
    
    def __init__(self, value):
        self.instance_attr = value  # Атрибут екземпляра

obj = MyClass(10)

# Атрибути екземпляра
obj.__dict__  # {'instance_attr': 10}

# Атрибути класу
MyClass.__dict__  # {..., 'class_attr': 1, ...}
```

**Правило LGB (Local → Global → Built-in)**:
- Спочатку шукається в екземплярі
- Потім у класі
- Потім у батьківських класах

## 6. Обмеження динамічних атрибутів: `__slots__`

### Проблема
Python дозволяє динамічно додавати атрибути, що споживає пам'ять.

### Рішення
```python
class Point3D:
    __slots__ = ('x', 'y', 'z')  # Фіксований список атрибутів
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

p = Point3D(1, 2, 3)
p.w = 4  # AttributeError! Неможливо додати новий атрибут
```

### Переваги `__slots__`:
✅ Економія пам'яті (немає `__dict__`)
✅ Захист від помилок
✅ Швидший доступ до атрибутів

## 7. Method Resolution Order (MRO)

### Проблема діаманта (Diamond Problem)

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")

class C(A):
    def method(self):
        print("C")

class D(B, C):  # Множинне успадкування
    pass

# Який метод викличеться?
D().method()  # B - перший у списку батьків
```

### Перевірка MRO

```python
D.__mro__  # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
D.mro()    # Те саме, але список
```

**Порядок розв'язання**: D → B → C → A → object

## 8. Динамічне виконання коду

### `eval()` - виконання виразів

```python
result = eval("2 + 2")  # 4
s = 3
eval("s + 1")  # 4
eval("str(10)")  # '10'
```

**Обмеження**: Тільки однорядкові вирази

### `exec()` - виконання складного коду

```python
code = """
for i in range(5):
    print(i ** 2)
"""
exec(code)
```

**Використання**: Динамічна генерація та виконання коду (наприклад, онлайн-тренажери)

## 9. Модуль `inspect`

### Дослідження модулів та класів

```python
import inspect
import my_module

# Отримати всі члени модуля
members = inspect.getmembers(my_module)

# Тільки класи
classes = inspect.getmembers(my_module, inspect.isclass)

# Тільки функції
functions = inspect.getmembers(my_module, inspect.isfunction)
```

### Отримання коду та документації

```python
# Отримати вихідний код
source = inspect.getsource(MyClass)
source = inspect.getsource(MyClass.method)

# Отримати документацію
doc = inspect.getdoc(MyClass)

# Сигнатура функції
sig = inspect.signature(function)
print(sig)  # (param1: int, param2: str) -> bool
```

### Різниця між методами та функціями

```python
class MyClass:
    @staticmethod
    def static_method():
        pass
    
    def instance_method(self):
        pass

# Для класу
inspect.getmembers(MyClass, inspect.isfunction)  # Обидва методи

# Для екземпляра
inspect.getmembers(instance, inspect.ismethod)  # Тільки instance_method
```

## 10. Інтроспекція vs Рефлексія

### Інтроспекція (Introspection)
**Дослідження** об'єктів без зміни:
- `type()`, `isinstance()`, `dir()`
- `__dict__`, `__class__`
- `inspect` модуль

### Рефлексія (Reflection)
**Динамічна зміна** об'єктів:
- `setattr()`, `delattr()`
- Динамічне створення класів через `type()`
- `eval()`, `exec()`

## 11. Глобальний та локальний простори імен

### `globals()` та `locals()`

```python
def my_function():
    local_var = 10
    print(locals())  # {'local_var': 10}

print(globals())  # Словник усіх глобальних змінних
```

## 12. Практичні рекомендації

### ✅ Найкращі практики

1. **Імена змінних**: Використовуйте релевантні назви
   ```python
   # Погано
   def func(x):
       return x + 1
   
   # Добре
   def increment_age(age: int) -> int:
       return age + 1
   ```

2. **Документація**: Завжди додавайте docstrings
   ```python
   def calculate_total(items: list) -> float:
       """
       Обчислює загальну вартість товарів.
       
       Args:
           items: Список товарів
       
       Returns:
           Загальна вартість
       """
       return sum(item.price for item in items)
   ```

3. **Анотації типів**: Використовуйте type hints
   ```python
   from typing import List, Dict
   
   def process_data(data: List[Dict[str, int]]) -> int:
       return len(data)
   ```

### ⚠️ Антипатерни

❌ **Всемогутній об'єкт** (God Object)
- Не запихайте всю логіку в один клас
- Розділяйте відповідальності

❌ **Динамічне видалення атрибутів**
- Краще заздалегідь проектувати структуру
- Використовуйте успадкування замість видалення

## 13. Патерн Singleton з метакласом

```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "Connected"

# Завжди повертається той самий екземпляр
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

## Додаткові матеріали з відкритих джерел

### Коли використовувати метакласи?

Цитата від Tim Peters (розробник Python):
> "Metaclasses are deeper magic than 99% of users should ever worry about. If you wonder whether you need them, you don't."

### Альтернативи метакласам:
- **Декоратори класів** - простіші для більшості випадків
- **`__init_subclass__`** - спрощений хук для модифікації підкласів
- **Дескриптори** - для контролю доступу до атрибутів

### Корисні посилання:
- [PEP 3115](https://peps.python.org/pep-3115/) - Metaclasses in Python 3
- [Python Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Descriptor HowTo Guide](https://docs.python.org/3/howto/descriptor.html)

---

## Домашнє завдання

**Практичне завдання**: Візьміть будь-який свій код (домашнє завдання) та дослідіть його, використовуючи інструменти інтроспекції:

1. `type()`, `isinstance()`, `issubclass()`
2. `hasattr()`, `getattr()`, `setattr()`, `delattr()`
3. `__dict__`, `__class__`, `dir()`
4. Модуль `inspect`
5. Створіть звіт про структуру вашого коду

**Бонус**: Спробуйте створити простий метаклас для валідації атрибутів класу.
---
### Інструменти
```python
type(), isinstance(), issubclass()
dir(), __dict__
hasattr(), getattr(), setattr(), delattr()
```

### Різниця між `__dict__` для класу та екземпляра

```python
class MyClass:
    class_attr = 1  # Атрибут класу
    
    def __init__(self, value):
        self.instance_attr = value  # Атрибут екземпляра

obj = MyClass(10)

# Для екземпляра БЕЗ __init__
obj.__dict__  # {} - порожній словник

# Для екземпляра З __init__
obj.__dict__  # {'instance_attr': 10}

# Для класу
MyClass.__dict__  # Повна структура класу
```

**Важливо**: Щоб `__dict__` екземпляра не був порожнім, потрібен `__init__` або динамічне додавання атрибутів.