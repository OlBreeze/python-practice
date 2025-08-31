# Завдання 6: Калькулятор з використанням замикань
# arr_symbols = ['+', '-', '*', '/', '%']

def create_operator(operator):
    def operation(a, b):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                return "Помилка: Ділення на нуль!"
            return a / b
        else:
            return "Невідомий оператор"

    return operation


# print(create_operator('+')(10, 5)) # можна й так

add = create_operator('+')
subtract = create_operator('-')
multiply = create_operator('*')
divide = create_operator('/')

# Check
print(f"Додавання: 10 + 5 = {add(10, 5)}")
print(f"Додавання: 15 + 5 = {add(15, 5)}")
print(f"Додавання: 55 + 5 = {add(55, 5)}")

print(f"\nВіднімання: 10 - 5 = {subtract(10, 5)}")
print(f"Множення: 10 * 5 = {multiply(10, 5)}")
print(f"Ділення: 10 / 5 = {divide(10, 5)}")
print(f"Ділення на нуль: 10 / 0 = {divide(10, 0)}")
