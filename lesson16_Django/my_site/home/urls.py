from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home_page, name='home'),
    re_path(r'^about/$', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),

    re_path(r'^post/(?P<id>\d+)/$', views.post_view, name='post'),
    re_path(r'^profile/(?P<username>[a-zA-Z]+)/$', views.profile_view, name='profile'),
    re_path(r'^event/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', views.event_view, name='event'),

    # (?P<year>\d{4}) — захоплює рівно 4 цифри для року
    # (?P<month>\d{2}) — захоплює рівно 2 цифри для місяця
    # (?P<day>\d{2}) — захоплює рівно 2 цифри для дня
]
