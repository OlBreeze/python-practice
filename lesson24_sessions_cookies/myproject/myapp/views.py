# myapp/views.py
from django.shortcuts import render, redirect
from django.core.cache import cache
from django.db.models import Count, Avg
from django.db import connection
from .models import Author, Book, Review
import time
from .tasks import import_books_from_csv
from celery.result import AsyncResult
from django.http import JsonResponse


# 1. Управління сесіями та cookies
def login_view(request):
    print("=== LOGIN VIEW CALLED ===")
    print(f"Method: {request.method}")

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        print(f"Name: {name}, Age: {age}")

        # Зберігаємо ім'я в cookies, вік у сесії
        response = redirect('welcome')
        response.set_cookie('user_name', name, max_age=3600)
        request.session['user_age'] = age
        print("Redirecting to welcome...")

        return response

    print("Rendering login.html")
    return render(request, 'login.html')


def welcome_view(request):
    print("=== WELCOME VIEW CALLED ===")
    name = request.COOKIES.get('user_name')
    age = request.session.get('user_age')
    print(f"Cookie name: {name}")
    print(f"Session age: {age}")

    # Якщо немає даних - перенаправляємо на login
    if not name or not age:
        print("No data found, redirecting to login")
        return redirect('login')

    print(f"Rendering welcome with name={name}, age={age}")
    response = render(request, 'welcome.html', {
        'name': name,
        'age': age
    })
    response.set_cookie('user_name', name, max_age=3600)

    return response


def logout_view(request):
    print("=== LOGOUT VIEW CALLED ===")
    response = redirect('login')
    response.delete_cookie('user_name')
    request.session.flush()
    print("Cookies and session cleared, redirecting to login")
    return response


# 2.1. Оптимізація запитів
def books_list_unoptimized(request):
    start_time = time.time()
    books = Book.objects.all()
    for book in books:
        author_name = book.author.name
        reviews_count = book.reviews.count()
    execution_time = time.time() - start_time

    return render(request, 'books_list.html', {
        'books': books,
        'execution_time': execution_time,
        'optimization': 'Без оптимізації'
    })


def books_list_optimized(request):
    start_time = time.time()
    books = Book.objects.select_related('author').prefetch_related('reviews').all()
    execution_time = time.time() - start_time

    return render(request, 'books_list.html', {
        'books': books,
        'execution_time': execution_time,
        'optimization': 'З оптимізацією'
    })


# 2.2. Кешування
def books_list_cached(request):
    cache_key = 'books_list'
    books = cache.get(cache_key)

    if not books:
        books = Book.objects.select_related('author').prefetch_related('reviews').all()
        cache.set(cache_key, books, 300)
        cached = False
    else:
        cached = True

    return render(request, 'books_cached.html', {
        'books': books,
        'cached': cached
    })


# 3.1. Анотації та агрегації
def authors_statistics(request):
    authors = Author.objects.annotate(
        avg_rating=Avg('books__reviews__rating'),
        books_count=Count('books'),
        reviews_count=Count('books__reviews')
    ).order_by('-avg_rating')

    books = Book.objects.annotate(
        reviews_count=Count('reviews'),
        avg_rating=Avg('reviews__rating')
    ).order_by('-reviews_count', '-avg_rating')

    return render(request, 'statistics.html', {
        'authors': authors,
        'books': books
    })


# 3.2. Raw SQL
def authors_with_popular_books(request):
    with connection.cursor() as cursor:
        cursor.execute("""
                       SELECT a.id, a.name, COUNT(DISTINCT b.id) as book_count
                       FROM myapp_author a
                                JOIN myapp_book b ON a.id = b.author_id
                                JOIN myapp_review r ON b.id = r.book_id
                       GROUP BY a.id, a.name
                       HAVING COUNT(r.id) > 10
                       """)
        results = cursor.fetchall()

    authors = [{'id': row[0], 'name': row[1], 'book_count': row[2]} for row in results]

    return render(request, 'popular_authors.html', {'authors': authors})

# - - - Celery - - - -
def start_import(request):
    if request.method == 'POST':
        file_path = 'data/books.csv'  # Путь к CSV
        task = import_books_from_csv.delay(file_path)
        return JsonResponse({'task_id': task.id})

    return render(request, 'import_books.html')


def task_status(request, task_id):
    task = AsyncResult(task_id)

    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Очікування...'}
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'percent': task.info.get('percent', 0),
        }
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}

    return JsonResponse(response)