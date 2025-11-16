# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Головна сторінка = форма логіну
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('welcome/', views.welcome_view, name='welcome'),
    path('logout/', views.logout_view, name='logout'),

    # Оптимізація запитів
    path('books/unoptimized/', views.books_list_unoptimized, name='books_unoptimized'),
    path('books/optimized/', views.books_list_optimized, name='books_optimized'),
    path('books/cached/', views.books_list_cached, name='books_cached'),

    # Статистика та аналітика
    path('statistics/', views.authors_statistics, name='statistics'),
    path('popular-authors/', views.authors_with_popular_books, name='popular_authors'),
    path('import/', views.start_import, name='import_books'),
    path('task/<str:task_id>/', views.task_status, name='task_status'),
]
