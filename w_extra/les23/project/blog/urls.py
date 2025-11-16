from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Головна сторінка та список статей
    path('', views.ArticleListView.as_view(), name='article_list'),

    # Деталі статті
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),

    # Створення та редагування статей
    path('article/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<slug:slug>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),

    # Статті за тегом
    path('tag/<str:tag_name>/', views.TaggedArticlesView.as_view(), name='tagged_articles'),

    # Пошук
    path('search/', views.SearchView.as_view(), name='search'),

    # Статті автора
    path('author/<str:username>/', views.UserArticlesView.as_view(), name='user_articles'),
]

