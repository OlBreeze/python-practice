# Завдання 5: Робота з XML
# Створи XML-файл, що містить інформацію про продукти магазину: Назва продукту, Ціна, Кількість на складі
# 2.Напиши програму, яка:
# Читає XML-файл і виводить назви продуктів та їхню кількість.
# Змінює кількість товару та зберігає зміни в XML-файл.

# ET.indent — это утилита из модуля xml.etree.ElementTree (введена в Python 3.9),
# которая добавляет отступы в древовидную структуру XML для красивого (pretty) вывода.
# Она изменяет дерево на месте, добавляя пробелы/переводы строки в text/tail узлов,
# чтобы при сериализации получился читаемый многострочный XML.

import xml.etree.ElementTree as ET
from typing import List, Dict
import os


def create_xml_file(filename: str = "products.xml") -> None:
    """
    Створює XML файл з початковими продуктами, якщо його немає.

    Args:
        filename (str): Ім'я файлу. За замовчуванням "products.xml"
    """
    if not os.path.exists(filename):
        # Створюємо кореневий елемент
        root = ET.Element("products")

        # Початкові продукти
        initial_products = [
            {"name": "Молоко", "price": 25, "quantity": 50},
            {"name": "Хліб", "price": 10, "quantity": 100},
            {"name": "Цукор", "price": 35, "quantity": 75},
        ]

        # Додаємо продукти до XML
        for product_data in initial_products:
            product = ET.SubElement(root, "product")

            name = ET.SubElement(product, "name")
            name.text = product_data["name"]

            price = ET.SubElement(product, "price")
            price.text = str(product_data["price"])

            quantity = ET.SubElement(product, "quantity")
            quantity.text = str(product_data["quantity"])

        # Створюємо дерево та зберігаємо
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ", level=0)  # Форматування для читабельності
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        print(f"Створено файл {filename} з початковими продуктами")


def add_product_to_xml(name: str, price: float, quantity: int, filename: str = "products.xml") -> None:
    """
    Додає новий продукт до існуючого XML файлу.
    """
    # Завантажуємо існуючі продукти
    products = read_xml(filename)

    # Перевіряємо, чи вже існує такий продукт
    for product in products:
        if product["name"].lower() == name.lower():
            print(f"Продукт '{name}' вже існує в магазині")
            return

    try:
        # Завантажуємо існуючий XML
        tree = ET.parse(filename)
        root = tree.getroot()

        # Створюємо новий продукт
        product = ET.SubElement(root, "product")

        name_elem = ET.SubElement(product, "name")
        name_elem.text = name

        price_elem = ET.SubElement(product, "price")
        price_elem.text = str(price)

        quantity_elem = ET.SubElement(product, "quantity")
        quantity_elem.text = str(quantity)

        # Зберігаємо оновлений XML
        ET.indent(tree, space="    ", level=0)
        tree.write(filename, encoding="utf-8", xml_declaration=True)

        print(f"Додано продукт '{name}' (ціна: {price} грн, кількість: {quantity}) до {filename}")

    except ET.ParseError as e:
        print(f"Помилка парсингу XML: {e}")
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")


def read_xml(filename: str = "products.xml") -> List[Dict[str, any]]:
    """
    Читає дані з XML файлу та повертає список продуктів.
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        products_data = []

        for product in root.findall('product'):
            product_dict = {
                'name': product.find('name').text if product.find('name') is not None else '',
                'price': float(product.find('price').text) if product.find('price') is not None else 0.0,
                'quantity': int(product.find('quantity').text) if product.find('quantity') is not None else 0
            }
            products_data.append(product_dict)

        return products_data

    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
        return []
    except ET.ParseError as e:
        print(f"Помилка парсингу XML файлу: {e}")
        return []
    except (ValueError, AttributeError) as e:
        print(f"Помилка обробки даних XML: {e}")
        return []


def display_all_products(filename: str = "products.xml") -> None:
    """
    Виводить інформацію про всі продукти.
    """
    products = read_xml(filename)
    if products:
        print("\nВсі продукти в магазині:")
        print(f"{'Назва':<15} {'Ціна (грн)':<12} {'Кількість':<10} {'Вартість (грн)':<15}")
        print("-" * 55)
        for product in products:
            total_value = product['price'] * product['quantity']
            print(f"{product['name']:<15} {product['price']:<12.2f} {product['quantity']:<10} {total_value:<15.2f}")
        print("-" * 55)
    else:
        print("Магазин порожній або файл не знайдено")


def update_product_quantity(name: str, new_quantity: int, filename: str = "products.xml") -> bool:
    """
    Змінює кількість товару та зберігає зміни в XML-файл.

    Args:
        name (str): Назва продукту
        new_quantity (int): Нова кількість
        filename (str): Ім'я файлу. За замовчуванням "products.xml"

    Returns:
        bool: True, якщо продукт знайдено та оновлено
    """
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        # Шукаємо продукт за назвою
        for product in root.findall('product'):
            name_elem = product.find('name')
            if name_elem is not None and name_elem.text.lower() == name.lower():
                # Оновлюємо кількість
                quantity_elem = product.find('quantity')
                if quantity_elem is not None:
                    old_quantity = quantity_elem.text
                    quantity_elem.text = str(new_quantity)

                    # Зберігаємо зміни
                    ET.indent(tree, space="    ", level=0)
                    tree.write(filename, encoding="utf-8", xml_declaration=True)

                    print(f"Оновлено кількість продукту '{name}': {old_quantity} → {new_quantity}")
                    return True

        print(f"Продукт '{name}' не знайдено")
        return False

    except ET.ParseError as e:
        print(f"Помилка парсингу XML: {e}")
        return False
    except FileNotFoundError:
        print(f"Файл {filename} не знайдено")
        return False


def main() -> None:
    """
    Головна функція для демонстрації роботи з XML файлами та магазином продуктів.
    """
    filename = "products.xml"
    create_xml_file(filename)

    display_all_products(filename)

    print("\nДодаємо нові продукти:")
    products_to_add = [
        ("Йогурт", 18.5, 25),
        ("Кефір", 22.0, 35),
    ]

    for name, price, quantity in products_to_add:
        add_product_to_xml(name, price, quantity, filename)

    # Змінюємо кількість товару
    print("\nЗмінюємо кількість товарів:")
    update_product_quantity("Молоко", 80, filename)
    update_product_quantity("Хліб", 150, filename)
    update_product_quantity("Сир", 25, filename)

    display_all_products(filename)


if __name__ == "__main__":
    main()
