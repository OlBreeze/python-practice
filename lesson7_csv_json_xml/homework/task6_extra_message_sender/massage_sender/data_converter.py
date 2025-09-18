"""
ЧАСТИНА 2: ПЕРЕТВОРЕННЯ ФОРМАТІВ ФАЙЛІВ
Перетворення між форматами:

Реалізуй класи, які перетворюватимуть CSV-файл до JSON та навпаки.
Додай функціонал для перетворення XML-файлу до JSON.
"""
import csv
import json
import xml.etree.ElementTree as ET
import logging
from abc import abstractmethod, ABC
from io import StringIO
from typing import List, Dict, Any

# Налаштування логування для обробки помилок
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Получает логгер с именем, равным текущему модулю (__name__).

class DataConverter(ABC):
    @abstractmethod
    def convert(self, data: str) -> str:
        pass


# Існуючі класи для роботи з різними форматами
class CSVProcessor:
    def parse_csv(self, csv_data: str) -> List[Dict[str, Any]]:
        """Парсить CSV дані і повертає список словників"""
        reader = csv.DictReader(StringIO(csv_data)) # StringIO — это класс из модуля io в Python, который позволяет работать со строкой как с файловым объектом. Это очень удобно, когда ты хочешь использовать функции, которые читают или пишут в файл, но вместо настоящего файла использовать строку в памяти
        return list(reader)

    def create_csv(self, data: List[Dict[str, Any]]) -> str:
        """Створює CSV строку з списку словників"""
        if not data:
            return ""

        output = StringIO() # Создаёт временный файловый объект в памяти для записи текста (в данном случае CSV).
        fieldnames = data[0].keys() # Получает имена столбцов (заголовки CSV) из ключей первого словаря
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue() # Возвращает строку CSV целиком


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
