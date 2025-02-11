from django import template


register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter  
def format_currency(value):
    try:
        value = float(value)
        formatted_value = f"{value:,.2f}"
        formatted_value = formatted_value.replace(",", " ").replace(".", ",")
        return f"{formatted_value} €"
    except (ValueError, TypeError):
        return value