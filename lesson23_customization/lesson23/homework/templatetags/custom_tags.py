from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def current_time():
    return datetime.now().strftime("%H:%M:%S")

@register.filter
def upper(value):
    return value.upper()
