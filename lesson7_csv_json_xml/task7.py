import csv
import json
import xml.etree.ElementTree as ET

people_data = [
    {"first_name": "Іван", "last_name": "Петренко", "age": 25},
    {"first_name": "Олексій", "last_name": "Шевченко", "age": 28},
    {"first_name": "Дмитро", "last_name": "Іваненко", "age": 35}
]

def write_to_csv():
    print("-- ЗАПИСЬ В CSV --")

    with open("people.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["first_name", "last_name", "age"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Записываем заголовки
        writer.writerows(people_data)  # Записываем все строки


def write_to_json():
    print("\n--- ЗАПИСЬ В JSON ---")

    with open("people.json", "w", encoding="utf-8") as jsonfile:
        json.dump(people_data, jsonfile, ensure_ascii=False, indent=4)


def write_to_xml():
    print("\n--- ЗАПИСЬ В XML ---")

    root = ET.Element("people")

    for person_data in people_data:
        person = ET.SubElement(root, "person")

        first_name = ET.SubElement(person, "first_name")
        first_name.text = person_data["first_name"]

        last_name = ET.SubElement(person, "last_name")
        last_name.text = person_data["last_name"]

        age = ET.SubElement(person, "age")
        age.text = str(person_data["age"])

    tree = ET.ElementTree(root)
    tree.write("people.xml", encoding="utf-8", xml_declaration=True)


#-------------
write_to_csv()
write_to_json()
write_to_xml()