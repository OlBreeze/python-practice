# Задача 4: створення веб-сервера, що обслуговує кілька клієнтів одночасно
# Напишіть простий веб-сервер, який може обслуговувати кілька
# клієнтів одночасно, використовуючи потоки або процеси.
# Ваша програма повинна відповідати на HTTP-запити клієнтів
# і відправляти їм текстові повідомлення.
#
# Підказка: можна використовувати вбудовану бібліотеку http.server.

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from typing import Tuple


class SimpleRequestHandler(BaseHTTPRequestHandler):
    """
    Клас-обробник HTTP-запитів.
    Відповідає на GET-запити простим текстовим повідомленням.
    """

    def do_GET(self) -> None:
        """
        Обробляє GET-запит від клієнта.
        """
        message = f"Привіт! Ви звернулись до сервера за адресою: {self.path}\n"
        self.send_response(200)  # HTTP статус OK
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        # Отправляет тело ответа (сам текст) клиенту (байты, а не строку)
        self.wfile.write(message.encode("utf-8"))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    HTTP-сервер, який обробляє кожен запит у окремому потоці.
    Це дозволяє обслуговувати кількох клієнтів одночасно.
    """
    daemon_threads = True  # Автоматично знищує потоки після завершення


def run_server(server_address: Tuple[str, int]) -> None:
    """
    Запускає сервер на вказаній адресі.

    Parameters:
        server_address (Tuple[str, int]): кортеж з IP-адреси та порту.

    Returns:
        None
    """
    httpd = ThreadedHTTPServer(server_address, SimpleRequestHandler)
    print(f"Сервер запущено на http://{server_address[0]}:{server_address[1]}")
    try:
        # Запускає сервер у нескінченному циклі, поки не буде вручну зупинено.
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер зупинено.")
    finally:
        httpd.server_close()


# --------------------------------------------
if __name__ == "__main__":
    run_server(("localhost", 8080))
