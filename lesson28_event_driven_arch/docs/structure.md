## 📁 Структура проекта

```
event-driven-architecture/
│
├── README.md                          # Підсумки та висновки (з артефакту)
├── requirements.txt                   # Залежності
│
├── level_1_basic/                     # 🟢 Рівень 1 - Базовий
│   ├── __init__.py
│   ├── eventbus.py                    # EventBus клас
│   ├── demo_basic.py                  # Демонстрація з 3 подіями та listener-ами
│   └── logs/                          # Логи подій
│       └── .gitkeep
│
├── level_2_intermediate/              # 🟡 Рівень 2 - Середній
│   ├── __init__.py
│   ├── eventbus_queue.py              # EventBus з чергою
│   ├── order_service.py               # Сервіс замовлень
│   ├── notification_service.py        # Сервіс сповіщень
│   ├── analytics_service.py           # Сервіс аналітики
│   ├── main.py                        # Запуск симуляції магазину
│   └── demo_queue.py                  # Демо з чергою та worker-ом
│
├── level_3_advanced/                  # 🔥 Рівень 3 - Просунутий
│   ├── __init__.py
│   │
│   ├── event_replay/                  # Event Replay
│   │   ├── eventbus_replay.py         # EventBus з replay
│   │   ├── demo_replay.py             # Демонстрація
│   │   └── events.log                 # Файл з подіями
│   │
│   ├── rabbitmq_simulation/           # RabbitMQ імітація
│   │   ├── simulated_rabbitmq.py      # Імітація RabbitMQ
│   │   ├── producer.py                # Producer (UserRegistrationService)
│   │   ├── consumer_email.py          # Email Worker
│   │   ├── consumer_analytics.py      # Analytics Worker
│   │   ├── main.py                    # Запуск всієї системи
│   │   └── README_RABBITMQ.md         # Інструкції для реального RabbitMQ
│   │
│   └── webhook/                       # Webhook Server
│       ├── webhook_server.py          # Flask сервер
│       ├── eventbus_webhook.py        # EventBus для webhook
│       ├── test_webhook.sh            # Скрипт для тестування curl
│       └── README_WEBHOOK.md          # Інструкції
│
├── level_4_hard/                      # 💎 Рівень 4 - Hard Mode
│   ├── __init__.py
│   │
│   ├── file_kafka/                    # Kafka на файлах
│   │   ├── producer.py                # Producer
│   │   ├── consumer.py                # Consumer
│   │   ├── demo.py                    # Повна демонстрація
│   │   └── kafka_data/                # Директорія для топіків
│   │       ├── orders.log             # Topic файл
│   │       ├── consumer_1_offset.txt  # Offset consumer-а 1
│   │       └── consumer_2_offset.txt  # Offset consumer-а 2
│   │
│   └── saga_pattern/                  # Saga Pattern
│       ├── saga_orchestrator.py       # Оркестратор
│       ├── inventory_service.py       # Сервіс складу
│       ├── payment_service.py         # Сервіс оплати
│       ├── delivery_service.py        # Сервіс доставки
│       ├── demo.py                    # Демонстрація різних сценаріїв
│       └── saga_logs/                 # Логи Saga
│           └── .gitkeep
│
├── common/                            # 🔧 Спільні утиліти
│   ├── __init__.py
│   ├── base_eventbus.py               # Базовий клас EventBus
│   └── logger.py                      # Загальний logger
│
├── examples/                          # 📚 Додаткові приклади
│   ├── simple_pub_sub.py              # Найпростіший приклад pub/sub
│   ├── multiple_workers.py            # Приклад з кількома worker-ами
│   └── error_handling.py              # Приклад обробки помилок
│
├── tests/                             # 🧪 Тести
│   ├── __init__.py
│   ├── test_eventbus.py
│   ├── test_queue.py
│   ├── test_replay.py
│   └── test_saga.py
│
├── docker/                            # 🐳 Docker конфігурації
│   ├── docker-compose.yml             # RabbitMQ, Redis
│   └── Dockerfile                     # Для деплою
│
└── docs/                              # 📖 Документація
    ├── architecture.md                # Архітектурна діаграма
    ├── patterns.md                    # Опис паттернів
    └── deployment.md                  # Гайд по деплою
```

---

## 📝 **requirements.txt**

```txt
# Level 3 - Webhook
flask==3.0.0

# Level 3 - Real RabbitMQ (опціонально)
pika==1.3.2

# Для тестів
pytest==7.4.3
pytest-asyncio==0.21.1

# Utilities
python-dotenv==1.0.0
```

---

## 🚀 **Швидкий старт**

```bash
# Клонувати структуру
mkdir event-driven-architecture
cd event-driven-architecture

# Створити віртуальне середовище
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate     # Windows

# Встановити залежності
pip install -r requirements.txt

# Запустити приклади по рівнях
python level_1_basic/demo_basic.py
python level_2_intermediate/main.py
python level_3_advanced/event_replay/demo_replay.py
python level_3_advanced/webhook/webhook_server.py
python level_4_hard/file_kafka/demo.py
python level_4_hard/saga_pattern/demo.py
```

---

## 🎯 **Альтернативна структура (спрощена)**

Якщо хочеш простішу структуру без підпапок:

```
event-driven-architecture/
│
├── README.md
├── requirements.txt
│
├── 1_eventbus_basic.py              # Рівень 1
├── 2_shop_simulation.py             # Рівень 2, завдання 3
├── 3_event_queue.py                 # Рівень 2, завдання 4
├── 4_event_replay.py                # Рівень 3, завдання 5
├── 5_rabbitmq_simple.py             # Рівень 3, завдання 6
├── 6_webhook_server.py              # Рівень 3, завдання 7
├── 7_file_kafka.py                  # Рівень 4, завдання 8
├── 8_saga_pattern.py                # Рівень 4, завдання 9
│
├── events.log                        # Для event replay
├── kafka_data/                       # Для file kafka
└── logs/                             # Загальні логи
```

Ця структура **простіша для навчання** - один файл = одне завдання! 🎓