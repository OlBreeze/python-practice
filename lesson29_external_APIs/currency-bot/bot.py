import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
import telebot
from telebot import types

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Инициализация бота
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')

if not TELEGRAM_TOKEN or not EXCHANGE_API_KEY:
    logger.error("Отсутствуют токены в .env файле!")
    raise ValueError("Необходимо указать TELEGRAM_BOT_TOKEN и EXCHANGE_API_KEY в .env файле")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Базовый URL для API курсов валют
BASE_URL = "https://v6.exchangerate-api.com/v6"

# Популярные валюты
CURRENCIES = {
    'USD': '🇺🇸 Доллар США',
    'EUR': '🇪🇺 Евро',
    'UAH': '🇺🇦 Гривна',
    'GBP': '🇬🇧 Фунт стерлингов',
    'PLN': '🇵🇱 Польский злотый',
    'RUB': '🇷🇺 Российский рубль'
}

# Хранилище для временных данных пользователей
user_data = {}


def get_exchange_rate(from_currency, to_currency):
    """Получает курс обмена валют"""
    try:
        url = f"{BASE_URL}/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}"

        logger.info(f"Запрос курса: {from_currency} -> {to_currency}")

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()

            if data['result'] == 'success':
                rate = data['conversion_rate']
                logger.info(f"Успешно получен курс: {from_currency}/{to_currency} = {rate}")
                return rate
            else:
                logger.error(f"Ошибка API: {data.get('error-type', 'Unknown error')}")
                return None
        else:
            logger.error(f"HTTP ошибка: {response.status_code}")
            return None

    except requests.exceptions.Timeout:
        logger.error("Превышено время ожидания запроса")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return None


def create_currency_keyboard():
    """Создает клавиатуру с валютами"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(f"{code} - {name}") for code, name in CURRENCIES.items()]
    markup.add(*buttons)
    markup.add(types.KeyboardButton("❌ Отмена"))
    return markup


def create_main_keyboard():
    """Создает главную клавиатуру"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("💱 Обмен валют"),
        types.KeyboardButton("ℹ️ Помощь")
    )
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start"""
    user_name = message.from_user.first_name
    welcome_text = f"""
Привет, {user_name}! 👋

Я бот для обмена валют 💱

Я помогу тебе узнать актуальные курсы валют.

Используй кнопки ниже или команды:
/help - помощь
/exchange - обмен валют
"""

    logger.info(f"Пользователь {message.from_user.id} ({user_name}) запустил бота")

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    help_text = """
📖 <b>Доступные команды:</b>

/start - Начать работу с ботом
/help - Показать это сообщение
/exchange - Обменять валюту

💱 <b>Как использовать:</b>

1. Нажмите "Обмен валют" или используйте /exchange
2. Выберите валюту, которую хотите обменять
3. Выберите валюту, которую хотите получить
4. Введите сумму для обмена

<b>Поддерживаемые валюты:</b>
🇺🇸 USD - Доллар США
🇪🇺 EUR - Евро
🇺🇦 UAH - Гривна
🇬🇧 GBP - Фунт стерлингов
🇵🇱 PLN - Польский злотый
🇷🇺 RUB - Российский рубль
"""

    logger.info(f"Пользователь {message.from_user.id} запросил помощь")

    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='HTML',
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['exchange'])
def start_exchange(message):
    """Начало процесса обмена валют"""
    user_id = message.chat.id
    user_data[user_id] = {'step': 'from_currency'}

    logger.info(f"Пользователь {user_id} начал процесс обмена")

    bot.send_message(
        user_id,
        "💱 <b>Обмен валют</b>\n\nВыберите валюту, которую хотите обменять:",
        parse_mode='HTML',
        reply_markup=create_currency_keyboard()
    )


@bot.message_handler(func=lambda message: message.text == "💱 Обмен валют")
def exchange_button(message):
    """Обработчик кнопки 'Обмен валют'"""
    start_exchange(message)


@bot.message_handler(func=lambda message: message.text == "ℹ️ Помощь")
def help_button(message):
    """Обработчик кнопки 'Помощь'"""
    send_help(message)


@bot.message_handler(func=lambda message: message.text == "❌ Отмена")
def cancel_operation(message):
    """Отмена текущей операции"""
    user_id = message.chat.id

    if user_id in user_data:
        del user_data[user_id]
        logger.info(f"Пользователь {user_id} отменил операцию")

    bot.send_message(
        user_id,
        "❌ Операция отменена",
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех текстовых сообщений"""
    user_id = message.chat.id
    text = message.text

    # Проверяем, есть ли пользователь в процессе обмена
    if user_id not in user_data:
        bot.send_message(
            user_id,
            "Используйте кнопки или команды для работы с ботом",
            reply_markup=create_main_keyboard()
        )
        return

    step = user_data[user_id]['step']

    # Шаг 1: Выбор исходной валюты
    if step == 'from_currency':
        currency_code = text.split(' - ')[0].strip()

        if currency_code in CURRENCIES:
            user_data[user_id]['from_currency'] = currency_code
            user_data[user_id]['step'] = 'to_currency'

            logger.info(f"Пользователь {user_id} выбрал исходную валюту: {currency_code}")

            bot.send_message(
                user_id,
                f"Вы выбрали: {CURRENCIES[currency_code]}\n\nТеперь выберите валюту, которую хотите получить:",
                reply_markup=create_currency_keyboard()
            )
        else:
            bot.send_message(
                user_id,
                "❌ Пожалуйста, выберите валюту из списка",
                reply_markup=create_currency_keyboard()
            )

    # Шаг 2: Выбор целевой валюты
    elif step == 'to_currency':
        currency_code = text.split(' - ')[0].strip()

        if currency_code in CURRENCIES:
            from_curr = user_data[user_id]['from_currency']

            if currency_code == from_curr:
                bot.send_message(
                    user_id,
                    "❌ Нельзя обменять валюту саму на себя. Выберите другую валюту:",
                    reply_markup=create_currency_keyboard()
                )
                return

            user_data[user_id]['to_currency'] = currency_code
            user_data[user_id]['step'] = 'amount'

            logger.info(f"Пользователь {user_id} выбрал целевую валюту: {currency_code}")

            # Убираем клавиатуру для ввода суммы
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("❌ Отмена"))

            bot.send_message(
                user_id,
                f"Вы выбрали: {CURRENCIES[currency_code]}\n\nВведите сумму для обмена (число):",
                reply_markup=markup
            )
        else:
            bot.send_message(
                user_id,
                "❌ Пожалуйста, выберите валюту из списка",
                reply_markup=create_currency_keyboard()
            )

    # Шаг 3: Ввод суммы и расчет
    elif step == 'amount':
        try:
            amount = float(text.replace(',', '.'))

            if amount <= 0:
                bot.send_message(
                    user_id,
                    "❌ Сумма должна быть больше 0. Попробуйте еще раз:"
                )
                return

            from_curr = user_data[user_id]['from_currency']
            to_curr = user_data[user_id]['to_currency']

            logger.info(f"Пользователь {user_id} запросил обмен: {amount} {from_curr} -> {to_curr}")

            # Получаем курс
            bot.send_message(user_id, "⏳ Получаю актуальный курс...")

            rate = get_exchange_rate(from_curr, to_curr)

            if rate:
                result = amount * rate

                result_text = f"""
💱 <b>Результат обмена</b>

<b>Из:</b> {amount:.2f} {from_curr} ({CURRENCIES[from_curr]})
<b>В:</b> {result:.2f} {to_curr} ({CURRENCIES[to_curr]})

<b>Курс:</b> 1 {from_curr} = {rate:.4f} {to_curr}

<i>Данные на {datetime.now().strftime('%d.%m.%Y %H:%M')}</i>
"""

                bot.send_message(
                    user_id,
                    result_text,
                    parse_mode='HTML',
                    reply_markup=create_main_keyboard()
                )

                logger.info(f"Успешно выполнен обмен для пользователя {user_id}")

            else:
                bot.send_message(
                    user_id,
                    "❌ Не удалось получить курс валют. Попробуйте позже.",
                    reply_markup=create_main_keyboard()
                )

                logger.error(f"Не удалось получить курс для пользователя {user_id}")

            # Очищаем данные пользователя
            del user_data[user_id]

        except ValueError:
            bot.send_message(
                user_id,
                "❌ Пожалуйста, введите корректное число (например: 100 или 100.50)"
            )


# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен и готов к работе")
    print("🤖 Бот запущен...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise