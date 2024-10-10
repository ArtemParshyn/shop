# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='split')
def split(value, separator=' '):

    return value.split(separator)
