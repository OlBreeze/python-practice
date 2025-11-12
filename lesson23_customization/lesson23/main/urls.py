from django.urls import path
from main import views  # импорт твоего приложения

urlpatterns = [
    path('main/', views.main_view, name='main'),  # <--- главная страница
]

#
# urlpatterns = [
#     path('', views.main_view, name='main'),
#     path('about/', views.about_view, name='about'),
# ]
