from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    if value:
        return value.split(key)
    return []
