from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def current_time(format_string="%H:%M:%S"):
    """Выводит текущее время"""
    return datetime.now().strftime(format_string)


# {% load custom_tags %}
# <p>Сейчас: {% current_time "%d.%m.%Y %H:%M:%S" %}</p>