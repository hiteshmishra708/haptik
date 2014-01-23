from django import template
from django.template.defaultfilters import stringfilter
from datetime import timedelta

register = template.Library()

@register.filter
@stringfilter
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.filter
def convert_to_pst(value):
    return value - timedelta(hours=8)

@register.filter
def convert_to_ist(value):
    return value + timedelta(minutes=330)
