from django import template

register = template.Library()


@register.filter
def pluralize_response(value, args=("е", "я", "й")):
    if not value:
        value = 0
    ending = get_ending(value, args)
    return ending


@register.filter
def pluralize_views(value, args=("", "а", "ов")):
    ending = get_ending(value, args)
    return ending


def get_ending(value, args):
    number = abs(int(value))
    a = number % 10
    b = number % 100
    if (a == 1) and (b != 11):
        return args[0]
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return args[1]
    else:
        return args[2]
