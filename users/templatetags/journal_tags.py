from django import template

register = template.Library()


@register.filter
def splitpart(value):
    if len(value.split()) == 3:
        return f'{value.split()[0]} {value.split()[1][0]}. {value.split()[2][0]}.'
    elif len(value.split()) == 2:
        return f'{value.split()[0]} {value.split()[1][0]}. '
    else:
        return f'{value.split()[0]}'
