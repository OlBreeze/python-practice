from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_date(value):
    """Форматировать дату в красивый вид"""
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y %H:%M")
    return value

# {{ some_date|format_date }} пример использования