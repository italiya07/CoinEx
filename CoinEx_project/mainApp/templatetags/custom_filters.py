# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()


@register.filter
def get_index_color(value):
    try:
        value = int(value)  # Convert value to integer
    except ValueError:
        return "gray"  # Return a default color for non-integer values

    if 1 <= value <= 20:
        return "red"
    elif 21 <= value <= 40:
        return "#FFA07A"
    elif 41 <= value <= 60:
        return "orange"
    elif 61 <= value <= 80:
        return "lightgreen"
    elif 81 <= value <= 100:
        return "green"
    else:
        return "gray"
