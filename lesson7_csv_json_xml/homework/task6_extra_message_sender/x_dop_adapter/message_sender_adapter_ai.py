#  Як використовувати:
#
# Запустіть програму - вона створить тестові файли
# Створіть власні файли з даними у форматі CSV/JSON/XML
# Програма автоматично знайде та оброблятиме ваші файли
# Результати будуть збережені в нові файли

import json
import csv
import xml.etree.ElementTree as ET
from io import StringIO
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import logging

# Налаштування логування для обробки помилок
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================
# ЧАСТИНА 1: СИСТЕМА ВІДПРАВКИ ПОВІДОМЛЕНЬ
# ======================================

# Інтерфейс MessageSender
class MessageSender(ABC):
    @abstractmethod
    def send_message(self, message: str):
        pass


# Існуючі класи для відправки повідомлень
class SMSService:
    def send_sms(self, phone_number: str, message: str):
        print(f"📱 Відправка SMS на {phone_number}: {message}")
        # Симуляція можливої помилки
        if not phone_number.startswith('+'):
            raise ValueError("Неправильний формат номера телефону")


class EmailService:
    def send_email(self, email_address: str, message: str):
        print(f"📧 Відправка Email на {email_address}: {message}")
        # Симуляція можливої помилки
        if '@' not in email_address:
            raise ValueError("Неправильний формат email адреси")


class PushService:
    def send_push(self, device_id: str, message: str):
        print(f"📲 Відправка Push-повідомлення на пристрій {device_id}: {message}")
        # Симуляція можливої помилки
        if len(device_id) < 5:
            raise ValueError("Неправильний формат ID пристрою")


# Адаптери з обробкою помилок
class SMSAdapter(MessageSender):
    def __init__(self, sms_service: SMSService, phone_number: str):
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str):
        try:
            self.sms_service.send_sms(self.phone_number, message)
            logger.info(f"SMS успішно відправлено на {self.phone_number}")
        except Exception as e:
            logger.error(f"Помилка відправки SMS на {self.phone_number}: {e}")
            raise


class EmailAdapter(MessageSender):
    def __init__(self, email_service: EmailService, email_address: str):
        self.email_service = email_service
        self.email_address = email_address

    def send_message(self, message: str):
        try:
            self.email_service.send_email(self.email_address, message)
            logger.info(f"Email успішно відправлено на {self.email_address}")
        except Exception as e:
            logger.error(f"Помилка відправки Email на {self.email_address}: {e}")
            raise


class PushAdapter(MessageSender):
    def __init__(self, push_service: PushService, device_id: str):
        self.push_service = push_service
        self.device_id = device_id

    def send_message(self, message: str):
        try:
            self.push_service.send_push(self.device_id, message)
            logger.info(f"Push-повідомлення успішно відправлено на {self.device_id}")
        except Exception as e:
            logger.error(f"Помилка відправки Push на {self.device_id}: {e}")
            raise


# Система відправки повідомлень через декілька сервісів
class MessageBroadcaster:
    def __init__(self, adapters: List[MessageSender]):
        self.adapters = adapters

    def broadcast_message(self, message: str):
        """Відправляє повідомлення через всі доступні сервіси"""
        successful_sends = 0
        failed_sends = 0

        for adapter in self.adapters:
            try:
                adapter.send_message(message)
                successful_sends += 1
            except Exception as e:
                failed_sends += 1
                continue

        print(f"\n📊 Результат розсилки:")
        print(f"✅ Успішно відправлено: {successful_sends}")
        print(f"❌ Помилок: {failed_sends}")


# ======================================
# ЧАСТИНА 2: ПЕРЕТВОРЕННЯ ФОРМАТІВ ФАЙЛІВ
# ======================================

class DataConverter(ABC):
    @abstractmethod
    def convert(self, data: str) -> str:
        pass


# Існуючі класи для роботи з різними форматами
class CSVProcessor:
    def parse_csv(self, csv_data: str) -> List[Dict[str, Any]]:
        """Парсить CSV дані і повертає список словників"""
        reader = csv.DictReader(StringIO(csv_data))
        return list(reader)

    def create_csv(self, data: List[Dict[str, Any]]) -> str:
        """Створює CSV строку з списку словників"""
        if not data:
            return ""

        output = StringIO()
        fieldnames = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()


class JSONProcessor:
    def parse_json(self, json_data: str) -> List[Dict[str, Any]]:
        """Парсить JSON дані"""
        return json.loads(json_data)

    def create_json(self, data: List[Dict[str, Any]]) -> str:
        """Створює JSON строку"""
        return json.dumps(data, ensure_ascii=False, indent=2)


class XMLProcessor:
    def parse_xml(self, xml_data: str) -> List[Dict[str, Any]]:
        """Парсить XML дані і повертає список словників"""
        root = ET.fromstring(xml_data)
        result = []

        # Припускаємо, що XML має структуру з повторюваними елементами
        for item in root:
            item_dict = {}
            if item.text and item.text.strip():
                item_dict['text'] = item.text.strip()

            # Додаємо атрибути
            item_dict.update(item.attrib)

            # Додаємо дочірні елементи
            for child in item:
                if child.text and child.text.strip():
                    item_dict[child.tag] = child.text.strip()
                if child.attrib:
                    for attr, value in child.attrib.items():
                        item_dict[f"{child.tag}_{attr}"] = value

            result.append(item_dict)

        return result


# Адаптери для перетворення форматів
class CSVToJSONAdapter(DataConverter):
    def __init__(self):
        self.csv_processor = CSVProcessor()
        self.json_processor = JSONProcessor()

    def convert(self, csv_data: str) -> str:
        """Перетворює CSV в JSON"""
        try:
            parsed_data = self.csv_processor.parse_csv(csv_data)
            return self.json_processor.create_json(parsed_data)
        except Exception as e:
            logger.error(f"Помилка перетворення CSV в JSON: {e}")
            raise


class JSONToCSVAdapter(DataConverter):
    def __init__(self):
        self.json_processor = JSONProcessor()
        self.csv_processor = CSVProcessor()

    def convert(self, json_data: str) -> str:
        """Перетворює JSON в CSV"""
        try:
            parsed_data = self.json_processor.parse_json(json_data)
            return self.csv_processor.create_csv(parsed_data)
        except Exception as e:
            logger.error(f"Помилка перетворення JSON в CSV: {e}")
            raise


class XMLToJSONAdapter(DataConverter):
    def __init__(self):
        self.xml_processor = XMLProcessor()
        self.json_processor = JSONProcessor()

    def convert(self, xml_data: str) -> str:
        """Перетворює XML в JSON"""
        try:
            parsed_data = self.xml_processor.parse_xml(xml_data)
            return self.json_processor.create_json(parsed_data)
        except Exception as e:
            logger.error(f"Помилка перетворення XML в JSON: {e}")
            raise


# ======================================
# РОБОТА З ТЕСТОВИМИ ФАЙЛАМИ
# ======================================

class TestDataLoader:
    """Клас для завантаження тестових даних з файлів"""

    @staticmethod
    def load_test_data(filename: str) -> str:
        """Завантажує тестові дані з файлу"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            logger.warning(f"Файл {filename} не знайдено. Використовуємо вбудовані дані.")
            return TestDataLoader.get_fallback_data(filename)
        except Exception as e:
            logger.error(f"Помилка читання файлу {filename}: {e}")
            return TestDataLoader.get_fallback_data(filename)

    @staticmethod
    def get_fallback_data(filename: str) -> str:
        """Повертає резервні дані, якщо файл недоступний"""
        fallback_data = {
            'test_data.csv': """name,age,city
Іван,25,Київ
Марія,30,Львів
Петро,35,Одеса""",

            'test_data.json': """[
  {"name": "Анна", "age": 28, "city": "Харків"},
  {"name": "Олег", "age": 32, "city": "Дніпро"}
]""",

            'test_data.xml': """<?xml version="1.0" encoding="UTF-8"?>
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
        }
        return fallback_data.get(filename, "")

    @staticmethod
    def create_test_files():
        """Створює тестові файли з даними"""
        test_files = {
            'test_data.csv': """name,age,city
Іван,25,Київ
Марія,30,Львів
Петро,35,Одеса
Олександр,28,Запоріжжя
Катерина,31,Чернівці""",

            'test_data.json': """[
  {"name": "Анна", "age": 28, "city": "Харків"},
  {"name": "Олег", "age": 32, "city": "Дніпро"},
  {"name": "Тетяна", "age": 26, "city": "Суми"},
  {"name": "Віктор", "age": 29, "city": "Кропивницький"}
]""",

            'test_data.xml': """<?xml version="1.0" encoding="UTF-8"?>
<people>
    <person id="1">
        <name>Світлана</name>
        <age>27</age>
        <city>Полтава</city>
        <profession>Вчитель</profession>
    </person>
    <person id="2">
        <name>Максим</name>
        <age>33</age>
        <city>Вінниця</city>
        <profession>Інженер</profession>
    </person>
    <person id="3">
        <name>Ольга</name>
        <age>24</age>
        <city>Луцьк</city>
        <profession>Дизайнер</profession>
    </person>
</people>"""
        }

        for filename, content in test_files.items():
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"✅ Створено файл: {filename}")
            except Exception as e:
                logger.error(f"Помилка створення файлу {filename}: {e}")


# ======================================
# ДЕМОНСТРАЦІЯ ВИКОРИСТАННЯ
# ======================================

def demo_messaging_system():
    print("=" * 50)
    print("ДЕМОНСТРАЦІЯ СИСТЕМИ ПОВІДОМЛЕНЬ")
    print("=" * 50)

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
    print("\n\n" + "=" * 50)
    print("ДЕМОНСТРАЦІЯ ПЕРЕТВОРЕННЯ ФАЙЛІВ")
    print("=" * 50)

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


if __name__ == "__main__":
    # Запуск демонстрацій
    demo_messaging_system()
    demo_file_conversion()
    # demo_custom_data_files()

    print("\n\n" + "=" * 50)
    print("СТВОРЕНІ ФАЙЛИ")
    print("=" * 50)
    print("📁 Тестові файли:")
    print("   ├── test_data.csv")
    print("   ├── test_data.json")
    print("   └── test_data.xml")
    print("\n📁 Результати конвертації:")
    print("   ├── converted_csv_to_json.json")
    print("   ├── converted_json_to_csv.csv")
    print("   └── converted_xml_to_json.json")

    print("\n" + "=" * 50)
    print("ВИСНОВОК")
    print("=" * 50)
    print("Паттерн Адаптер успішно реалізовано для:")
    print("✅ Уніфікації систем відправки повідомлень")
    print("✅ Перетворення між форматами файлів")
    print("✅ Обробки помилок та логування")
    print("✅ Масової розсилки повідомлень")
    print("✅ Роботи з зовнішніми файлами даних")
    print("✅ Автоматичного створення тестових файлів")