import csv

print("Дані успішно записані до new_employees.csv!")

employees_data = [
    {'id': '1', 'name': 'Pavlo', 'position': 'Manager'},
    {'id': '2', 'name': 'Maria', 'position': 'Data Engineer'},
    {'id': '3', 'name': 'Igor', 'position': 'Developer'},
]

fieldnames = ['id', 'name', 'position']

# Вариант 1: DictWriter (как в исходном коде)
with open('new_employees1.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employees_data)

# Вариант 2: DictWriter с записью по одной строке
with open('new_employees2.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for employee in employees_data:
        writer.writerow(employee)

# Вариант 3: Обычный csv.writer
with open('new_employees3.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    # Записываем заголовки
    writer.writerow(fieldnames)
    # Записываем данные
    for employee in employees_data:
        writer.writerow([employee['id'], employee['name'], employee['position']])

# Вариант 4: csv.writer со всеми строками сразу
with open('new_employees4.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.writer(csvfile)
    # Записываем заголовки
    writer.writerow(fieldnames)
    # Подготавливаем данные в виде списка списков
    rows = [[emp['id'], emp['name'], emp['position']] for emp in employees_data]
    writer.writerows(rows)

# Вариант 5: Запись с разделителем (например, точка с запятой)
with open('new_employees5.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(employees_data)

# Вариант 6: Добавление данных к существующему файлу (режим 'a')
with open('new_employees6.csv', 'a', newline='', encoding='UTF-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Записываем только данные (без заголовка, если файл уже существует)
    writer.writerows(employees_data)

# Вариант 7: Запись с дополнительными параметрами
with open('new_employees7.csv', 'w', newline='', encoding='UTF-8') as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=fieldnames,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    writer.writeheader()
    writer.writerows(employees_data)

print("Все варианты записи выполнены успешно!")