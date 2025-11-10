# ЗАМЫКАНИЯ (CLOSURES) в Python

def curr_add(a):  # Внешняя функция принимает параметр 'a'
    def in_b(b):  # Внутренняя функция принимает параметр 'b'
        return a + b  # Использует 'a' из внешней функции!
    return in_b  # Возвращает внутреннюю функцию

# Создаем функцию с "запомненным" значением a = 1
my_add = curr_add(1)
print(my_add(1))    # Выведет: 2 (1 + 1)
print(my_add(123))  # Выведет: 124 (1 + 123)

print("\n=== Подробное объяснение ===")

# Шаг за шагом:
print("1. Вызываем curr_add(1):")
my_add = curr_add(1)
print(f"   my_add теперь = {my_add}")
print(f"   my_add это функция: {type(my_add)}")

print("\n2. my_add 'помнит' что a = 1")
print("3. Когда мы вызываем my_add(123), она делает: a + b = 1 + 123")

# Создаем разные замыкания
print("\n=== Создание разных замыканий ===")
add_5 = curr_add(5)   # a = 5
add_10 = curr_add(10) # a = 10
add_100 = curr_add(100) # a = 100

print(f"add_5(3) = {add_5(3)}")     # 5 + 3 = 8
print(f"add_10(3) = {add_10(3)}")   # 10 + 3 = 13
print(f"add_100(3) = {add_100(3)}") # 100 + 3 = 103

# Каждая функция "помнит" свое значение a!

print("\n=== Другие примеры замыканий ===")

# Пример 1: Множитель
def make_multiplier(x):
    def multiply(y):
        return x * y
    return multiply

multiply_by_3 = make_multiplier(3)
print(f"multiply_by_3(4) = {multiply_by_3(4)}")  # 3 * 4 = 12

# Пример 2: Счетчик
def make_counter():
    count = 0
    def counter():
        nonlocal count  # Изменяем переменную из внешней области
        count += 1
        return count
    return counter

counter1 = make_counter()
counter2 = make_counter()

print(f"counter1(): {counter1()}")  # 1
print(f"counter1(): {counter1()}")  # 2
print(f"counter2(): {counter2()}")  # 1 (независимый счетчик)

# Пример 3: Конфигурация функции
def make_greeting(greeting):
    def greet(name):
        return f"{greeting}, {name}!"
    return greet

say_hello = make_greeting("Hello")
say_hi = make_greeting("Hi")

print(f"say_hello('Alice') = {say_hello('Alice')}")  # Hello, Alice!
print(f"say_hi('Bob') = {say_hi('Bob')}")            # Hi, Bob!

print("\n=== Как это работает внутри ===")
print("1. Внешняя функция создает локальную переменную")
print("2. Внутренняя функция 'захватывает' эту переменную")
print("3. Даже после завершения внешней функции,")
print("   внутренняя функция помнит захваченные переменные")
print("4. Это называется 'замыканием' (closure)")

# Проверим что переменная действительно захвачена
print(f"\nmy_add.__closure__ = {my_add.__closure__}")
if my_add.__closure__:
    print(f"Захваченное значение: {my_add.__closure__[0].cell_contents}")