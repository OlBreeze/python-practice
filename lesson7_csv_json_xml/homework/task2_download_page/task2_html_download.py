# #Завдання 2: Робота з зовнішніми пакетами
# Встанови пакет requests за допомогою pip. (bash:  pip install requests)
# Напиши скрипт, який завантажує сторінку з вказаного URL та зберігає її вміст у текстовий файл.
# Додай обробку помилок на випадок, якщо сторінка недоступна.

import requests


def download_page(url: str, filename: str) -> None:
    """
    Завантажує HTML-сторінку за вказаним URL і зберігає її у файл.

    :param url: Адреса сторінки для завантаження
    :param filename: Ім'я файлу для збереження вмісту
    """
    try:
        response = requests.get(url, timeout=10)  # таймаут 10 секунд
        response.raise_for_status()  # помилка, якщо статус-код не 200
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Сторінку збережено у файл: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Помилка при завантаженні сторінки: {e}")


if __name__ == "__main__":
    url = "https://olbreeze.github.io/CatchChicken/"
    download_page(url, "page.html")
