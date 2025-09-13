numbers = []

for i in range(10):
    value = input(f"Enter number #{i + 1}: ")
    numbers.append(value)

test_file = "example8.txt"

with open(test_file, "w", encoding="utf-8") as f:
    for number in numbers:
        f.write(number + "\n")

print(f"Дані записано у файл {test_file}")