from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """
    Головна сторінка додатку.

    Аргументи:
        request: HTTP-запит від клієнта

    Повертає:
        HttpResponse: відрендерений шаблон home.html
    """
    # return HttpResponse("<html><body>Hello HOME</body></html>")
    return render(request, 'home/home.html')


def home_page(request: HttpRequest) -> HttpResponse:
    """
    Домашня сторінка з привітанням.

    Аргументи:
        request: HTTP-запит від клієнта

    Повертає:
        HttpResponse: відрендерений шаблон home.html
    """
    return render(request, 'home/home.html')


def about_page(request: HttpRequest) -> HttpResponse:
    """
    Сторінка "Про нас" з інформацією про проект.

    Аргументи:
        request: HTTP-запит від клієнта

    Повертає:
        HttpResponse: відрендерений шаблон about.html
    """
    return render(request, 'home/about.html')


def contact_page(request: HttpRequest) -> HttpResponse:
    """
    Сторінка контактів для зв'язку з користувачами.

    Аргументи:
        request: HTTP-запит від клієнта

    Повертає:
        HttpResponse: відрендерений шаблон contact.html
    """
    return render(request, 'home/contact.html')


def post_view(request: HttpRequest, id: str) -> HttpResponse:
    """
    Відображення конкретного поста за його ID.

    Аргументи:
        request: HTTP-запит від клієнта
        id: ідентифікатор поста (рядок з цифр)

    Повертає:
        HttpResponse: відрендерений шаблон post.html з ID поста

    Приклад:
        URL: /post/123/ виведе "Ви переглядаєте пост з ID: 123"
    """
    context = {'post_id': id}
    return render(request, 'home/post.html', context)


def profile_view(request: HttpRequest, username: str) -> HttpResponse:
    """
    Відображення профілю користувача за іменем.

    Аргументи:
        request: HTTP-запит від клієнта
        username: ім'я користувача (тільки літери)

    Повертає:
        HttpResponse: відрендерений шаблон profile.html з іменем користувача

    Приклад:
        URL: /profile/john/ виведе "Ви переглядаєте профіль користувача: john"
    """
    context = {'username': username}
    return render(request, 'home/profile.html', context)


def event_view(request: HttpRequest, year: str, month: str, day: str) -> HttpResponse:
    """
    Відображення сторінки події з конкретною датою.

    Аргументи:
        request: HTTP-запит від клієнта
        year: рік події (4 цифри)
        month: місяць події (2 цифри)
        day: день події (2 цифри)

    Повертає:
        HttpResponse: відрендерений шаблон event.html з датою події

    Приклад:
        URL: /event/2024/12/25/ виведе "Дата події: 2024-12-25"
    """
    context = {
        'year': year,
        'month': month,
        'day': day,
        'full_date': f"{year}-{month}-{day}"
    }
    return render(request, 'home/event.html', context)
