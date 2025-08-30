# Обычная функция
def add(a, b):
    return a + b

# Лямбда-функция (анонимная функция)
# lambda аргументы: выражение
test_function = lambda x, y: x + y

# Вызов лямбда-функции
print(test_function(1, 2))  # Выведет: 3

# Другие примеры лямбда-функций:

# Простая лямбда
square = lambda x: x ** 2
print(square(5))  # Выведет: 25

# Лямбда с условием
max_value = lambda a, b: a if a > b else b
print(max_value(10, 5))  # Выведет: 10

# Использование лямбда с встроенными функциями
numbers = [1, 2, 3, 4, 5]

# map() с лямбда
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # Выведет: [1, 4, 9, 16, 25]

# filter() с лямбда
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # Выведет: [2, 4]

# sorted() с лямбда
students = [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
sorted_by_grade = sorted(students, key=lambda student: student[1])
print(sorted_by_grade)  # Сортировка по оценкам
