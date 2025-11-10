from django.shortcuts import render

def home(request):
    """Головна сторінка"""
    context = {
        'title': 'Головна',
        'welcome_message': 'Ласкаво просимо на наш сайт!'
    }
    return render(request, 'main/home.html', context)

def about(request):
    """Сторінка про сайт"""
    context = {
        'title': 'Про сайт',
        'description': 'Це навчальний Django-проект, створений для демонстрації роботи з шаблонами, представленнями та маршрутизацією.'
    }
    return render(request, 'main/about.html', context)

def contact(request):
    """Сторінка контактів"""
    context = {
        'title': 'Контакти',
        'contacts': {
            'phone': '+380 12 345 6789',
        }
    }
    return render(request, 'main/contact.html', context)