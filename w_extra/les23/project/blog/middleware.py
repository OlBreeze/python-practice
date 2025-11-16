# ========== ЗАВДАННЯ 5: Кастомний Middleware ==========
# blog/middleware.py

import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class CustomHeaderMiddleware(MiddlewareMixin):
    """Middleware, який додає кастомний заголовок до відповідей"""

    def process_response(self, request, response):
        # Додаємо кастомні заголовки
        response['X-Custom-Header'] = 'Django-Blog-App'
        response['X-Powered-By'] = 'Django'
        response['X-Request-ID'] = getattr(request, 'request_id', 'unknown')

        return response


class RequestTimingMiddleware(MiddlewareMixin):
    """Middleware для вимірювання часу обробки запиту"""

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Request-Duration'] = f'{duration:.3f}s'

            # Логування повільних запитів
            if duration > 1.0:
                logger.warning(
                    f'Slow request: {request.path} took {duration:.3f}s'
                )

        return response


class RequestIDMiddleware(MiddlewareMixin):
    """Middleware для генерації унікального ID запиту"""

    def process_request(self, request):
        import uuid
        request.request_id = str(uuid.uuid4())


class CustomSecurityMiddleware(MiddlewareMixin):
    """Middleware для додаткової безпеки"""

    def process_response(self, request, response):
        # Додаємо security заголовки
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'

        return response


class UserActivityMiddleware(MiddlewareMixin):
    """Middleware для відстеження активності користувача"""

    def process_request(self, request):
        if request.user.is_authenticated:
            # Оновлюємо час останньої активності
            from django.utils import timezone
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])

