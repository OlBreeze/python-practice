# Исходные данные
students = [('Alice', 85), ('Bob', 90), ('Charlie', 78)]
print("Исходный список:")
print(students)
print()

# Что происходит внутри sorted()
print("Пошаговое объяснение:")
print("1. sorted() берет каждый элемент списка")
print("2. Применяет к нему key-функцию (lambda)")
print("3. Сортирует по полученным значениям")
print()

# Давайте посмотрим что возвращает lambda для каждого элемента:
print("Что возвращает lambda для каждого студента:")
for student in students:
    key_value = (lambda student: student[1])(student)
    print(f"Для {student} -> key = {key_value}")
print()

# Результат сортировки
sorted_by_grade = sorted(students, key=lambda student: student[1])
print("Результат сортировки по оценкам (по возрастанию):")
print(sorted_by_grade)
print()

# Альтернативные способы записи той же логики:

# 1. Обычная функция вместо lambda
def get_grade(student):
    return student[1]

sorted_alternative1 = sorted(students, key=get_grade)
print("То же самое с обычной функцией:")
print(sorted_alternative1)
print()

# 2. Сортировка по убыванию
sorted_desc = sorted(students, key=lambda student: student[1], reverse=True)
print("Сортировка по убыванию оценок:")
print(sorted_desc)
print()

# 3. Сортировка по имени (первый элемент кортежа)
sorted_by_name = sorted(students, key=lambda student: student[0])
print("Сортировка по имени:")
print(sorted_by_name)
print()

# 4. Более сложная сортировка - сначала по оценке, потом по имени
students_extended = [('Alice', 85), ('Bob', 90), ('Charlie', 78), ('David', 85)]
sorted_complex = sorted(students_extended, key=lambda student: (student[1], student[0]))
print("Сортировка сначала по оценке, потом по имени:")
print(sorted_complex)
print()

# 5. Использование operator.itemgetter (более эффективно)
from operator import itemgetter
sorted_itemgetter = sorted(students, key=itemgetter(1))
print("То же самое с itemgetter:")
print(sorted_itemgetter)
print()

# Демонстрация того, как работает key внутри
print("Как работает параметр key:")
print("sorted() создает пары (ключ, элемент) для сортировки:")
print("[(ключ, элемент), ...]")
for student in students:
    key = (lambda student: student[1])(student)  # Правильно: 1 аргумент
    print(f"({key}, {student})")

# Показываем как sorted() использует эти ключи
print("\nПорядок сортировки по ключам:")
keys_and_elements = [(student[1], student) for student in students]
print("До сортировки:", keys_and_elements)
keys_and_elements.sort(key=lambda x: x[0])  # Сортируем по первому элементу (ключу)
print("После сортировки:", keys_and_elements)
print("Финальный результат:", [element for key, element in keys_and_elements])