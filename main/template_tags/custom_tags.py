from django.template.defaulttags import register
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_header(dictionary, key):
    return dictionary.get(key).items()

@register.filter
def index(indexable, i):
    return indexable[i]