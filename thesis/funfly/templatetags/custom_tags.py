from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def classname(obj):
    return obj.__class__.__name__