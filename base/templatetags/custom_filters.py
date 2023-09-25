from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits a string into a list based on the given key.
    """
    return value.split(key)
