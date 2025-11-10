🌿 
Вот полностью структурированный и дополненный конспект лекции **“UNIT_01_UA (26.08.2025) Python Pro (02.09.2025)”** в формате **Markdown**, с пояснениями, примерами кода и расширенным материалом для лучшего понимания.
---

# 🐍 UNIT 01 — Декораторы, Класи, Магічні методи

---

## 🔹 1. Декоратори (Decorators)

### 📘 Визначення

**Декоратор** — це функція, яка приймає іншу функцію (або клас) і повертає нову функцію з розширеною поведінкою, не змінюючи початковий код.

> 🔸 Використовується для:
>
> * логування
> * кешування
> * перевірки прав доступу
> * вимірювання часу виконання
> * модифікації аргументів або результату

---

### 🧩 Приклад: Функціональний декоратор

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Перед викликом функції")
        result = func(*args, **kwargs)
        print("Після виклику функції")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Привіт, {name}!")

greet("Ольга")
```

📤 **Вивід:**

```
Перед викликом функції
Привіт, Ольга!
Після виклику функції
```

---

### 🧱 Декоратори класів

Декоратор може приймати і **класи**, модифікуючи їх методи або атрибути.

```python
def add_repr(cls):
    cls.__repr__ = lambda self: f"{cls.__name__}({self.__dict__})"
    return cls

@add_repr
class User:
    def __init__(self, name):
        self.name = name

user = User("Olga")
print(user)
```

📤 **Вивід:**

```
User({'name': 'Olga'})
```

---

## 🔹 2. Класи та об’єкти

### 📘 Основні поняття

* **Клас** — це шаблон (план, креслення), який описує структуру та поведінку об’єктів.
* **Об’єкт** — це екземпляр класу (реалізація цього шаблону).

```python
class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("Барсик")
dog2 = Dog("Мухтар")
```

---

## 🔹 3. Магічні (dunder) методи

**Dunder methods** — спеціальні методи, імена яких починаються і закінчуються подвійними підкресленнями `__`.

| Метод                  | Призначення                                     |
| ---------------------- | ----------------------------------------------- |
| `__init__`             | Ініціалізація об’єкта                           |
| `__str__`              | Рядкове представлення (для користувача)         |
| `__repr__`             | Технічне представлення (для розробника)         |
| `__add__`              | Перевизначення оператора `+`                    |
| `__sub__`              | Перевизначення оператора `-`                    |
| `__mul__`              | Перевизначення оператора `*`                    |
| `__eq__`               | Порівняння об’єктів на рівність                 |
| `__lt__`               | Менше (`<`)                                     |
| `__iter__`, `__next__` | Ітератори                                       |
| `__del__`              | Деструктор (викликається при видаленні об’єкта) |

---

### ⚙️ Приклад: Перевантаження операторів

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(4, 1)
print(v1 + v2)
```

📤 **Вивід:**

```
Vector(6, 4)
```

---

### 🧮 Приклад: Комплексні числа

```python
class ComplexNumber:
    def __init__(self, real, imag):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        return ComplexNumber(self.real + other.real, self.imag + other.imag)

    def __str__(self):
        return f"{self.real} + {self.imag}i"

num1 = ComplexNumber(3, 2)
num2 = ComplexNumber(1, 7)
print(num1 + num2)
```

📤 **Вивід:**

```
4 + 9i
```

---

## 🔹 4. Порівняння об’єктів

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        return self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

p1 = Person("Olga", 30)
p2 = Person("Anna", 25)
print(p1 == p2)  # False
print(p1 < p2)   # False
```

---

## 🔹 5. Ітератори

Щоб об’єкт можна було перебирати у `for`-циклі, потрібно реалізувати `__iter__` і `__next__`.

```python
class Counter:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit:
            self.current += 1
            return self.current
        else:
            raise StopIteration

for i in Counter(3):
    print(i)
```

📤 **Вивід:**

```
1
2
3
```

---

## 🔹 6. Конструктор і деструктор

| Метод      | Призначення                            |
| ---------- | -------------------------------------- |
| `__new__`  | Виділяє пам’ять під об’єкт             |
| `__init__` | Ініціалізує об’єкт (заповнює атрибути) |
| `__del__`  | Викликається перед знищенням об’єкта   |

```python
class Example:
    def __new__(cls):
        print("Виділяємо пам’ять (__new__)")
        instance = super().__new__(cls)
        return instance

    def __init__(self):
        print("Ініціалізація (__init__)")

    def __del__(self):
        print("Об’єкт знищено (__del__)")

obj = Example()
del obj
```

---

## 🔹 7. Різниця між `__str__` і `__repr__`

```python
class Car:
    def __init__(self, brand):
        self.brand = brand

    def __str__(self):
        return f"Авто: {self.brand}"

    def __repr__(self):
        return f"Car('{self.brand}')"

c = Car("Tesla")
print(str(c))   # Авто: Tesla
print(repr(c))  # Car('Tesla')
```

> 🔸 `__str__` — для користувача (зрозуміло і красиво)
> 🔸 `__repr__` — для розробника (точно і формально)

---

## 🔹 8. Аналогія: Склад і коробки

> `__new__` — будуємо склад (створюємо об’єкт).  
> `__init__` — заповнюємо коробки товарами (атрибути).  
> `__del__` — прибираємо сміття після використання (знищення об’єкта).  

---

## 📚 Додатково для самостійного вивчення

1. 📖 [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
2. 📖 [Python Data Model — офіційна документація](https://docs.python.org/3/reference/datamodel.html)
3. 📘 Книга: *Fluent Python* (Luciano Ramalho) — розділи про dunder methods
4. 💻 Практика: реалізуйте власний клас `Matrix` з перевантаженням `+`, `-`, `*`
5. 🧠 Для тренування:

   * Створіть декоратор `@timer`, який виводить час виконання функції.
   * Реалізуйте клас `Temperature`, який підтримує порівняння і друк у °C і °F.

---
## 🧠 9. Практика

### 🧩 Завдання 1: Декоратор `timer`

Створи декоратор, який виводить час виконання функції.

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Функція {func.__name__} виконалась за {end - start:.4f} сек.")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()
```

---

### 🧩 Завдання 2: Клас `Matrix`

Реалізуй клас, який підтримує додавання матриць:

```python
class Matrix:
    def __init__(self, data):
        self.data = data

    def __add__(self, other):
        result = [
            [a + b for a, b in zip(row_a, row_b)]
            for row_a, row_b in zip(self.data, other.data)
        ]
        return Matrix(result)

    def __repr__(self):
        return f"Matrix({self.data})"
```

---

### 🧩 Завдання 3: Ітератор парних чисел

```python
class EvenNumbers:
    def __init__(self, limit):
        self.limit = limit
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.current += 2
        if self.current <= self.limit:
            return self.current
        raise StopIteration
```

---

## 🧪 10. Тести (unittest)

```python
import unittest
from time import sleep

class TestDecorators(unittest.TestCase):
    def test_timer(self):
        from time import time

        times = []
        def test_func():
            sleep(0.1)
        start = time()
        test_func()
        end = time()
        self.assertGreater(end - start, 0.09)

class TestVector(unittest.TestCase):
    def test_addition(self):
        v1 = Vector(1, 2)
        v2 = Vector(3, 4)
        v3 = v1 + v2
        self.assertEqual((v3.x, v3.y), (4, 6))

if __name__ == "__main__":
    unittest.main()
```

---

## 📚 Рекомендована література

1. [PEP 318 — Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
2. [Python Data Model — офіційна документація](https://docs.python.org/3/reference/datamodel.html)
3. *Fluent Python* (Luciano Ramalho)
4. *Effective Python* (Brett Slatkin), розділи про об’єктно-орієнтоване програмування

