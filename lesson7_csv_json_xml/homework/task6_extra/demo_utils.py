"""
ДЕМОНСТРАЦІЯ ВИКОРИСТАННЯ
"""
from data_converter import CSVToJSONAdapter, JSONToCSVAdapter, XMLToJSONAdapter
from message_service import *


def demo_messaging_system():
    print("ДЕМОНСТРАЦІЯ СИСТЕМИ ПОВІДОМЛЕНЬ")
    print("-" * 50)

    # Створення сервісів
    sms_service = SMSService()
    email_service = EmailService()
    push_service = PushService()

    # Створення адаптерів
    sms_adapter = SMSAdapter(sms_service, "+380123456789")
    email_adapter = EmailAdapter(email_service, "user@example.com")
    push_adapter = PushAdapter(push_service, "device123456")

    # Тестове повідомлення
    message = "Привіт! Це тестове повідомлення через паттерн Адаптер."

    print("\n1. Індивідуальна відправка через кожен адаптер:")
    print("-" * 50)

    # Відправка через кожен адаптер окремо
    try:
        sms_adapter.send_message(message)
    except Exception as e:
        print(f"Помилка SMS: {e}")

    try:
        email_adapter.send_message(message)
    except Exception as e:
        print(f"Помилка Email: {e}")

    try:
        push_adapter.send_message(message)
    except Exception as e:
        print(f"Помилка Push: {e}")

    print("\n2. Масова розсилка через MessageBroadcaster:")
    print("-" * 50)

    # Створення системи масової розсилки
    broadcaster = MessageBroadcaster([sms_adapter, email_adapter, push_adapter])
    broadcaster.broadcast_message("Масове повідомлення для всіх сервісів!")

    print("\n3. Тестування обробки помилок:")
    print("-" * 50)

    # Тестування з неправильними даними
    faulty_adapters = [
        SMSAdapter(sms_service, "123456789"),  # Без +
        EmailAdapter(email_service, "invalid-email"),  # Без @
        PushAdapter(push_service, "123")  # Короткий ID
    ]

    faulty_broadcaster = MessageBroadcaster(faulty_adapters)
    faulty_broadcaster.broadcast_message("Тест з помилками")


def demo_file_conversion():
    print("ДЕМОНСТРАЦІЯ ПЕРЕТВОРЕННЯ ФАЙЛІВ")
    print("-" * 50)

    # Тестові дані
    csv_data = """name,age,city
Іван,25,Київ
Марія,30,Львів
Петро,35,Одеса"""

    json_data = """[
  {"name": "Анна", "age": 28, "city": "Харків"},
  {"name": "Олег", "age": 32, "city": "Дніпро"}
]"""

    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<people>
    <person>
        <name>Світлана</name>
        <age>27</age>
        <city>Полтава</city>
    </person>
    <person>
        <name>Максим</name>
        <age>33</age>
        <city>Вінниця</city>
    </person>
</people>"""

    # Створення адаптерів
    csv_to_json = CSVToJSONAdapter()
    json_to_csv = JSONToCSVAdapter()
    xml_to_json = XMLToJSONAdapter()

    print("\n1. Перетворення CSV в JSON:")
    print("-" * 30)
    print("Початкові CSV дані:")
    print(csv_data)

    try:
        json_result = csv_to_json.convert(csv_data)
        print("\nРезультат JSON:")
        print(json_result)
    except Exception as e:
        print(f"Помилка: {e}")

    print("\n2. Перетворення JSON в CSV:")
    print("-" * 30)
    print("Початкові JSON дані:")
    print(json_data)

    try:
        csv_result = json_to_csv.convert(json_data)
        print("\nРезультат CSV:")
        print(csv_result)
    except Exception as e:
        print(f"Помилка: {e}")

    print("\n3. Перетворення XML в JSON:")
    print("-" * 30)
    print("Початкові XML дані:")
    print(xml_data)

    try:
        json_from_xml = xml_to_json.convert(xml_data)
        print("\nРезультат JSON:")
        print(json_from_xml)
    except Exception as e:
        print(f"Помилка: {e}")
