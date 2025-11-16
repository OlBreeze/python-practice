# middleware.py
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin


class CacheAnonymousMiddleware(MiddlewareMixin):
    """
    Middleware для кешування сторінок для анонімних користувачів
    """

    def process_request(self, request):
        # Перевіряємо чи користувач анонімний
        if not request.user.is_authenticated:
            # Генеруємо ключ кешу на основі шляху
            cache_key = f'page_cache_{request.path}'

            # Перевіряємо чи є кешована версія
            cached_response = cache.get(cache_key)

            if cached_response:
                return cached_response

        return None

    def process_response(self, request, response):
        # Кешуємо відповідь для анонімних користувачів
        if not request.user.is_authenticated and request.method == 'GET':
            cache_key = f'page_cache_{request.path}'

            # Кешуємо на 5 хвилин
            cache.set(cache_key, response, 300)

        return response


class CheckCookiesMiddleware(MiddlewareMixin):
    """
    Middleware для перевірки cookies
    """

    def process_request(self, request):
        # Перевіряємо чи не склали cookies
        user_name = request.COOKIES.get('user_name')

        if user_name:
            # Якщо cookies існують, автоматично подовжуємо їх
            request._cookies_need_refresh = True

        return None

    def process_response(self, request, response):
        # Автоподовження cookies
        if hasattr(request, '_cookies_need_refresh'):
            user_name = request.COOKIES.get('user_name')
            if user_name:
                response.set_cookie('user_name', user_name, max_age=3600)

        return response