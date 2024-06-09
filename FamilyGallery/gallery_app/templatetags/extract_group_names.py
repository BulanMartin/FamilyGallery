from django import template

register = template.Library()

@register.filter
def group_names(groups):
    return [group.name for group in groups]