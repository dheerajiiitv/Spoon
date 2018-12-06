from django import template

register = template.Library()


@register.filter(name='increment')
def increment(value, n):
    value = int(value) + int(n)
    return value

@register.filter(name='decrement')
def decrement(value, n):
    value = int(value) - int(n)
    return value