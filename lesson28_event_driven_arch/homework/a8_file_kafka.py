"""
KAFKA НА ФАЙЛАХ - розуміння log-based storage

Це спрощена версія того, як працює Apache Kafka:
- Producer пише повідомлення в кінець файлу (append-only log)
- Consumer читає з певного offset-у
- Кожен consumer зберігає свій offset

ЦЕ ДОПОМАГАЄ ЗРОЗУМІТИ:
1. Що таке offset
2. Як масштабується Kafka
3. Чому Kafka такий швидкий
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


# ====================================
# FILE-BASED KAFKA PRODUCER
# ====================================

class FileKafkaProducer:
    """Producer що пише повідомлення в файл"""

    def __init__(self, topic: str, data_dir: str = "kafka_data"):
        self.topic = topic
        self.data_dir = data_dir
        self.topic_file = os.path.join(data_dir, f"{topic}.log")

        # Створюємо директорію якщо не існує
        os.makedirs(data_dir, exist_ok=True)

        # Якщо файл не існує - створюємо
        if not os.path.exists(self.topic_file):
            with open(self.topic_file, 'w') as f:
                pass
            print(f"✅ Topic '{topic}' створено")

    def send(self, message: dict):
        """Відправити повідомлення (append в кінець файлу)"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "message": message
        }

        # Дописуємо в кінець файлу (append-only)
        with open(self.topic_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

        print(f"📤 Producer -> {self.topic}: {message}")


# ====================================
# FILE-BASED KAFKA CONSUMER
# ====================================

class FileKafkaConsumer:
    """Consumer що читає з певного offset-у"""

    def __init__(self, topic: str, consumer_id: str, data_dir: str = "kafka_data"):
        self.topic = topic
        self.consumer_id = consumer_id
        self.data_dir = data_dir
        self.topic_file = os.path.join(data_dir, f"{topic}.log")
        self.offset_file = os.path.join(data_dir, f"{consumer_id}_offset.txt")

        # Завантажуємо поточний offset
        self.current_offset = self._load_offset()
        print(f"✅ Consumer '{consumer_id}' підключився до '{topic}' (offset: {self.current_offset})")

    def _load_offset(self) -> int:
        """Завантажити збережений offset"""
        if os.path.exists(self.offset_file):
            with open(self.offset_file, 'r') as f:
                return int(f.read().strip())
        return 0

    def _save_offset(self):
        """Зберегти поточний offset"""
        with open(self.offset_file, 'w') as f:
            f.write(str(self.current_offset))

    def poll(self, max_messages: int = 10) -> List[Dict]:
        """
        Прочитати нові повідомлення з offset-у

        Це як Kafka's consumer.poll():
        - Читає тільки нові повідомлення
        - Оновлює offset
        """
        messages = []

        if not os.path.exists(self.topic_file):
            return messages

        with open(self.topic_file, 'r', encoding='utf-8') as f:
            # Пропускаємо рядки до current_offset
            for _ in range(self.current_offset):
                f.readline()

            # Читаємо нові повідомлення
            for _ in range(max_messages):
                line = f.readline()
                if not line:
                    break

                try:
                    record = json.loads(line.strip())
                    messages.append(record)
                    self.current_offset += 1
                except json.JSONDecodeError:
                    continue

        # Зберігаємо новий offset
        self._save_offset()

        if messages:
            print(
                f"📥 Consumer '{self.consumer_id}' прочитав {len(messages)} повідомлень (новий offset: {self.current_offset})")

        return messages

    def reset_offset(self, offset: int = 0):
        """Скинути offset (для replay)"""
        self.current_offset = offset
        self._save_offset()
        print(f"🔄 Consumer '{self.consumer_id}' offset скинуто на {offset}")

    def get_total_messages(self) -> int:
        """Скільки всього повідомлень в топіку"""
        if not os.path.exists(self.topic_file):
            return 0

        with open(self.topic_file, 'r') as f:
            return sum(1 for _ in f)


# ====================================
# ДЕМОНСТРАЦІЯ
# ====================================

if __name__ == "__main__":
    print("=" * 60)
    print("FILE-BASED KAFKA - Log Storage Demo")
    print("=" * 60 + "\n")

    # Очищаємо старі дані
    import shutil

    if os.path.exists("kafka_data"):
        shutil.rmtree("kafka_data")

    # ====================================
    # СЦЕНАРІЙ 1: Producer пише повідомлення
    # ====================================

    print("\n📤 PRODUCER: Відправляємо повідомлення\n")

    producer = FileKafkaProducer("orders")

    producer.send({"order_id": 1, "amount": 100})
    producer.send({"order_id": 2, "amount": 200})
    producer.send({"order_id": 3, "amount": 300})
    producer.send({"order_id": 4, "amount": 400})
    producer.send({"order_id": 5, "amount": 500})

    # ====================================
    # СЦЕНАРІЙ 2: Consumer 1 читає
    # ====================================

    print("\n" + "=" * 60)
    print("📥 CONSUMER 1: Читаємо перші 3 повідомлення")
    print("=" * 60 + "\n")

    consumer1 = FileKafkaConsumer("orders", "consumer_1")
    messages = consumer1.poll(max_messages=3)

    for msg in messages:
        print(f"  ✅ Оброблено: {msg['message']}")

    # ====================================
    # СЦЕНАРІЙ 3: Producer додає ще
    # ====================================

    print("\n" + "=" * 60)
    print("📤 PRODUCER: Додаємо ще повідомлення")
    print("=" * 60 + "\n")

    producer.send({"order_id": 6, "amount": 600})
    producer.send({"order_id": 7, "amount": 700})

    # ====================================
    # СЦЕНАРІЙ 4: Consumer 1 читає нові
    # ====================================

    print("\n" + "=" * 60)
    print("📥 CONSUMER 1: Читаємо нові повідомлення")
    print("=" * 60 + "\n")

    messages = consumer1.poll(max_messages=10)

    for msg in messages:
        print(f"  ✅ Оброблено: {msg['message']}")

    # ====================================
    # СЦЕНАРІЙ 5: Consumer 2 читає ВСЕ з початку
    # ====================================

    print("\n" + "=" * 60)
    print("📥 CONSUMER 2: Новий consumer (читає з початку)")
    print("=" * 60 + "\n")

    consumer2 = FileKafkaConsumer("orders", "consumer_2")
    messages = consumer2.poll(max_messages=100)

    print(f"Consumer 2 прочитав {len(messages)} повідомлень:")
    for msg in messages:
        print(f"  ✅ {msg['message']}")

    # ====================================
    # СЦЕНАРІЙ 6: Consumer 1 робить REPLAY
    # ====================================

    print("\n" + "=" * 60)
    print("🔄 CONSUMER 1: Replay - перечитуємо все з початку")
    print("=" * 60 + "\n")

    consumer1.reset_offset(0)
    messages = consumer1.poll(max_messages=100)

    print(f"Consumer 1 перечитав {len(messages)} повідомлень:")
    for msg in messages:
        print(f"  ✅ {msg['message']}")

    # ====================================
    # СТАТИСТИКА
    # ====================================

    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)
    print(f"Всього повідомлень в топіку: {consumer1.get_total_messages()}")
    print(f"Consumer 1 offset: {consumer1.current_offset}")
    print(f"Consumer 2 offset: {consumer2.current_offset}")

    # ====================================
    # ВИСНОВКИ
    # ====================================

    print("\n" + "=" * 60)
    print("💡 ЩО МИ ДІЗНАЛИСЯ:")
    print("=" * 60)
    print("1️⃣  Offset - це позиція consumer-а в логі")
    print("2️⃣  Кожен consumer має свій offset (незалежні)")
    print("3️⃣  Producer просто дописує в кінець (append-only)")
    print("4️⃣  Можна перечитати (replay) історію скинувши offset")
    print("5️⃣  Це дозволяє масштабувати Kafka горизонтально")

    print("\n📌 ЯК ЦЕ ПРАЦЮЄ В KAFKA:")
    print("   - Topic розбивається на партиції (файли)")
    print("   - Кожна партиція - це append-only лог")
    print("   - Consumer group координує offset між consumer-ами")
    print("   - Це дає величезну швидкість (10M+ msg/sec)")

    print("\n🔥 Файл з повідомленнями: kafka_data/orders.log")
    print("🔥 Offset consumer-ів: kafka_data/*_offset.txt")