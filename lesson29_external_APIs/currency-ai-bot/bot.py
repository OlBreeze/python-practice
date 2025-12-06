import os
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv
import telebot
from telebot import types
import google.generativeai as genai

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

# Инициализация токенов
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Проверка токенов
if not TELEGRAM_TOKEN:
    print("❌ ОШИБКА: TELEGRAM_BOT_TOKEN не найден!")
    exit(1)

if ':' not in TELEGRAM_TOKEN:
    print("❌ ОШИБКА: Неверный формат TELEGRAM_BOT_TOKEN!")
    exit(1)

if not EXCHANGE_API_KEY:
    print("❌ ОШИБКА: EXCHANGE_API_KEY не найден!")
    exit(1)

if not GEMINI_API_KEY:
    print("⚠️ ВНИМАНИЕ: GEMINI_API_KEY не найден!")
    print("AI функции будут отключены")
    AI_ENABLED = False
else:
    # Настройка Gemini AI
    genai.configure(api_key=GEMINI_API_KEY)
    ai_model = genai.GenerativeModel('gemini-2.0-flash-exp')
    AI_ENABLED = True
    logger.info("Gemini AI инициализирован")

logger.info("Токены загружены успешно")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Базовый URL для API курсов валют
BASE_URL = "https://v6.exchangerate-api.com/v6"

# Популярные валюты
CURRENCIES = {
    'USD': '🇺🇸 Доллар США',
    'EUR': '🇪🇺 Евро',
    'UAH': '🇺🇦 Гривна',
    'ILS': '🇮🇱 Шекель',
    'PLN': '🇵🇱 Польский злотый',
    'RUB': '🇷🇺 Российский рубль',
    'JPY': '🇯🇵 Японская йена',
    'CNY': '🇨🇳 Китайский юань'
}

# Хранилище для данных пользователей
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
                logger.info(f"Успешно получен курс: {rate}")
                return rate
            else:
                logger.error(f"Ошибка API: {data.get('error-type')}")
                return None
        else:
            logger.error(f"HTTP ошибка: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Ошибка запроса: {e}")
        return None


def ask_ai(question, user_context=None):
    """Спрашивает AI о валютах и финансах"""
    if not AI_ENABLED:
        return "❌ AI функция недоступна. Добавьте GEMINI_API_KEY в .env файл."

    try:
        # Контекст для AI
        system_prompt = f"""Ты - эксперт по валютам и финансам. 
Отвечай на русском языке кратко и понятно.
Если вопрос о курсах валют, объясни факторы, влияющие на них.
Если вопрос о финансовых советах, дай практические рекомендации.

Доступные валюты для обмена: {', '.join(CURRENCIES.keys())}

Текущая дата: {datetime.now().strftime('%d.%m.%Y')}
"""

        if user_context:
            system_prompt += f"\n\nКонтекст пользователя: {user_context}"

        full_prompt = f"{system_prompt}\n\nВопрос пользователя: {question}"

        logger.info(f"Запрос к AI: {question[:50]}...")

        response = ai_model.generate_content(full_prompt)
        answer = response.text

        logger.info("AI ответ получен")
        return answer

    except Exception as e:
        logger.error(f"Ошибка AI: {e}")
        return f"❌ Ошибка AI: {str(e)}"


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
    buttons = [
        types.KeyboardButton("💱 Обмен валют"),
        types.KeyboardButton("🤖 Спросить AI"),
        types.KeyboardButton("📊 Курсы валют"),
        types.KeyboardButton("ℹ️ Помощь")
    ]
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start"""
    user_name = message.from_user.first_name

    ai_status = "✅ включен" if AI_ENABLED else "❌ выключен"

    welcome_text = f"""
👋 Привет, {user_name}!

Я умный бот для обмена валют 💱

<b>Что я умею:</b>
💱 Конвертировать валюты
📊 Показывать актуальные курсы
🤖 Отвечать на вопросы об экономике (AI {ai_status})
💡 Давать финансовые советы

Используй кнопки ниже или команды:
/help - помощь
/exchange - обмен валют
/rates - курсы валют
/ask - спросить AI
"""

    logger.info(f"Пользователь {message.from_user.id} ({user_name}) запустил бота")

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='HTML',
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help"""
    ai_status = "доступна" if AI_ENABLED else "недоступна"

    help_text = f"""
📖 <b>Доступные команды:</b>

/start - Начать работу
/help - Это сообщение
/exchange - Обменять валюту
/rates - Посмотреть курсы
/ask - Спросить AI ({ai_status})

💱 <b>Обмен валют:</b>
1. Выбери исходную валюту
2. Выбери целевую валюту
3. Введи сумму

🤖 <b>AI помощник:</b>
Задавай любые вопросы о валютах, экономике и финансах!

Примеры вопросов:
• Почему растет доллар?
• Стоит ли сейчас покупать евро?
• Что влияет на курс гривны?
• Какую валюту выбрать для сбережений?

<b>Поддерживаемые валюты:</b>
🇺🇸 USD  🇪🇺 EUR  🇺🇦 UAH  🇮🇱 ILS
🇵🇱 PLN  🇷🇺 RUB  🇯🇵 JPY  🇨🇳 CNY
"""

    logger.info(f"Пользователь {message.from_user.id} запросил помощь")

    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='HTML',
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['rates'])
def show_rates(message):
    """Показывает основные курсы валют"""
    user_id = message.chat.id

    bot.send_message(user_id, "⏳ Загружаю курсы валют...")

    try:
        # Получаем курсы относительно USD
        base_currency = 'USD'
        url = f"{BASE_URL}/{EXCHANGE_API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            rates = data['conversion_rates']

            rates_text = f"""
📊 <b>Актуальные курсы валют</b>

<b>Базовая валюта: 1 USD</b>

🇪🇺 EUR: {rates.get('EUR', 'N/A'):.4f}
🇺🇦 UAH: {rates.get('UAH', 'N/A'):.4f}
🇮🇱 ILS: {rates.get('ILS', 'N/A'):.4f}
🇵🇱 PLN: {rates.get('PLN', 'N/A'):.4f}
🇷🇺 RUB: {rates.get('RUB', 'N/A'):.4f}
🇯🇵 JPY: {rates.get('JPY', 'N/A'):.4f}
🇨🇳 CNY: {rates.get('CNY', 'N/A'):.4f}

<i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}</i>
"""

            bot.send_message(
                user_id,
                rates_text,
                parse_mode='HTML',
                reply_markup=create_main_keyboard()
            )

            logger.info(f"Пользователь {user_id} запросил курсы валют")
        else:
            bot.send_message(
                user_id,
                "❌ Не удалось получить курсы. Попробуйте позже.",
                reply_markup=create_main_keyboard()
            )
    except Exception as e:
        logger.error(f"Ошибка при получении курсов: {e}")
        bot.send_message(
            user_id,
            "❌ Произошла ошибка. Попробуйте позже.",
            reply_markup=create_main_keyboard()
        )


@bot.message_handler(commands=['ask'])
def start_ai_chat(message):
    """Начало диалога с AI"""
    user_id = message.chat.id

    if not AI_ENABLED:
        bot.send_message(
            user_id,
            "❌ AI функция недоступна.\n\nДля активации:\n1. Получите API ключ на https://aistudio.google.com/apikey\n2. Добавьте в .env: GEMINI_API_KEY=ваш_ключ",
            reply_markup=create_main_keyboard()
        )
        return

    user_data[user_id] = {'step': 'ai_chat'}

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Завершить диалог"))

    bot.send_message(
        user_id,
        "🤖 <b>AI Помощник активирован</b>\n\nЗадавай любые вопросы о валютах, экономике и финансах!\n\nПримеры:\n• Почему растет доллар?\n• Стоит ли покупать евро?\n• Что влияет на курс валют?",
        parse_mode='HTML',
        reply_markup=markup
    )

    logger.info(f"Пользователь {user_id} начал диалог с AI")


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


@bot.message_handler(func=lambda message: message.text == "🤖 Спросить AI")
def ai_button(message):
    """Обработчик кнопки 'Спросить AI'"""
    start_ai_chat(message)


@bot.message_handler(func=lambda message: message.text == "📊 Курсы валют")
def rates_button(message):
    """Обработчик кнопки 'Курсы валют'"""
    show_rates(message)


@bot.message_handler(func=lambda message: message.text == "ℹ️ Помощь")
def help_button(message):
    """Обработчик кнопки 'Помощь'"""
    send_help(message)


@bot.message_handler(func=lambda message: message.text in ["❌ Отмена", "❌ Завершить диалог"])
def cancel_operation(message):
    """Отмена текущей операции"""
    user_id = message.chat.id

    if user_id in user_data:
        del user_data[user_id]
        logger.info(f"Пользователь {user_id} отменил операцию")

    bot.send_message(
        user_id,
        "✅ Операция завершена",
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработчик всех текстовых сообщений"""
    user_id = message.chat.id
    text = message.text

    # Если пользователь в режиме AI чата
    if user_id in user_data and user_data[user_id].get('step') == 'ai_chat':
        if not AI_ENABLED:
            bot.send_message(user_id, "❌ AI недоступен")
            return

        # Отправляем "печатает..."
        bot.send_chat_action(user_id, 'typing')

        logger.info(f"Пользователь {user_id} спросил AI: {text[:50]}...")

        # Получаем ответ от AI
        answer = ask_ai(text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("❌ Завершить диалог"))

        bot.send_message(
            user_id,
            f"🤖 <b>AI Ответ:</b>\n\n{answer}",
            parse_mode='HTML',
            reply_markup=markup
        )
        return

    # Если пользователь не в процессе обмена
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

            logger.info(f"Пользователь {user_id} выбрал: {currency_code}")

            bot.send_message(
                user_id,
                f"✅ {CURRENCIES[currency_code]}\n\nТеперь выберите валюту для получения:",
                reply_markup=create_currency_keyboard()
            )
        else:
            bot.send_message(
                user_id,
                "❌ Выберите валюту из списка",
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
                    "❌ Выберите другую валюту",
                    reply_markup=create_currency_keyboard()
                )
                return

            user_data[user_id]['to_currency'] = currency_code
            user_data[user_id]['step'] = 'amount'

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("❌ Отмена"))

            bot.send_message(
                user_id,
                f"✅ {CURRENCIES[currency_code]}\n\nВведите сумму:",
                reply_markup=markup
            )
        else:
            bot.send_message(
                user_id,
                "❌ Выберите валюту из списка",
                reply_markup=create_currency_keyboard()
            )

    # Шаг 3: Расчет
    elif step == 'amount':
        try:
            amount = float(text.replace(',', '.'))

            if amount <= 0:
                bot.send_message(user_id, "❌ Сумма должна быть больше 0")
                return

            from_curr = user_data[user_id]['from_currency']
            to_curr = user_data[user_id]['to_currency']

            bot.send_message(user_id, "⏳ Получаю курс...")

            rate = get_exchange_rate(from_curr, to_curr)

            if rate:
                result = amount * rate

                result_text = f"""
💱 <b>Результат обмена</b>

<b>Из:</b> {amount:.2f} {from_curr}
<b>В:</b> {result:.2f} {to_curr}

<b>Курс:</b> 1 {from_curr} = {rate:.4f} {to_curr}

<i>{datetime.now().strftime('%d.%m.%Y %H:%M')}</i>
"""

                bot.send_message(
                    user_id,
                    result_text,
                    parse_mode='HTML',
                    reply_markup=create_main_keyboard()
                )

                logger.info(f"Обмен выполнен: {amount} {from_curr} -> {result:.2f} {to_curr}")
            else:
                bot.send_message(
                    user_id,
                    "❌ Не удалось получить курс",
                    reply_markup=create_main_keyboard()
                )

            del user_data[user_id]

        except ValueError:
            bot.send_message(user_id, "❌ Введите число (например: 100)")


# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен и готов к работе")
    print("🤖 Бот запущен...")
    if AI_ENABLED:
        print("✅ AI функция активна")
    else:
        print("⚠️  AI функция отключена")

    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise