# Використовуючи бібліотеку aiohttp, створіть простий асинхронний веб-сервер,
# який має два маршрути:
#
# /, який повертає простий текст "Hello, World!".
# /slow, який симулює довгу операцію з затримкою в 5 секунд
# і повертає текст "Operation completed".
# Запустіть сервер і перевірте, що він може обробляти
# кілька запитів одночасно (зокрема, маршрут /slow не блокує інші запити).

from aiohttp import web
import asyncio


async def handle_root(request: web.Request) -> web.Response:
    """
    Обробляє GET-запит на маршрут "/".

    :param request: Об'єкт запиту (не використовується у відповіді).
    :return: Відповідь з текстом "Hello, World!".
    """
    return web.Response(text="Hello, World!")


async def handle_slow(request: web.Request) -> web.Response:
    """
    Обробляє GET-запит на маршрут "/slow", імітуючи тривалу операцію.

    :param request: Об'єкт запиту.
    :return: Відповідь з текстом "Operation completed" через 5 секунд.
    """
    await asyncio.sleep(5)  # Асинхронна пауза — не блокує інші запити
    return web.Response(text="Operation completed")


async def init_app() -> web.Application:
    """
    Ініціалізує та повертає aiohttp-додаток із налаштованими маршрутами.

    :return: Об'єкт веб-додатку aiohttp.
    """
    app: web.Application = web.Application()
    app.router.add_get("/", handle_root)
    app.router.add_get("/slow", handle_slow)
    return app


def main() -> None:
    """
    Запускає веб-сервер на локальному хості (127.0.0.1) і порту 8080.
    """
    web.run_app(init_app(), host="127.0.0.1", port=8080)


# -------------------------------------------------------------
if __name__ == "__main__":
    main()
#
# curl http://127.0.0.1:8080/       # миттєва відповідь
# curl http://127.0.0.1:8080/slow   # відповідь через 5 секунд
