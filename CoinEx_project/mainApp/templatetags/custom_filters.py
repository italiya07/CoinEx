# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_index_color(value):
    if value >= 1 and value <= 20:
        return "red"
    elif value >= 21 and value <= 40:
        return "#FFA07A"
    elif value >= 41 and value <= 60:
        return "orange"
    elif value >= 61 and value <= 80:
        return "lightgreen"
    elif value >= 81 and value <= 100:
        return "green"
    else:
        return "gray"