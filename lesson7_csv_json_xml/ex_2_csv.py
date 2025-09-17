import csv

# Первый способ - обычный csv.reader
with open("employees.csv", encoding="UTF-8", newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        employee_id, name, department, salary = row
        print(f'{employee_id}, {name}, {department}, {salary}')

# Второй способ - csv.DictReader
with open("employees.csv", encoding="UTF-8", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    print("Data of employees:")
    for row in reader:
        print(row)