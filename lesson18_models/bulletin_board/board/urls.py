"""
URL маршрути для застосунку дошки оголошень.
"""

from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # Головна та списки
    path('', views.index, name='index'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),

    # CRUD оголошень
    path('ads/create/', views.ad_create, name='ad_create'),
    path('ads/<int:ad_id>/update/', views.ad_update, name='ad_update'),
    path('ads/<int:ad_id>/delete/', views.ad_delete, name='ad_delete'),

    # Коментарі
    path('ads/<int:ad_id>/comment/', views.comment_create, name='comment_create'),

    # Особистий кабінет
    path('my-ads/', views.my_ads, name='my_ads'),

    # Категорії
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:category_id>/', views.category_detail, name='category_detail'),

    # Статистика
    path('statistics/', views.statistics, name='statistics'),
]