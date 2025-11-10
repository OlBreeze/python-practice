# Лекция: Web Scraping с Beautiful Soup

## 1. Введение в Web Scraping

### 1.1 Что такое Web Scraping?

**Web Scraping (парсинг веб-страниц)** — это автоматизированный процесс извлечения данных с веб-сайтов.

```
┌─────────────┐
│  Веб-сайт   │
│   (HTML)    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Парсер     │
│ (Beautiful  │
│   Soup)     │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│ Структури-  │
│ рованные    │
│   данные    │
└─────────────┘
```

### 1.2 Для чего используется?

#### 📊 Сбор данных для анализа
- Мониторинг цен конкурентов
- Анализ рынка
- Исследование трендов

#### 📰 Агрегация контента
- Новостные агрегаторы
- Сбор вакансий с разных сайтов
- Мониторинг объявлений

#### 🔍 SEO и маркетинг
- Анализ ключевых слов
- Мониторинг упоминаний бренда
- Сбор контактов

#### 📈 Финансы
- Сбор котировок акций
- Мониторинг криптовалют
- Анализ финансовых показателей

#### 🎓 Научные исследования
- Сбор данных для исследований
- Создание датасетов для ML
- Мониторинг публикаций

### 1.3 Beautiful Soup — что это?

**Beautiful Soup** — Python библиотека для парсинга HTML и XML документов.

**Преимущества:**
- ✅ Простой и понятный синтаксис
- ✅ Автоматическое исправление невалидного HTML
- ✅ Мощные инструменты поиска
- ✅ Поддержка различных парсеров
- ✅ Хорошая документация

**Альтернативы:**
- `lxml` — быстрее, но сложнее
- `Scrapy` — фреймворк для больших проектов
- `Selenium` — для динамических сайтов (JavaScript)

---

## 2. Основы HTML

### 2.1 Структура HTML документа

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Заголовок страницы</title>
</head>
<body>
    <header>
        <h1>Главный заголовок</h1>
        <nav>
            <a href="/about">О нас</a>
            <a href="/contact">Контакты</a>
        </nav>
    </header>
    
    <main>
        <article class="post">
            <h2 id="post-title">Название статьи</h2>
            <p class="description">Краткое описание</p>
            <div class="content">
                <p>Текст статьи...</p>
            </div>
        </article>
    </main>
    
    <footer>
        <p>&copy; 2024 Мой сайт</p>
    </footer>
</body>
</html>
```

### 2.2 Ключевые элементы HTML

#### Теги
**Тег** — основной строительный блок HTML.

```html
<!-- Открывающий и закрывающий теги -->
<p>Это параграф</p>

<!-- Самозакрывающийся тег -->
<img src="image.jpg" />

<!-- Вложенные теги -->
<div>
    <p>Текст внутри div</p>
</div>
```

#### Атрибуты
**Атрибуты** — дополнительная информация об элементе.

```html
<!-- Атрибуты элемента -->
<a href="https://example.com" 
   class="link" 
   id="main-link" 
   target="_blank">
   Ссылка
</a>

<!-- Популярные атрибуты -->
id        <!-- Уникальный идентификатор -->
class     <!-- CSS класс (может быть несколько) -->
href      <!-- URL для ссылок -->
src       <!-- Источник для изображений/скриптов -->
alt       <!-- Альтернативный текст -->
title     <!-- Всплывающая подсказка -->
data-*    <!-- Кастомные атрибуты -->
```

#### Классы и ID

```html
<!-- ID - уникальный идентификатор -->
<div id="header">Шапка сайта</div>

<!-- Class - может повторяться -->
<p class="text">Первый параграф</p>
<p class="text highlight">Второй параграф</p>
<p class="text">Третий параграф</p>

<!-- Несколько классов -->
<button class="btn btn-primary btn-large">Кнопка</button>
```

### 2.3 Часто используемые теги

```html
<!-- Заголовки (h1 - самый важный, h6 - наименее важный) -->
<h1>Главный заголовок</h1>
<h2>Подзаголовок</h2>

<!-- Параграфы и текст -->
<p>Обычный текст</p>
<strong>Жирный текст</strong>
<em>Курсивный текст</em>
<span>Инлайн элемент</span>

<!-- Ссылки -->
<a href="https://example.com">Ссылка</a>

<!-- Изображения -->
<img src="photo.jpg" alt="Описание">

<!-- Списки -->
<ul>  <!-- Маркированный список -->
    <li>Пункт 1</li>
    <li>Пункт 2</li>
</ul>

<ol>  <!-- Нумерованный список -->
    <li>Первый</li>
    <li>Второй</li>
</ol>

<!-- Таблицы -->
<table>
    <thead>
        <tr>
            <th>Заголовок 1</th>
            <th>Заголовок 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Ячейка 1</td>
            <td>Ячейка 2</td>
        </tr>
    </tbody>
</table>

<!-- Блочные контейнеры -->
<div>Блочный элемент</div>
<section>Секция</section>
<article>Статья</article>
<header>Шапка</header>
<footer>Подвал</footer>
<nav>Навигация</nav>
```

### 2.4 Инструменты для инспекции HTML

#### Chrome DevTools

```
1. Открыть DevTools:
   - Windows/Linux: F12 или Ctrl+Shift+I
   - Mac: Cmd+Option+I

2. Вкладка Elements:
   - Просмотр HTML структуры
   - Выделение элементов на странице
   - Редактирование HTML в реальном времени

3. Инструмент выбора элемента:
   - Иконка курсора в углу
   - Наведение на элементы страницы
   - Автоматический переход к коду
```

#### Полезные возможности

```html
<!-- Копирование селектора -->
Правый клик на элементе → Copy → Copy selector

<!-- Копирование XPath -->
Правый клик на элементе → Copy → Copy XPath

<!-- Просмотр вычисленных стилей -->
Вкладка Computed в правой панели
```

---

## 3. Установка и настройка

### 3.1 Установка необходимых пакетов

```bash
# Установка Beautiful Soup
pip install beautifulsoup4

# Установка requests для HTTP запросов
pip install requests

# Установка lxml парсера (рекомендуется)
pip install lxml

# Альтернатива: html5lib (для сложного HTML)
pip install html5lib
```

### 3.2 Импорт библиотек

```python
# Основные импорты
from bs4 import BeautifulSoup
import requests

# Дополнительные (по необходимости)
import json
import csv
import time
from urllib.parse import urljoin
```

### 3.3 Проверка установки

```python
# Проверка версии Beautiful Soup
import bs4
print(f"Beautiful Soup версия: {bs4.__version__}")

# Проверка requests
import requests
print(f"Requests версия: {requests.__version__}")
```

---

## 4. Получение веб-страницы

### 4.1 Базовый запрос

```python
import requests
from bs4 import BeautifulSoup

# URL страницы
url = "https://example.com"

# Отправка GET запроса
response = requests.get(url)

# Проверка статуса
if response.status_code == 200:
    print("✅ Страница успешно загружена")
    html_content = response.text
else:
    print(f"❌ Ошибка: {response.status_code}")
```

### 4.2 Обработка ошибок

```python
import requests
from bs4 import BeautifulSoup

def get_page(url):
    """Безопасное получение страницы"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Вызовет исключение для 4xx/5xx
        return response.text
    except requests.exceptions.Timeout:
        print("⏱️ Превышено время ожидания")
    except requests.exceptions.ConnectionError:
        print("🔌 Ошибка соединения")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP ошибка: {e}")
    except Exception as e:
        print(f"⚠️ Неизвестная ошибка: {e}")
    return None

# Использование
html = get_page("https://example.com")
if html:
    soup = BeautifulSoup(html, 'lxml')
```

### 4.3 Заголовки запроса

```python
# Добавление User-Agent (важно!)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)

# Дополнительные заголовки
headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    'Referer': 'https://google.com'
}
```

### 4.4 Создание объекта BeautifulSoup

```python
from bs4 import BeautifulSoup

# HTML код
html_doc = """
<html>
<head><title>Тестовая страница</title></head>
<body>
    <p class="title"><b>Заголовок</b></p>
    <p class="story">Текст истории...</p>
</body>
</html>
"""

# Создание объекта BeautifulSoup
soup = BeautifulSoup(html_doc, 'lxml')

# Альтернативные парсеры:
# soup = BeautifulSoup(html_doc, 'html.parser')  # Встроенный
# soup = BeautifulSoup(html_doc, 'html5lib')     # Самый мягкий

# Красивый вывод HTML
print(soup.prettify())
```

---

## 5. Навигация по HTML дереву

### 5.1 Поиск элементов по тегам

```python
from bs4 import BeautifulSoup

html = """
<html>
<body>
    <h1>Главный заголовок</h1>
    <p>Первый параграф</p>
    <p>Второй параграф</p>
    <div>
        <p>Вложенный параграф</p>
    </div>
</body>
</html>
"""

soup = BeautifulSoup(html, 'lxml')

# Найти первый элемент
h1 = soup.find('h1')
print(h1)  # <h1>Главный заголовок</h1>
print(h1.text)  # Главный заголовок

# Найти все элементы
paragraphs = soup.find_all('p')
print(f"Найдено параграфов: {len(paragraphs)}")

for p in paragraphs:
    print(p.text)
```

### 5.2 Поиск по классам

```python
html = """
<div class="container">
    <p class="text">Обычный текст</p>
    <p class="text highlight">Выделенный текст</p>
    <p class="description">Описание</p>
</div>
"""

soup = BeautifulSoup(html, 'lxml')

# Найти по одному классу
text_elements = soup.find_all(class_='text')
print(f"Элементов с классом 'text': {len(text_elements)}")

# Найти по нескольким классам (все должны совпадать)
highlighted = soup.find_all(class_='text highlight')

# Альтернативный синтаксис
text_elements = soup.find_all('p', class_='text')

# Найти элементы с любым из классов
elements = soup.find_all('p', class_=['text', 'description'])
```

### 5.3 Поиск по ID

```python
html = """
<div id="header">Шапка</div>
<div id="content">Контент</div>
<div id="footer">Подвал</div>
"""

soup = BeautifulSoup(html, 'lxml')

# Поиск по ID
header = soup.find(id='header')
print(header.text)  # Шапка

# Альтернатива
header = soup.find('div', id='header')

# ID уникален, поэтому find() достаточно
```

### 5.4 Получение текста и атрибутов

```python
html = """
<a href="https://example.com" class="link" id="main-link" title="Пример">
    Перейти на сайт
</a>
<img src="photo.jpg" alt="Фото" width="800" height="600">
"""

soup = BeautifulSoup(html, 'lxml')

link = soup.find('a')

# Получение текста
print(link.text)  # Перейти на сайт
print(link.get_text())  # Альтернатива

# Получение атрибутов
print(link['href'])  # https://example.com
print(link.get('href'))  # Безопасный способ
print(link.get('data-id', 'Не найден'))  # С значением по умолчанию

# Все атрибуты
print(link.attrs)  
# {'href': 'https://example.com', 'class': ['link'], 'id': 'main-link', 'title': 'Пример'}

# Проверка наличия атрибута
if link.has_attr('href'):
    print("Ссылка имеет href")

# Работа с изображениями
img = soup.find('img')
print(f"Изображение: {img['src']}")
print(f"Размер: {img['width']}x{img['height']}")
```

### 5.5 Навигация по дереву

#### Родители, дети и соседи

```python
html = """
<div id="parent">
    <h1>Заголовок</h1>
    <p id="first">Первый параграф</p>
    <p id="second">Второй параграф</p>
    <ul>
        <li>Элемент 1</li>
        <li>Элемент 2</li>
    </ul>
</div>
"""

soup = BeautifulSoup(html, 'lxml')

# Получение элемента
first_p = soup.find('p', id='first')

# Родитель
parent = first_p.parent
print(f"Родитель: {parent.name}")  # div

# Все родители (до корня)
for parent in first_p.parents:
    print(parent.name)  # div, body, html, [document]

# Дети
div = soup.find('div', id='parent')
children = list(div.children)
print(f"Количество детей: {len(children)}")

# Прямые дети (только теги, без текста)
for child in div.children:
    if child.name:  # Пропускаем текстовые узлы
        print(child.name)

# Все потомки (рекурсивно)
descendants = list(div.descendants)
print(f"Всего потомков: {len(descendants)}")

# Следующий сосед
next_sibling = first_p.next_sibling
while next_sibling and not next_sibling.name:
    next_sibling = next_sibling.next_sibling
print(f"Следующий элемент: {next_sibling.text}")

# Предыдущий сосед
previous = first_p.previous_sibling

# Все следующие соседи
for sibling in first_p.next_siblings:
    if sibling.name:
        print(sibling.name)

# Все предыдущие соседи
for sibling in first_p.previous_siblings:
    if sibling.name:
        print(sibling.name)
```

### 5.6 Продвинутый поиск

```python
# Поиск с несколькими условиями
results = soup.find_all('p', class_='text', id='intro')

# Ограничение количества результатов
first_three = soup.find_all('p', limit=3)

# Рекурсивный поиск (по умолчанию True)
direct_children = soup.find_all('p', recursive=False)

# Поиск по содержимому текста
elements = soup.find_all(string='Искомый текст')

# Поиск по регулярному выражению
import re
elements = soup.find_all(string=re.compile('паттерн'))

# Поиск по функции
def has_href(tag):
    return tag.has_attr('href')

links = soup.find_all(has_href)

# Комбинированный поиск
def custom_filter(tag):
    return (
        tag.name == 'p' and
        tag.has_attr('class') and
        'highlight' in tag['class']
    )

highlighted = soup.find_all(custom_filter)
```

---

## 6. CSS селекторы

### 6.1 Метод select()

**CSS селекторы** — мощный инструмент для поиска элементов.

```python
html = """
<div class="container">
    <h1 id="title">Заголовок</h1>
    <p class="text">Первый параграф</p>
    <p class="text highlight">Второй параграф</p>
    <ul class="list">
        <li>Элемент 1</li>
        <li class="active">Элемент 2</li>
        <li>Элемент 3</li>
    </ul>
    <a href="/page1">Ссылка 1</a>
    <a href="/page2" class="external">Ссылка 2</a>
</div>
"""

soup = BeautifulSoup(html, 'lxml')

# По тегу
paragraphs = soup.select('p')

# По классу
texts = soup.select('.text')

# По ID
title = soup.select('#title')

# Комбинация
highlighted = soup.select('p.text.highlight')

# Потомки
items = soup.select('div.container li')

# Прямые дети
direct_children = soup.select('div.container > p')

# Атрибуты
external_links = soup.select('a[class="external"]')
all_links = soup.select('a[href]')
specific_links = soup.select('a[href="/page1"]')

# Начинается с
starts_with = soup.select('a[href^="/page"]')

# Заканчивается на
ends_with = soup.select('a[href$=".pdf"]')

# Содержит
contains = soup.select('a[href*="page"]')

# Псевдоклассы
first_item = soup.select('li:first-child')
last_item = soup.select('li:last-child')
nth_item = soup.select('li:nth-child(2)')

# Несколько селекторов (ИЛИ)
elements = soup.select('p, li, a')
```

### 6.2 Примеры сложных селекторов

```python
# Пример сложной структуры
html = """
<article class="post" data-id="123">
    <header>
        <h2 class="post-title">Название статьи</h2>
        <div class="meta">
            <span class="author">Автор: Иван</span>
            <span class="date">2024-01-15</span>
        </div>
    </header>
    <div class="content">
        <p>Текст статьи...</p>
        <a href="/read-more" class="btn">Читать далее</a>
    </div>
</article>
"""

soup = BeautifulSoup(html, 'lxml')

# Заголовок статьи
title = soup.select_one('article.post h2.post-title').text

# Автор (вложенный поиск)
author = soup.select_one('.meta .author').text

# Кнопка внутри контента
button = soup.select_one('.content a.btn')['href']

# Атрибут data
post_id = soup.select_one('article[data-id]')['data-id']

# Комбинация условий
link = soup.select_one('article.post .content a[href^="/"]')
```

---

## 7. Практические примеры

### 7.1 Парсинг новостного сайта

```python
import requests
from bs4 import BeautifulSoup

def parse_news():
    """Парсинг заголовков новостей"""
    url = "https://example-news.com"
    
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Поиск статей
        articles = soup.find_all('article', class_='news-item')
        
        news_list = []
        for article in articles:
            # Заголовок
            title = article.find('h2', class_='title')
            title_text = title.text.strip() if title else "Без заголовка"
            
            # Ссылка
            link = article.find('a', class_='read-more')
            link_href = link['href'] if link else None
            
            # Дата
            date = article.find('span', class_='date')
            date_text = date.text.strip() if date else None
            
            # Описание
            desc = article.find('p', class_='description')
            desc_text = desc.text.strip() if desc else None
            
            news_list.append({
                'title': title_text,
                'link': link_href,
                'date': date_text,
                'description': desc_text
            })
        
        return news_list
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

# Использование
news = parse_news()
for item in news:
    print(f"📰 {item['title']}")
    print(f"   {item['date']}")
    print(f"   {item['link']}\n")
```

### 7.2 Парсинг интернет-магазина

```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_products(url):
    """Парсинг товаров из интернет-магазина"""
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })
    
    soup = BeautifulSoup(response.text, 'lxml')
    
    products = []
    
    # Поиск карточек товаров
    items = soup.select('.product-card')
    
    for item in items:
        # Название
        name = item.select_one('.product-name')
        name_text = name.text.strip() if name else None
        
        # Цена
        price = item.select_one('.price')
        price_text = price.text.strip() if price else None
        
        # Преобразование цены в число
        if price_text:
            price_value = float(
                price_text.replace('₽', '')
                          .replace(' ', '')
                          .replace(',', '.')
            )
        else:
            price_value = None
        
        # Изображение
        img = item.select_one('.product-image img')
        img_url = urljoin(url, img['src']) if img else None
        
        # Ссылка на товар
        link = item.select_one('a.product-link')
        product_url = urljoin(url, link['href']) if link else None
        
        # Рейтинг
        rating = item.select_one('.rating')
        rating_value = float(rating['data-rating']) if rating and rating.has_attr('data-rating') else None
        
        # Наличие
        in_stock = item.select_one('.in-stock') is not None
        
        products.append({
            'name': name_text,
            'price': price_value,
            'image': img_url,
            'url': product_url,
            'rating': rating_value,
            'in_stock': in_stock
        })
    
    return products

# Использование
products = parse_products('https://shop.example.com/products')

for product in products:
    print(f"🛍️ {product['name']}")
    print(f"   Цена: {product['price']} ₽")
    print(f"   Рейтинг: {product['rating']}")
    print(f"   {'✅ В наличии' if product['in_stock'] else '❌ Нет в наличии'}\n")
```

### 7.3 Парсинг таблиц

```python
def parse_table(url):
    """Парсинг HTML таблицы"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Найти таблицу
    table = soup.find('table', class_='data-table')
    
    if not table:
        return []
    
    # Заголовки
    headers = []
    thead = table.find('thead')
    if thead:
        for th in thead.find_all('th'):
            headers.append(th.text.strip())
    
    # Данные
    data = []
    tbody = table.find('tbody')
    if tbody:
        for tr in tbody.find_all('tr'):
            row = {}
            cells = tr.find_all('td')
            
            for i, cell in enumerate(cells):
                header = headers[i] if i < len(headers) else f'column_{i}'
                row[header] = cell.text.strip()
            
            data.append(row)
    
    return data

# Использование
table_data = parse_table('https://example.com/table-page')

for row in table_data:
    print(row)
```

### 7.4 Парсинг с пагинацией

```python
import time

def parse_all_pages(base_url):
    """Парсинг нескольких страниц"""
    all_items = []
    page = 1
    
    while True:
        print(f"Парсинг страницы {page}...")
        
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Найти элементы на странице
        items = soup.find_all('div', class_='item')
        
        if not items:
            print("Больше нет страниц")
            break
        
        # Обработка элементов
        for item in items:
            title = item.find('h3')
            if title:
                all_items.append(title.text.strip())
        
        # Проверка наличия следующей страницы
        next_button = soup.find('a', class_='next-page')
        if not next_button:
            break
        
        page += 1
        
        # Задержка между запросами
        time.sleep(1)
    
    return all_items

# Использование
items = parse_all_pages('https://example.com/catalog')
print(f"Всего найдено: {len(items)} элементов")
```

---

## 8. Сохранение данных

### 8.1 Сохранение в CSV

```python
import csv
from bs4 import BeautifulSoup
import requests


def save_to_csv(data, filename='output.csv'):
    """Сохранение данных в CSV"""
    if not data:
        print("Нет данных для сохранения")
        return
    
    # Получаем заголовки из первого элемента
    headers = data[0].keys()
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Данные сохранены в {filename}")


# Пример использования
products = [
    {'name': 'Товар 1', 'price': 1000, 'rating': 4.5},
    {'name': 'Товар 2', 'price': 2000, 'rating': 4.8},
    {'name': 'Товар 3', 'price': 1500, 'rating': 4.2}
]

save_to_csv(products, 'products.csv')
```

**Альтернативный способ с pandas:**

```python
import pandas as pd

def save_to_csv_pandas(data, filename='output.csv'):
    """Сохранение с помощью pandas"""
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Данные сохранены в {filename}")

# Использование
save_to_csv_pandas(products, 'products_pandas.csv')
```

### 8.2 Сохранение в JSON

```python
import json


def save_to_json(data, filename='output.json'):
    """Сохранение данных в JSON"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Данные сохранены в {filename}")


# Пример использования
news_data = [
    {
        'title': 'Новость 1',
        'date': '2024-01-15',
        'link': 'https://example.com/news/1'
    },
    {
        'title': 'Новость 2',
        'date': '2024-01-16',
        'link': 'https://example.com/news/2'
    }
]

save_to_json(news_data, 'news.json')
```

**Чтение из JSON:**

```python
def load_from_json(filename='output.json'):
    """Загрузка данных из JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Использование
loaded_data = load_from_json('news.json')
print(loaded_data)
```

### 8.3 Сохранение в Excel

```python
import pandas as pd


def save_to_excel(data, filename='output.xlsx'):
    """Сохранение данных в Excel"""
    df = pd.DataFrame(data)
    
    # Создание Excel файла с форматированием
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Данные', index=False)
        
        # Получение объектов для форматирования
        workbook = writer.book
        worksheet = writer.sheets['Данные']
        
        # Автоматическая ширина столбцов
        for i, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).apply(len).max(),
                len(col)
            ) + 2
            worksheet.set_column(i, i, max_length)
    
    print(f"✅ Данные сохранены в {filename}")


# Использование
save_to_excel(products, 'products.xlsx')
```

### 8.4 Сохранение в базу данных SQLite

```python
import sqlite3


def save_to_database(data, db_name='scraping.db', table_name='products'):
    """Сохранение данных в SQLite"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Создание таблицы
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            rating REAL,
            url TEXT,
            parsed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Вставка данных
    for item in data:
        cursor.execute(f'''
            INSERT INTO {table_name} (name, price, rating, url)
            VALUES (?, ?, ?, ?)
        ''', (
            item.get('name'),
            item.get('price'),
            item.get('rating'),
            item.get('url')
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Данные сохранены в {db_name}")


# Использование
save_to_database(products)
```

---

## 9. Расширенные возможности

### 9.1 Обработка JavaScript-сайтов

Для сайтов, использующих JavaScript, Beautiful Soup не подходит. Используйте **Selenium**.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Настройка драйвера
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Без GUI
driver = webdriver.Chrome(options=options)

try:
    # Загрузка страницы
    driver.get('https://dynamic-site.com')
    
    # Ожидание загрузки элемента
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'product-card'))
    )
    
    # Получение HTML после выполнения JavaScript
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    # Парсинг как обычно
    products = soup.find_all('div', class_='product-card')
    
finally:
    driver.quit()
```

### 9.2 Работа с формами и аутентификацией

```python
import requests
from bs4 import BeautifulSoup

# Создание сессии
session = requests.Session()

# Авторизация
login_url = 'https://example.com/login'
login_data = {
    'username': 'user@example.com',
    'password': 'password123'
}

response = session.post(login_url, data=login_data)

if response.ok:
    # Теперь можем делать запросы от имени авторизованного пользователя
    protected_page = session.get('https://example.com/profile')
    soup = BeautifulSoup(protected_page.text, 'lxml')
    
    # Парсинг защищенной страницы
    user_data = soup.find('div', class_='user-info')
    print(user_data.text)
```

### 9.3 Обработка AJAX запросов

```python
import requests
import json

# Многие сайты загружают данные через AJAX
# Найдите нужный endpoint в DevTools → Network → XHR

def parse_ajax_data(url, params=None):
    """Парсинг данных из AJAX запроса"""
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',  # Важно для AJAX
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.ok:
        data = response.json()
        return data
    
    return None

# Пример
ajax_url = 'https://example.com/api/products'
params = {'page': 1, 'limit': 20}

products = parse_ajax_data(ajax_url, params)
if products:
    for product in products['items']:
        print(product['name'])
```

### 9.4 Обработка больших объёмов данных

```python
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor


def parse_page(url):
    """Парсинг одной страницы"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Извлечение данных
        items = soup.find_all('div', class_='item')
        return [item.text.strip() for item in items]
    
    except Exception as e:
        print(f"Ошибка на {url}: {e}")
        return []


def parse_multiple_pages(urls, max_workers=5):
    """Параллельный парсинг нескольких страниц"""
    all_results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Запуск параллельных задач
        results = executor.map(parse_page, urls)
        
        # Сбор результатов
        for page_results in results:
            all_results.extend(page_results)
    
    return all_results


# Использование
urls = [f'https://example.com/page/{i}' for i in range(1, 11)]
results = parse_multiple_pages(urls, max_workers=5)

print(f"Собрано {len(results)} элементов")
```

### 9.5 Обработка кодировок

```python
import requests
from bs4 import BeautifulSoup

# Автоматическое определение кодировки
response = requests.get(url)
response.encoding = response.apparent_encoding  # Автоопределение
soup = BeautifulSoup(response.text, 'lxml')

# Явное указание кодировки
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml', from_encoding='windows-1251')

# Обработка ошибок декодирования
try:
    text = element.text
except UnicodeDecodeError:
    text = element.text.encode('utf-8', errors='ignore').decode('utf-8')
```

---

## 10. Этические аспекты Web Scraping

### 10.1 Легальность и robots.txt

**robots.txt** — файл с правилами для парсеров.

```python
import requests
from urllib.robotparser import RobotFileParser

def can_fetch(url):
    """Проверка, разрешён ли парсинг"""
    parser = RobotFileParser()
    robots_url = f"{url.split('/')[0]}//{url.split('/')[2]}/robots.txt"
    parser.set_url(robots_url)
    parser.read()
    
    user_agent = 'MyBot'
    return parser.can_fetch(user_agent, url)

# Проверка
url = 'https://example.com/products'
if can_fetch(url):
    print("✅ Парсинг разрешён")
else:
    print("❌ Парсинг запрещён")
```

**Пример robots.txt:**

```
User-agent: *
Disallow: /admin/
Disallow: /private/
Allow: /public/

Crawl-delay: 10
```

### 10.2 Правила хорошего тона

#### ✅ DO (Делайте)

```python
# 1. Используйте задержки между запросами
import time

for url in urls:
    response = requests.get(url)
    # ... парсинг ...
    time.sleep(1)  # Задержка 1 секунда

# 2. Указывайте User-Agent
headers = {
    'User-Agent': 'MyBot/1.0 (+https://mysite.com/bot-info)'
}

# 3. Обрабатывайте ошибки
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Ошибка: {e}")

# 4. Кешируйте результаты
import hashlib
import pickle

def get_cached_or_fetch(url, cache_dir='cache'):
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = f"{cache_dir}/{cache_key}.pkl"
    
    # Проверка кеша
    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        pass
    
    # Запрос данных
    response = requests.get(url)
    data = response.text
    
    # Сохранение в кеш
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)
    
    return data

# 5. Ограничивайте параллелизм
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=3) as executor:  # Не более 3 потоков
    results = executor.map(parse_page, urls)
```

#### ❌ DON'T (Не делайте)

```python
# ❌ Не делайте слишком частые запросы
for i in range(10000):
    requests.get(url)  # DDoS!

# ❌ Не игнорируйте robots.txt
# Всегда проверяйте robots.txt перед парсингом

# ❌ Не скрывайте своё происхождение
headers = {'User-Agent': 'Mozilla/5.0...'}  # Выдаём себя за браузер

# ❌ Не парсите личные данные без согласия
# Уважайте конфиденциальность пользователей

# ❌ Не перегружайте сервер
# Используйте разумные задержки и ограничения
```

### 10.3 Terms of Service (ToS)

**Всегда проверяйте Terms of Service сайта:**

- 📜 Некоторые сайты явно запрещают парсинг
- ⚖️ Нарушение ToS может иметь юридические последствия
- 🤝 Рассмотрите возможность использования официального API

### 10.4 Лучшие практики

```python
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class EthicalScraper:
    """Этичный парсер с ограничениями"""
    
    def __init__(self, delay_range=(1, 3), max_retries=3):
        self.delay_range = delay_range
        self.session = requests.Session()
        
        # Настройка повторных попыток
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
    
    def get(self, url, **kwargs):
        """GET запрос с задержкой"""
        # Случайная задержка
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)
        
        # Запрос
        headers = kwargs.get('headers', {})
        headers.setdefault('User-Agent', 'EthicalScraper/1.0')
        kwargs['headers'] = headers
        
        try:
            response = self.session.get(url, timeout=10, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None


# Использование
scraper = EthicalScraper(delay_range=(2, 5))

for url in urls:
    response = scraper.get(url)
    if response:
        soup = BeautifulSoup(response.text, 'lxml')
        # ... парсинг ...
```

---

## 11. Отладка и устранение проблем

### 11.1 Частые ошибки

#### 404 Not Found

```python
response = requests.get(url)
if response.status_code == 404:
    print("Страница не найдена")
elif response.status_code == 200:
    # Обработка
    pass
```

#### Элемент не найден

```python
# ❌ Плохо
title = soup.find('h1', class_='title').text  # AttributeError если None

# ✅ Хорошо
title_element = soup.find('h1', class_='title')
title = title_element.text if title_element else "Заголовок не найден"

# ✅ Ещё лучше
title = soup.find('h1', class_='title')
if title:
    print(title.text)
else:
    print("Заголовок не найден")
```

#### Изменение структуры сайта

```python
def safe_parse(soup):
    """Безопасный парсинг с несколькими вариантами"""
    # Попытка 1
    title = soup.find('h1', class_='title')
    if title:
        return title.text
    
    # Попытка 2
    title = soup.find('h2', class_='page-title')
    if title:
        return title.text
    
    # Попытка 3
    title = soup.select_one('#main-title')
    if title:
        return title.text
    
    return "Заголовок не найден"
```

### 11.2 Логирование

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def parse_with_logging(url):
    """Парсинг с логированием"""
    logger.info(f"Начало парсинга: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='item')
        
        logger.info(f"Найдено элементов: {len(items)}")
        return items
    
    except requests.exceptions.Timeout:
        logger.error(f"Таймаут при запросе {url}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP ошибка на {url}: {e}")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка на {url}: {e}")
    
    return []
```

### 11.3 Инструменты для отладки

```python
# Вывод красивого HTML
print(soup.prettify())

# Вывод конкретного элемента
element = soup.find('div', class_='content')
print(element.prettify())

# Проверка наличия атрибута
if element.has_attr('data-id'):
    print(f"ID: {element['data-id']}")

# Получение всех атрибутов
print(element.attrs)

# Путь до элемента
def get_path(element):
    """Получить CSS путь до элемента"""
    path = []
    while element:
        if element.name:
            selector = element.name
            if element.get('id'):
                selector += f"#{element['id']}"
            elif element.get('class'):
                selector += f".{'.'.join(element['class'])}"
            path.insert(0, selector)
        element = element.parent
    return ' > '.join(path)

element = soup.find('div', class_='content')
print(get_path(element))
```

---

## 12. Практическое задание

### Задание 1: Парсинг новостей

Создайте скрипт для парсинга новостного сайта:

```python
"""
Задача:
1. Выберите новостной сайт
2. Извлеките:
   - Заголовки новостей
   - Краткое описание
   - Ссылки на полные статьи
   - Дату публикации
3. Сохраните данные в CSV
4. Выведите статистику: сколько новостей собрано
"""

def parse_news_site():
    # Ваш код здесь
    pass

if __name__ == "__main__":
    news = parse_news_site()
    # Сохранение и вывод
```

### Задание 2: Мониторинг цен

```python
"""
Задача:
1. Выберите интернет-магазин
2. Извлеките информацию о товарах:
   - Название
   - Цена
   - Наличие
   - Рейтинг
3. Сохраните в JSON
4. Реализуйте функцию сравнения цен
"""

def monitor_prices(urls):
    # Ваш код здесь
    pass
```

### Задание 3: Агрегатор вакансий

```python
"""
Задача:
1. Выберите сайт с вакансиями
2. Извлеките:
   - Название вакансии
   - Компания
   - Зарплата
   - Требования
   - Контакты
3. Сохраните в базу данных SQLite
4. Реализуйте поиск по ключевым словам
"""

def scrape_jobs(search_query):
    # Ваш код здесь
    pass
```

---

## 13. Полезные советы и трюки

### 13.1 Работа с динамическим контентом

```python
# Если контент загружается при скролле
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get(url)

# Скролл вниз для загрузки контента
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')
```

### 13.2 Обход блокировок

```python
# Ротация User-Agent
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Mozilla/5.0 (X11; Linux x86_64)...'
]

headers = {
    'User-Agent': random.choice(user_agents)
}

# Использование прокси
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080'
}

response = requests.get(url, headers=headers, proxies=proxies)
```

### 13.3 Извлечение данных из скриптов

```python
import json
import re

# Многие сайты встраивают данные в JavaScript
html = """
<script>
var productData = {
    "name": "Товар",
    "price": 1000,
    "rating": 4.5
};
</script>
"""

soup = BeautifulSoup(html, 'lxml')

# Поиск скрипта
script = soup.find('script', string=re.compile('productData'))
if script:
    # Извлечение JSON
    json_text = re.search(r'var productData = ({.*?});', script.string, re.DOTALL)
    if json_text:
        data = json.loads(json_text.group(1))
        print(data)
```

---

## Ключевые выводы

### Основные концепции

✅ **Beautiful Soup** — библиотека для парсинга HTML/XML  
✅ **requests** — для получения веб-страниц  
✅ **HTML** — структурированный язык разметки  
✅ **Селекторы** — теги, классы, ID, CSS-селекторы  

### Методы поиска

| Метод | Описание | Пример |
|-------|----------|--------|
| `find()` | Первый элемент | `soup.find('div')` |
| `find_all()` | Все элементы | `soup.find_all('p')` |
| `select()` | CSS селектор | `soup.select('.class')` |
| `select_one()` | Первый по CSS | `soup.select_one('#id')` |

### Форматы сохранения

- 📄 **CSV** — для табличных данных
- 📋 **JSON** — для структурированных данных
- 📊 **Excel** — для отчётов
- 🗄️ **SQLite** — для больших объёмов

### Этика

⚠️ **Уважайте robots.txt**  
⚠️ **Используйте задержки**  
⚠️ **Указывайте User-Agent**  
⚠️ **Проверяйте ToS**  
⚠️ **Не перегружайте серверы**  

---

## Полезные ресурсы

📚 **Документация:**
- Beautiful Soup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Requests: https://requests.readthedocs.io/
- Selenium: https://selenium-python.readthedocs.io/

📖 **Библиотеки:**
- `beautifulsoup4` — парсинг HTML/XML
- `requests` — HTTP запросы
- `selenium` — автоматизация браузера
- `scrapy` — фреймворк для парсинга
- `lxml` — быстрый парсер
- `pandas` — обработка данных

🛠️ **Инструменты:**
- Chrome DevTools — инспекция HTML
- Postman — тестирование API
- SelectorGadget — помощь с CSS селекторами

📺 **Практика:**
- Тренируйтесь на простых сайтах
- Изучайте структуру разных сайтов
- Создавайте реальные проекты