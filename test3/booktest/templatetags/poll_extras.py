from django import template

register = template.Library()

@register.filter
def mod(value):
    return value%2 == 0