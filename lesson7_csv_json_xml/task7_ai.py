import csv
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Исходные данные
people_data = [
    {"first_name": "Іван", "last_name": "Петренко", "age": 25},
    {"first_name": "Марія", "last_name": "Коваленко", "age": 30},
    {"first_name": "Олексій", "last_name": "Шевченко", "age": 28},
    {"first_name": "Анна", "last_name": "Мельник", "age": 22},
    {"first_name": "Дмитро", "last_name": "Іваненко", "age": 35}
]


# ==================== ЗАПИСЬ В CSV ====================

def write_to_csv():
    print("=== ЗАПИСЬ В CSV ===")

    # Вариант 1: С использованием DictWriter
    with open("people.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["first_name", "last_name", "age"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Записываем заголовки
        writer.writerows(people_data)  # Записываем все строки

    print("✅ Данные записаны в people.csv")

    # Вариант 2: С использованием обычного writer
    with open("people_simple.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовок
        writer.writerow(["Имя", "Фамилия", "Возраст"])

        # Записываем данные
        for person in people_data:
            writer.writerow([person["first_name"], person["last_name"], person["age"]])

    print("✅ Данные записаны в people_simple.csv")


# ==================== ЗАПИСЬ В JSON ====================

def write_to_json():
    print("\n=== ЗАПИСЬ В JSON ===")

    # Вариант 1: Простая запись
    with open("people.json", "w", encoding="utf-8") as jsonfile:
        json.dump(people_data, jsonfile, ensure_ascii=False, indent=4)

    print("✅ Данные записаны в people.json")

    # Вариант 2: Структурированная запись
    structured_data = {
        "people": people_data,
        "total_count": len(people_data),
        "created_at": "2024-01-01"
    }

    with open("people_structured.json", "w", encoding="utf-8") as jsonfile:
        json.dump(structured_data, jsonfile, ensure_ascii=False, indent=2)

    print("✅ Структурированные данные записаны в people_structured.json")


# ==================== ЗАПИСЬ В XML ====================

def write_to_xml():
    print("\n=== ЗАПИСЬ В XML ===")

    # Вариант 1: Простая структура
    root = ET.Element("people")

    for person_data in people_data:
        person = ET.SubElement(root, "person")

        first_name = ET.SubElement(person, "first_name")
        first_name.text = person_data["first_name"]

        last_name = ET.SubElement(person, "last_name")
        last_name.text = person_data["last_name"]

        age = ET.SubElement(person, "age")
        age.text = str(person_data["age"])

    # Записываем без форматирования
    tree = ET.ElementTree(root)
    tree.write("people.xml", encoding="utf-8", xml_declaration=True)
    print("✅ Данные записаны в people.xml")

    # Вариант 2: С красивым форматированием
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open("people_pretty.xml", "w", encoding="utf-8") as xmlfile:
        xmlfile.write(pretty_xml)

    print("✅ Красиво отформатированные данные записаны в people_pretty.xml")

    # Вариант 3: С атрибутами
    root_with_attrs = ET.Element("people")

    for i, person_data in enumerate(people_data, 1):
        person = ET.SubElement(root_with_attrs, "person", id=str(i))
        person.set("full_name", f"{person_data['first_name']} {person_data['last_name']}")

        ET.SubElement(person, "first_name").text = person_data["first_name"]
        ET.SubElement(person, "last_name").text = person_data["last_name"]
        ET.SubElement(person, "age").text = str(person_data["age"])

    # Форматируем и сохраняем
    rough_string = ET.tostring(root_with_attrs, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")

    with open("people_with_attributes.xml", "w", encoding="utf-8") as xmlfile:
        xmlfile.write(pretty_xml)

    print("✅ XML с атрибутами записан в people_with_attributes.xml")


# ==================== ЧТЕНИЕ ДАННЫХ ====================

def read_csv():
    print("\n=== ЧТЕНИЕ CSV ===")
    try:
        with open("people.csv", "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Имя: {row['first_name']}, Фамилия: {row['last_name']}, Возраст: {row['age']}")
    except FileNotFoundError:
        print("Файл people.csv не найден")


def read_json():
    print("\n=== ЧТЕНИЕ JSON ===")
    try:
        with open("people.json", "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            for person in data:
                print(f"Имя: {person['first_name']}, Фамилия: {person['last_name']}, Возраст: {person['age']}")
    except FileNotFoundError:
        print("Файл people.json не найден")


def read_xml():
    print("\n=== ЧТЕНИЕ XML ===")
    try:
        tree = ET.parse("people.xml")
        root = tree.getroot()

        for person in root.findall("person"):
            first_name = person.find("first_name").text
            last_name = person.find("last_name").text
            age = person.find("age").text
            print(f"Имя: {first_name}, Фамилия: {last_name}, Возраст: {age}")
    except FileNotFoundError:
        print("Файл people.xml не найден")


# ==================== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ====================

def add_person_to_files(first_name, last_name, age):
    """Добавляет нового человека во все форматы"""
    print(f"\n=== ДОБАВЛЕНИЕ: {first_name} {last_name}, {age} лет ===")

    new_person = {"first_name": first_name, "last_name": last_name, "age": age}

    # Добавляем в CSV
    with open("people.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["first_name", "last_name", "age"])
        writer.writerow(new_person)

    # Добавляем в JSON
    try:
        with open("people.json", "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError:
        data = []

    data.append(new_person)

    with open("people.json", "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)

    print("✅ Новый человек добавлен в CSV и JSON")


def get_statistics():
    """Показывает статистику по возрасту"""
    print("\n=== СТАТИСТИКА ===")

    ages = [person["age"] for person in people_data]

    print(f"Общее количество людей: {len(people_data)}")
    print(f"Средний возраст: {sum(ages) / len(ages):.1f}")
    print(f"Минимальный возраст: {min(ages)}")
    print(f"Максимальный возраст: {max(ages)}")


# ==================== ЗАПУСК ПРОГРАММЫ ====================

if __name__ == "__main__":
    # Записываем данные в разные форматы
    write_to_csv()
    write_to_json()
    write_to_xml()

    # Читаем данные из файлов
    read_csv()
    read_json()
    read_xml()

    # Дополнительные операции
    add_person_to_files("Петро", "Сидоренко", 27)
    get_statistics()

    print("\n🎉 Все операции выполнены успешно!")