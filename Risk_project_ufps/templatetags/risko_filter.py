from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='reducir')
@stringfilter
def reducir(value):
    length = len(value)
    if(length > 20):
    	value = value[:17] + "..."
    return value