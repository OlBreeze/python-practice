# Конспект лекції: Файли, Ітератори та Генератори в Python

## 1. Повторення: Інтроспекція та Рефлексія

### Основні поняття
- **Інтроспекція** - дослідження коду без його зміни
- **Рефлексія** - можливість динамічно змінювати структуру коду

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

## 2. Робота з файлами

### Що таке файл?
> **Файл** - це сукупність даних, об'єднаних ім'ям і розширенням, які зберігаються фізично на носії інформації.

### Типи файлів
- **Текстові** - зберігають символи, літери
- **Бінарні** - медіафайли (зображення, аудіо, відео)

### Різниця між файлом та файловим об'єктом

| Файл | Файловий об'єкт |
|------|-----------------|
| Фізичне сховище на диску | Об'єкт в оперативній пам'яті |
| Постійне зберігання | Тимчасовий для роботи програми |

### Функція `open()`

```python
# Базовий синтаксис
open(filename, mode='r', encoding='utf-8')
```

#### Режими роботи з файлами

| Режим | Опис |
|-------|------|
| `'r'` | Читання (за замовчуванням). Помилка, якщо файл не існує |
| `'w'` | Запис. Створює файл, якщо не існує. **ПЕРЕЗАПИСУЄ** вміст |
| `'a'` | Дозапис. Створює файл, якщо не існує. Додає в кінець |
| `'r+'` | Читання та запис |
| `'b'` | Бінарний режим (додається до інших: `'rb'`, `'wb'`) |

### Приклади роботи з файлами

#### Запис у файл

```python
# БЕЗ контекстного менеджера (погано)
file = open('test.txt', 'w', encoding='utf-8')
file.write('Test message')
file.close()  # Можна забути!

# З контекстним менеджером (добре)
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write('Test message')
# Автоматичне закриття файлу
```

#### Читання з файлу

```python
# Метод 1: read() - весь файл
with open('test.txt', 'r', encoding='utf-8') as file:
    data = file.read()  # Вся інформація як один рядок

# Метод 2: readline() - один рядок
with open('test.txt', 'r', encoding='utf-8') as file:
    line = file.readline()  # Перший рядок

# Метод 3: readlines() - список рядків
with open('test.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()  # ['рядок1\n', 'рядок2\n', ...]

# Метод 4: ітерація (найкраще для великих файлів)
with open('test.txt', 'r', encoding='utf-8') as file:
    for line in file:
        print(line.strip())  # strip() видаляє \n
```

#### Обмеження читання

```python
with open('test.txt', 'r', encoding='utf-8') as file:
    data = file.read(10)  # Перші 10 символів
```

### Контекстний менеджер `with`

**Переваги:**
✅ Автоматичне закриття файлу
✅ Коректна робота навіть при помилках
✅ Звільнення ресурсів гарантовано

```python
# Людський фактор - можна забути закрити
file = open('data.txt')
data = file.read()
file.close()  # Що якщо забули?

# Контекстний менеджер - закриття автоматичне
with open('data.txt') as file:
    data = file.read()
# Файл закрито автоматично
```

## 3. Ітеровані об'єкти та Ітератори

### Основні поняття

**Ітерований об'єкт (Iterable)** - об'єкт, який можна перебирати (list, tuple, str, dict, set, file)

**Ітератор (Iterator)** - об'єкт з протоколом ітерації, який надає доступ до елементів послідовності

### Протокол ітерації

```python
my_list = [1, 2, 3, 4, 5]

# Створення ітератора
iterator = iter(my_list)  # або my_list.__iter__()

print(iterator)  # <list_iterator object at 0x...>

# Отримання наступного елемента
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3
# ...
# next(iterator)  # StopIteration - коли елементи закінчаться
```

### Виняток `StopIteration`

```python
iterator = iter([1, 2, 3])

while True:
    try:
        value = next(iterator)
        print(value)
    except StopIteration:
        print("Ітерація завершена")
        break
```

**Важливо**: Цикл `for` під капотом робить саме це!

### Цикл `for` під капотом

```python
# Що ви пишете
for item in my_list:
    print(item)

# Що насправді відбувається
iterator = iter(my_list)
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
```

## 4. Створення власних ітераторів

### Варіант 1: Клас-ітератор

```python
class DataIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0
    
    def __iter__(self):
        # Повертає сам об'єкт
        return self
    
    def __next__(self):
        # Перевірка виходу за межі
        if self.index >= len(self.data):
            raise StopIteration("Дані закінчилися")
        
        # Отримання поточного значення
        value = self.data[self.index]
        # Інкремент індексу
        self.index += 1
        # Повернення значення
        return value

# Використання
numbers = DataIterator([1, 2, 3, 4, 5])
for num in numbers:
    print(num)
```

### Магічні методи ітератора

- **`__iter__()`** - повертає об'єкт ітератора (зазвичай `self`)
- **`__next__()`** - повертає наступний елемент або викидає `StopIteration`

### Приклад: Range-подібний клас

```python
class MyRange:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.step > 0 and self.current < self.stop:
            result = self.current
            self.current += self.step
            return result
        elif self.step < 0 and self.current > self.stop:
            result = self.current
            self.current += self.step
            return result
        else:
            raise StopIteration

# Використання
for i in MyRange(0, 5):
    print(i)  # 0, 1, 2, 3, 4

for i in MyRange(10, 5, -1):
    print(i)  # 10, 9, 8, 7, 6
```

## 5. Генератори

### Що таке генератор?

> **Генератор** - це спеціальний тип ітератора, який створюється за допомогою функції з ключовим словом `yield`.

### Переваги генераторів
✅ Простіша реалізація (не потрібен клас)
✅ Автоматична реалізація `__iter__()` та `__next__()`
✅ Економія пам'яті (ліниві обчислення)

### Ліниві обчислення (Lazy Evaluation)

**Концепція**: Значення обчислюються тільки тоді, коли вони потрібні, а не всі одразу.

```python
# Звичайна функція - всі значення одразу
def get_numbers(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result  # Повертає весь список

# Генератор - по одному значенню
def get_numbers_gen(n):
    for i in range(n):
        yield i ** 2  # Повертає одне значення, зупиняється

# Використання
nums = get_numbers_gen(5)
print(next(nums))  # 0
print(next(nums))  # 1
print(next(nums))  # 4
```

### Різниця між `return` та `yield`

| `return` | `yield` |
|----------|---------|
| Завершує функцію | Призупиняє функцію |
| Повертає кінцевий результат | Повертає проміжний результат |
| Можна викликати 1 раз | Можна викликати багато разів |
| Очищає локальну пам'ять | Зберігає стан |

### Приклад генератора для файлів

```python
def read_file_generator(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# Використання
for line in read_file_generator('data.txt'):
    print(line)
```

### Генератор з `yield from`

```python
def show_letters(text):
    for char in text:
        if char.isalpha():
            yield char

def show_letters_v2(text):
    # Компактніша версія
    yield from (char for char in text if char.isalpha())

# Використання
text = "Hello, World! 123"
print(list(show_letters(text)))  # ['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']
```

## 6. Вирази генераторів та List Comprehension

### List Comprehension (спискове включення)

```python
# Створення списку
squares = [x ** 2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
print(type(squares))  # <class 'list'>
```

### Вираз генератора (Generator Expression)

```python
# Створення генератора
squares_gen = (x ** 2 for x in range(10))
print(squares_gen)  # <generator object at 0x...>
print(type(squares_gen))  # <class 'generator'>

# Для використання потрібно ітерувати
print(list(squares_gen))  # [0, 1, 4, 9, 16, ...]
```

### Порівняння синтаксису

```python
# List Comprehension - квадратні дужки []
list_comp = [x ** 2 for x in range(10)]

# Generator Expression - круглі дужки ()
gen_expr = (x ** 2 for x in range(10))
```

### Порівняння продуктивності

```python
import sys

# Пам'ять
list_comp = [x for x in range(10000)]
gen_expr = (x for x in range(10000))

print(sys.getsizeof(list_comp))  # ~85 KB
print(sys.getsizeof(gen_expr))   # ~208 bytes (!)
```

**Висновки:**
- **List Comprehension**: швидше на 15-20%, але споживає багато пам'яті
- **Generator Expression**: повільніше, але економить пам'ять (завжди ~200 байт)

### Коли що використовувати?

| Ситуація | Рішення |
|----------|---------|
| Потрібен весь список для обробки | List Comprehension |
| Великий обсяг даних | Generator Expression |
| Файли, мережеві запити, БД | Generator Expression |
| Багаторазове використання | List Comprehension |
| Одноразове перебирання | Generator Expression |

## 7. Функції вищого порядку

### `map()`

```python
# З list comprehension
squares = [x ** 2 for x in range(10)]

# З generator expression
squares_gen = (x ** 2 for x in range(10))

# З map() - функція вищого порядку
squares_map = map(lambda x: x ** 2, range(10))

# Для використання
print(list(squares_map))
```

**Примітка**: `map()` повертає ітератор, схожий на генератор.

## 8. Контекстні менеджери (Context Managers)

### Навіщо потрібні?

**Проблема**: Забути закрити файл/з'єднання/ресурс
**Рішення**: Контекстний менеджер автоматично закриває ресурси

### Варіант 1: Клас з магічними методами

```python
class CustomContextManager:
    def __init__(self, data):
        self.data = data
        print("Ініціалізація")
    
    def __enter__(self):
        print("Вхід в контекстний менеджер")
        return self  # Повертає об'єкт для роботи
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Вихід з контекстного менеджера")
        if exc_type:
            print(f"Виникла помилка: {exc_val}")
        return False  # False - пропустити помилку далі

# Використання
with CustomContextManager("test") as manager:
    print("Робота з менеджером")
    # manager.data доступний тут
```

### Магічні методи контекстного менеджера

- **`__enter__()`** - викликається при вході в блок `with`
- **`__exit__(exc_type, exc_val, exc_tb)`** - викликається при виході (навіть при помилці)

### Варіант 2: Функція-генератор з декоратором

```python
from contextlib import contextmanager

@contextmanager
def custom_manager(data):
    print("Enter")
    try:
        yield data  # Повертає об'єкт для роботи
    finally:
        print("Exit")

# Використання
with custom_manager("test") as data:
    print(f"Робота з {data}")
```

### Порівняння підходів

| Клас | Функція-генератор |
|------|-------------------|
| Більш гнучкий | Простіший |
| Повний контроль | Швидше написати |
| Для складної логіки | Для простих випадків |

### Приклад: Менеджер для файлів

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode, encoding='utf-8')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        return False

# Використання
with FileManager('test.txt', 'w') as file:
    file.write('Hello, World!')
```

## 9. Патерн проектування: Ітератор

### Що таке патерн Ітератор?

> **Ітератор** - поведінковий патерн проектування, який надає послідовний доступ до елементів колекції без розкриття її внутрішньої структури.

### Переваги патерну
✅ Приховування деталей реалізації (інкапсуляція)
✅ Уніфікований інтерфейс для різних колекцій
✅ Можливість перебирати без знання структури

## 10. Практичні рекомендації

### Робота з файлами

```python
# ✅ Добре
with open('file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        process(line.strip())

# ❌ Погано
f = open('file.txt')
data = f.read()  # Весь файл в пам'ять!
f.close()  # Можна забути
```

### Вибір між ітератором та генератором

```python
# Клас-ітератор - коли потрібен стан
class BookReader:
    def __init__(self, filename):
        self.filename = filename
        self.current_page = 0
    
    def next_page(self):
        ...
    
    def previous_page(self):  # Генератор цього не може!
        ...

# Генератор - для простих випадків
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

### Економія пам'яті

```python
# ❌ Багато пам'яті
numbers = [x ** 2 for x in range(1000000)]
process(numbers)

# ✅ Мало пам'яті
numbers = (x ** 2 for x in range(1000000))
for num in numbers:
    process(num)
```

## Додаткові матеріали

### Метод `seek()` для файлів

```python
with open('file.txt', 'r') as f:
    data = f.read(10)  # Перші 10 символів
    f.seek(0)  # Повернутися на початок
    data = f.read(10)  # Знову перші 10 символів
```

### Різниця між `for` та `while`

| `for` | `while`              |
|-------|----------------------|
| Для відомої кількості ітерацій | Для умовних ітерацій |
| Протокол ітерації | Умова True/False     |
| Компактніший | Гнучкіший            |

### PEP 8: Порожні рядки

```python
# ✅ Правильно
def function1():
    pass


def function2():  # Два порожні рядки між функціями
    pass


class MyClass:  # Два порожні рядки перед класом
    def method(self):
        pass
```

## Домашнє завдання

1. **Базове**: Створити функцію-генератор для читання великого файлу по рядках
2. **Середнє**: Створити клас-ітератор для перебирання діапазону чисел з кроком
3. **Складне**: Створити власний контекстний менеджер для роботи з файлами з логуванням

### Додаткові ресурси
- Відео "Ітератор-генератор від А до Я" на IT Education Hub
- Документація Python: [Iterators](https://docs.python.org/3/tutorial/classes.html#iterators)
- [PEP 255](https://peps.python.org/pep-0255/) - Simple Generators

---

**Ключові висновки:**
- Файли потрібно закривати (використовуйте `with`)
- Генератори економлять пам'ять
- Ітератори приховують деталі реалізації
- Вибір між list comprehension та generator expression залежить від задачі