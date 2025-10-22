from django.shortcuts import render
from django.views import View
from datetime import datetime


def home(request):
    """Головна сторінка"""
    context = {
        'title': 'Головна',
        'welcome_message': 'Ласкаво просимо на наш сайт!',
        'description': 'Ми надаємо якісні послуги для вашого бізнесу. Наша команда професіоналів завжди готова допомогти вам досягти успіху.',
        'current_date': datetime.now(),
    }
    return render(request, 'main/home.html', context)


def about(request):
    """Сторінка про нас"""
    context = {
        'title': 'Про нас',
        'company_name': 'ТОВ "Наша Компанія"',
        'description': 'Наша компанія була заснована у 2010 році і '
                       'з тих пір стала лідером у своїй галузі. Ми прагнемо надавати найкращі послуги нашим клієнтам та постійно вдосконалюємося.',
        'mission': 'Наша місія - зробити світ кращим через інновації та якісний сервіс.',
        'founded_year': 2010,
        'last_updated': datetime(2024, 10, 15),
        'has_contact': True,
    }
    return render(request, 'main/about.html', context)


class ContactView(View):
    """Контактна сторінка"""

    def get(self, request):
        context = {
            'title': 'Контакти',
            'address': 'вул. Хрещатик, 1, Київ, Україна',
            'phone': '+380 44 123 4567',
            'email': 'info@ourcompany.ua',
            'working_hours': 'Пн-Пт: 9:00 - 18:00',
            'has_email': True,
        }
        return render(request, 'main/contact.html', context)


class ServiceView(View):
    """Сторінка послуг"""

    def get(self, request):
        services = [
            {
                'name': 'Веб-розробка',
                'description': 'Створення сучасних та функціональних веб-сайтів для вашого бізнесу з використанням найновіших технологій',
                'price': 'від 10000 грн',
                'available': True,
            },
            {
                'name': 'Мобільні додатки',
                'description': 'Розробка iOS та Android додатків з інтуїтивним інтерфейсом',
                'price': 'від 25000 грн',
                'available': True,
            },
            {
                'name': 'SEO оптимізація',
                'description': 'Просування вашого сайту в пошукових системах для збільшення відвідуваності',
                'price': 'від 5000 грн/міс',
                'available': True,
            },
            {
                'name': 'Дизайн',
                'description': 'Створення унікального дизайну для вашого бренду',
                'price': 'від 8000 грн',
                'available': False,
            },
            {
                'name': 'Консультації',
                'description': 'Професійні консультації з IT питань',
                'price': 'від 1000 грн/год',
                'available': True,
            },
        ]

        context = {
            'title': 'Наші послуги',
            'services': services,
            'total_services': len(services),
            'last_updated': datetime(2025, 10, 22),
        }
        return render(request, 'main/services.html', context)
