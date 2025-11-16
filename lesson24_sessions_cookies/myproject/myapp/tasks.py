from celery import shared_task
from django.core.mail import send_mail
from .models import Book, Author
import csv
import time


@shared_task(bind=True)
def import_books_from_csv(self, file_path):
    try:
        total = 0
        imported = 0

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            total = len(rows)

            for i, row in enumerate(rows):
                self.update_state(
                    state='PROGRESS',
                    meta={'current': i + 1, 'total': total, 'percent': int((i + 1) / total * 100)}
                )

                author, _ = Author.objects.get_or_create(name=row['author'])
                Book.objects.create(
                    title=row['title'],
                    author=author,
                    published_year=int(row['year'])
                )

                imported += 1
                time.sleep(0.1)

        # Email
        send_mail(
            'Імпорт завершено',
            f'Успішно імпортовано {imported} книг з {total}',
            'from@example.com',
            ['to@example.com'],
        )

        return {'status': 'completed', 'imported': imported, 'total': total}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shared_task
def send_notification_email(subject, message, recipient):
    """
    Відправка email повідомлення
    """
    send_mail(
        subject,
        message,
        'from@example.com',
        [recipient],
        fail_silently=False,
    )
    return f'Email sent to {recipient}'
