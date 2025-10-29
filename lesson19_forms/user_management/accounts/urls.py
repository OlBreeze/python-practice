from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Реєстрація
    path('register/', views.register_view, name='register'),

    # Список користувачів
    path('users/', views.users_list_view, name='users_list'),

    # Профіль
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),

    # Зміна паролю
    path('password/change/', views.change_password_view, name='change_password'),

    # Вхід та вихід
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.logout_view, name='logout'),

    # Видалення акаунту (додаткова функція)
    path('delete/', views.delete_account_view, name='delete_account'),
]

# `LoginView` и `LogoutView` — это **готовые классовые представления** из модуля
# `django.contrib.auth.views`, которые позволяют **выполнить вход и выход пользователя
# без написания собственного кода.**
