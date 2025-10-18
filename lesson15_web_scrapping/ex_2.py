from bs4 import BeautifulSoup
import requests as r

response = r.get('https://sinoptik.ua/')

print(response)

soup = BeautifulSoup(response.text, 'lxml') # pip install lxml

# print(end='\n\n\n')
# print(soup.title)
# print(soup.title.name)
# print(soup.title.text)
# print(soup.title.parent)
# print(soup, end="\n\n")
# print(soup.prettify(), end="\n\n")
# print(soup.find('div'), end="\n\n")

search_tags = soup.find_all("ul")
for element in search_tags:
    print(' '.join(element.text.split()))
#
# Отправляет GET-запрос на сайт погоды sinoptik.ua
# Выводит response - объект ответа (покажет статус типа <Response [200]>)
# Парсит HTML с помощью BeautifulSoup
#
# Закомментированные строки показывают разные способы извлечения данных:
#
# soup.title - тег title целиком
# soup.title.name - имя тега ("title")
# soup.title.text - текст внутри тега
# soup.title.parent - родительский элемент
# soup.prettify() - красиво форматированный HTML
#
# Активная часть:
# pythonsearch_tags = soup.find_all("ul")
# Находит все теги <ul> (ненумерованные списки) на странице.
# python' '.join(element.text.split())
# Извлекает текст, убирает лишние пробелы и переносы строк, склеивает в одну строку.