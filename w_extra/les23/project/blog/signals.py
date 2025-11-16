from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Article, Comment, CustomUser, Tag
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    """
    Дії після збереження статті:
    - Відправка email при публікації
    - Логування створення/оновлення
    """
    if created:
        logger.info(f"Створено нову статтю: {instance.title} (ID: {instance.id})")

        # Ініціалізація метаданих
        if not instance.metadata:
            instance.metadata = {
                'created_by': instance.author.username,
                'version': 1
            }
            Article.objects.filter(id=instance.id).update(metadata=instance.metadata)

    else:
        logger.info(f"Оновлено статтю: {instance.title} (ID: {instance.id})")

        # Збільшення версії
        if instance.metadata:
            instance.metadata['version'] = instance.metadata.get('version', 1) + 1
            Article.objects.filter(id=instance.id).update(metadata=instance.metadata)

    # Відправка email при публікації
    if instance.status == 'published' and created:
        try:
            send_mail(
                subject=f'Нова стаття опублікована: {instance.title}',
                message=f'Автор {instance.author.username} опублікував нову статтю.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
            logger.info(f"Email відправлено для статті: {instance.title}")
        except Exception as e:
            logger.error(f"Помилка відправки email: {e}")


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, **kwargs):
    """
    Дії перед збереженням статті:
    - Автоматична генерація slug
    - Валідація даних
    """
    # Автоматична генерація slug якщо не вказано
    if not instance.slug:
        instance.slug = slugify(instance.title)

        # Перевірка унікальності slug
        original_slug = instance.slug
        counter = 1
        while Article.objects.filter(slug=instance.slug).exclude(id=instance.id).exists():
            instance.slug = f"{original_slug}-{counter}"
            counter += 1

    # Очищення контенту від небезпечних тегів (базова санітизація)
    if instance.content:
        # Тут можна додати більш складну логіку очищення
        pass


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    """
    Дії після збереження коментаря:
    - Відправка сповіщення автору статті
    - Логування
    """
    if created:
        logger.info(
            f"Новий коментар від {instance.author.username} "
            f"до статті '{instance.article.title}'"
        )

        # Сповіщення автора статті
        if instance.article.author != instance.author:
            try:
                send_mail(
                    subject=f'Новий коментар до вашої статті: {instance.article.title}',
                    message=(
                        f'{instance.author.username} залишив коментар:\n\n'
                        f'{instance.content}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.article.author.email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.error(f"Помилка відправки email: {e}")


@receiver(post_delete, sender=Article)
def article_post_delete(sender, instance, **kwargs):
    """Логування видалення статті"""
    logger.warning(
        f"Видалено статтю: {instance.title} (ID: {instance.id}) "
        f"автора {instance.author.username}"
    )


@receiver(m2m_changed, sender=Article.tags.through)
def article_tags_changed(sender, instance, action, **kwargs):
    """
    Відстеження змін тегів статті
    """
    if action in ['post_add', 'post_remove', 'post_clear']:
        tag_names = ', '.join([tag.name for tag in instance.tags.all()])
        logger.info(
            f"Теги статті '{instance.title}' змінено. "
            f"Поточні теги: {tag_names}"
        )


@receiver(post_save, sender=CustomUser)
def user_post_save(sender, instance, created, **kwargs):
    """
    Дії після реєстрації користувача:
    - Відправка вітального email
    - Логування
    """
    if created:
        logger.info(f"Зареєстровано нового користувача: {instance.username}")

        try:
            send_mail(
                subject='Ласкаво просимо до нашого блогу!',
                message=(
                    f'Привіт, {instance.username}!\n\n'
                    f'Дякуємо за реєстрацію в нашому блозі.'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        except Exception as e:
            logger.error(f"Помилка відправки вітального email: {e}")
