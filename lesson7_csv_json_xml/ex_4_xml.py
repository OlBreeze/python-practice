import xml.etree.ElementTree as ET
from xml.dom import minidom


# ================== СОЗДАНИЕ XML ==================

# Вариант 1: Создание XML с ElementTree
def create_xml_elementtree():
    # Создаем корневой элемент
    root = ET.Element("employees")

    # Добавляем сотрудников
    emp1 = ET.SubElement(root, "employee", id="1")
    ET.SubElement(emp1, "name").text = "Pavlo"
    ET.SubElement(emp1, "position").text = "Manager"
    ET.SubElement(emp1, "salary").text = "75000"

    emp2 = ET.SubElement(root, "employee", id="2")
    ET.SubElement(emp2, "name").text = "Maria"
    ET.SubElement(emp2, "position").text = "Data Engineer"
    ET.SubElement(emp2, "salary").text = "80000"

    # Записываем в файл
    tree = ET.ElementTree(root)
    tree.write("employees1.xml", encoding="utf-8", xml_declaration=True)
    print("XML создан с ElementTree")


# Вариант 2: Создание красивого XML с отступами
def create_pretty_xml():
    root = ET.Element("employees")

    employees_data = [
        {"id": "1", "name": "Igor", "position": "Developer", "salary": "70000"},
        {"id": "2", "name": "Anna", "position": "Designer", "salary": "65000"},
        {"id": "3", "name": "Dmitro", "position": "Tester", "salary": "60000"}
    ]

    for emp_data in employees_data:
        emp = ET.SubElement(root, "employee", id=emp_data["id"])
        for key, value in emp_data.items():
            if key != "id":
                ET.SubElement(emp, key).text = value

    # Делаем красивое форматирование
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open("employees2.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)
    print("Красивый XML создан")


# Вариант 3: Создание XML строкой
def create_xml_string():
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<company>
    <name>TechCorp</name>
    <location>Kyiv</location>
    <employees>
        <employee id="1">
            <name>Oleksandr</name>
            <position>Team Lead</position>
            <department>Development</department>
        </employee>
        <employee id="2">
            <name>Viktoria</name>
            <position>QA Engineer</position>
            <department>Quality Assurance</department>
        </employee>
    </employees>
</company>'''

    with open("company.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)
    print("XML создан строкой")


# ================== ЧТЕНИЕ XML ==================

# Вариант 4: Чтение XML из файла
def read_xml_from_file():
    try:
        tree = ET.parse("employees1.xml")
        root = tree.getroot()

        print(f"Корневой элемент: {root.tag}")

        for employee in root.findall("employee"):
            emp_id = employee.get("id")
            name = employee.find("name").text
            position = employee.find("position").text
            salary = employee.find("salary").text

            print(f"ID: {emp_id}, Имя: {name}, Позиция: {position}, Зарплата: {salary}")

    except FileNotFoundError:
        print("Файл не найден")
    except ET.ParseError as e:
        print(f"Ошибка парсинга: {e}")


# Вариант 5: Чтение XML из строки
def read_xml_from_string():
    xml_string = '''<?xml version="1.0"?>
    <books>
        <book id="1">
            <title>Python Programming</title>
            <author>John Doe</author>
            <price>29.99</price>
        </book>
        <book id="2">
            <title>Data Science</title>
            <author>Jane Smith</author>
            <price>39.99</price>
        </book>
    </books>'''

    root = ET.fromstring(xml_string)

    for book in root.findall("book"):
        book_id = book.get("id")
        title = book.find("title").text
        author = book.find("author").text
        price = book.find("price").text

        print(f"Книга {book_id}: '{title}' - {author} ({price}$)")


# ================== ПОИСК И ФИЛЬТРАЦИЯ ==================

# Вариант 6: Поиск элементов с условиями
def search_xml_elements():
    try:
        tree = ET.parse("company.xml")
        root = tree.getroot()

        # Поиск по тегу
        company_name = root.find("name").text
        print(f"Компания: {company_name}")

        # Поиск всех сотрудников
        employees = root.findall(".//employee")
        print(f"Всего сотрудников: {len(employees)}")

        # Поиск по атрибуту
        employee_1 = root.find(".//employee[@id='1']")
        if employee_1 is not None:
            name = employee_1.find("name").text
            print(f"Сотрудник с ID 1: {name}")

        # Поиск по тексту элемента
        for emp in employees:
            if emp.find("department").text == "Development":
                name = emp.find("name").text
                print(f"Разработчик: {name}")

    except Exception as e:
        print(f"Ошибка: {e}")


# ================== МОДИФИКАЦИЯ XML ==================

# Вариант 7: Изменение существующего XML
def modify_xml():
    try:
        tree = ET.parse("employees1.xml")
        root = tree.getroot()

        # Добавляем новый элемент
        new_employee = ET.SubElement(root, "employee", id="3")
        ET.SubElement(new_employee, "name").text = "Sergiy"
        ET.SubElement(new_employee, "position").text = "DevOps"
        ET.SubElement(new_employee, "salary").text = "85000"

        # Изменяем существующий элемент
        for emp in root.findall("employee"):
            if emp.get("id") == "1":
                salary_elem = emp.find("salary")
                salary_elem.text = "78000"  # Повышаем зарплату

        # Сохраняем изменения
        tree.write("employees_modified.xml", encoding="utf-8", xml_declaration=True)
        print("XML модифицирован")

    except Exception as e:
        print(f"Ошибка модификации: {e}")


# Вариант 8: Удаление элементов
def remove_xml_elements():
    try:
        tree = ET.parse("employees1.xml")
        root = tree.getroot()

        # Удаляем сотрудника с ID 2
        for emp in root.findall("employee"):
            if emp.get("id") == "2":
                root.remove(emp)
                print("Сотрудник с ID 2 удален")
                break

        tree.write("employees_after_removalxml", encoding="utf-8", xml_declaration=True)

    except Exception as e:
        print(f"Ошибка удаления: {e}")


# ================== КОНВЕРТАЦИЯ ==================

# Вариант 9: XML в словарь
def xml_to_dict():
    xml_string = '''<person>
        <name>John</name>
        <age>30</age>
        <city>New York</city>
    </person>'''

    root = ET.fromstring(xml_string)

    result = {}
    for child in root:
        result[child.tag] = child.text

    print("XML в словарь:", result)
    return result


# Вариант 10: Словарь в XML
def dict_to_xml(data, root_name="root"):
    root = ET.Element(root_name)

    for key, value in data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)

    tree = ET.ElementTree(root)
    tree.write(f"{root_name}.xml", encoding="utf-8", xml_declaration=True)
    print(f"Словарь конвертирован в {root_name}.xml")


# ================== ВАЛИДАЦИЯ ==================

# Вариант 11: Проверка структуры XML
def validate_xml_structure():
    try:
        tree = ET.parse("employees1.xml")
        root = tree.getroot()

        required_fields = ["name", "position", "salary"]

        for i, employee in enumerate(root.findall("employee")):
            print(f"Проверка сотрудника {i + 1}:")

            for field in required_fields:
                element = employee.find(field)
                if element is None:
                    print(f"  ❌ Отсутствует поле: {field}")
                else:
                    print(f"  ✅ Поле {field}: {element.text}")

    except Exception as e:
        print(f"Ошибка валидации: {e}")


# ================== ЗАПУСК ПРИМЕРОВ ==================

if __name__ == "__main__":
    print("=== СОЗДАНИЕ XML ===")
    create_xml_elementtree()
    create_pretty_xml()
    create_xml_string()

    print("\n=== ЧТЕНИЕ XML ===")
    read_xml_from_file()
    print()
    read_xml_from_string()

    print("\n=== ПОИСК В XML ===")
    search_xml_elements()

    print("\n=== МОДИФИКАЦИЯ XML ===")
    modify_xml()
    remove_xml_elements()

    print("\n=== КОНВЕРТАЦИЯ ===")
    person_dict = xml_to_dict()
    dict_to_xml({"name": "Alice", "age": 25, "job": "Engineer"}, "employee")

    print("\n=== ВАЛИДАЦИЯ ===")
    validate_xml_structure()