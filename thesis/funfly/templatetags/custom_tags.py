from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='is_in_group')
def is_in_group(user, group_name):
    if user:
        return user.groups.filter(name=group_name).exists()

@register.filter
def classname(obj):
    return obj.__class__.__name__


@register.filter()
def error_avatar(obj):
    if hasattr(obj, 'avatar'):
        if hasattr(obj.avatar, 'url'):
            return obj.avatar.url
        else:
            return ''
    else:
        return ''

@register.filter()
def tranform_gender_to_string(obj):
    if obj == '0':
        return 'Female'
    else:
        return 'Female'