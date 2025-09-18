"""
ЧАСТИНА 1: СИСТЕМА ВІДПРАВКИ ПОВІДОМЛЕНЬ

 Уяви, що ти розробляєш систему для відправки повідомлень різними каналами:
 через SMS, Email та Push-повідомлення.
 Усі ці канали мають різні інтерфейси для відправки повідомлень, але ти хочеш уніфікувати їх,
 щоб використовувати один універсальний інтерфейс для відправки повідомлень незалежно від каналу
"""
from abc import ABC, abstractmethod
from typing import List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Получает логгер с именем, равным текущему модулю (__name__).


# Інтерфейс MessageSender
class MessageSender(ABC):
    @abstractmethod  # это декоратор из модуля abc, который помечает метод как абстрактный.
    def send_message(self, message: str):
        pass


# Існуючі класи для відправки повідомлень
class SMSService:
    def send_sms(self, phone_number: str, message: str):
        """
        відправлення повідомлення
        """
        print(f"Відправка SMS на {phone_number}: {message}")
        # Симуляція можливої помилки
        if not phone_number.startswith('+'):
            raise ValueError("Неправильний формат номера телефону")


class EmailService:
    def send_email(self, email_address: str, message: str):
        """
        відправлення повідомлення
        """
        print(f"Відправка Email на {email_address}: {message}")
        # Симуляція можливої помилки
        if '@' not in email_address:
            raise ValueError("Неправильний формат email адреси")


class PushService:
    def send_push(self, device_id: str, message: str):
        """
        відправлення повідомлення
        """
        print(f"Відправка Push-повідомлення на пристрій {device_id}: {message}")
        # Симуляція можливої помилки
        if len(device_id) < 5:
            raise ValueError("Неправильний формат ID пристрою")


# Адаптери з обробкою помилок
class SMSAdapter(MessageSender):
    def __init__(self, sms_service: SMSService, phone_number: str):
        self.sms_service = sms_service
        self.phone_number = phone_number

    def send_message(self, message: str):
        """
        відправлення повідомлення
        """
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
        """
        відправлення повідомлення
        """
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
        """
        відправлення повідомлення
        """
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

        print(f"\nРезультат розсилки:")
        print(f"✅ Успішно відправлено: {successful_sends}")
        print(f"❌ Помилок: {failed_sends}")
