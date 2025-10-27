"""
Сигнали для застосунку дошки оголошень.

Цей модуль містить обробники сигналів для автоматичного надсилання
електронних листів та деактивації оголошень.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Ad, UserProfile
from django.contrib.auth.models import User


#    **Що відбувається:**
#     1. `@receiver` - декоратор, який "підписує" функцію на сигнал
#     2. `post_save` - сигнал "після збереження"
#     3. `sender=User` - реагуємо на збереження User
#     4. `created=True` - тільки якщо користувач НОВИЙ
#     5. → Створюємо профіль автоматично!
@receiver(post_save, sender=User)
def create_user_profile(sender: type[User], instance: User, created: bool, **kwargs) -> None:
    """
    Автоматично створює профіль користувача при реєстрації.

    Args:
        sender: Клас моделі, що викликала сигнал
        instance: Екземпляр користувача
        created: Чи був створений новий користувач
        **kwargs: Додаткові аргументи
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender: type[User], instance: User, **kwargs) -> None:
    """
    Автоматично зберігає профіль користувача при збереженні User.

    Args:
        sender: Клас моделі, що викликала сигнал
        instance: Екземпляр користувача
        **kwargs: Додаткові аргументи
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


# **Що відбувається:**
# 1. Коли створюється нове оголошення (`Ad`)
# 2. Автоматично надсилається email користувачу
# 3. Без додаткового коду у views!
@receiver(post_save, sender=Ad)
def send_ad_created_email(sender: type[Ad], instance: Ad, created: bool, **kwargs) -> None:
    """
    Надсилає електронний лист користувачу при створенні нового оголошення.

    Args:
        sender: Клас моделі, що викликала сигнал
        instance: Екземпляр оголошення
        created: Чи було створено нове оголошення
        **kwargs: Додаткові аргументи
    """
    if created and instance.user.email:
        subject = f'Ваше оголошення "{instance.title}" створено'
        message = f"""
        Вітаємо, {instance.user.username}!

        Ваше оголошення "{instance.title}" успішно створено.
        Категорія: {instance.category.name}
        Ціна: {instance.price} грн

        Оголошення буде активним протягом 30 днів.

        Дякуємо за використання нашого сервісу!
        """

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.user.email],
                fail_silently=True,
            )
        except Exception as e:
            # Логуємо помилку, але не зупиняємо виконання
            print(f"Помилка надсилання email: {e}")


# @receiver(post_save, sender=Ad)
# def schedule_ad_deactivation(sender: type[Ad], instance: Ad, created: bool, **kwargs) -> None:
#     """
#     НОВИЙ СИГНАЛ: Автоматично деактивує оголошення через 30 днів після створення.
#
#     Цей сигнал перевіряє чи оголошення старше 30 днів при кожному збереженні
#     та деактивує його якщо потрібно.
#
#     Args:
#         sender: Клас моделі, що викликала сигнал
#         instance: Екземпляр оголошення
#         created: Чи було створено нове оголошення
#         **kwargs: Додаткові аргументи
#     """
#     # Перевіряємо тільки активні оголошення
#     if instance.is_active:
#         expiration_date = instance.created_at + timedelta(days=30)
#
#         # Якщо пройшло 30 днів - деактивуємо
#         if timezone.now() >= expiration_date:
#             # Використовуємо update() щоб уникнути рекурсивного виклику post_save
#             Ad.objects.filter(id=instance.id).update(is_active=False)
#
#             # Надсилаємо email про деактивацію
#             if instance.user.email:
#                 subject = f'Ваше оголошення "{instance.title}" деактивовано'
#                 message = f"""
#                 Вітаємо, {instance.user.username}!
#
#                 Ваше оголошення "{instance.title}" було автоматично деактивовано,
#                 оскільки минуло 30 днів з моменту його створення.
#
#                 Ви можете активувати його знову через адмін-панель або створити нове.
#
#                 Дякуємо за використання нашого сервісу!
#                 """
#
#                 try:
#                     send_mail(
#                         subject=subject,
#                         message=message,
#                         from_email=settings.DEFAULT_FROM_EMAIL,
#                         recipient_list=[instance.user.email],
#                         fail_silently=True,
#                     )
#                 except Exception as e:
#                     print(f"Помилка надсилання email про деактивацію: {e}")