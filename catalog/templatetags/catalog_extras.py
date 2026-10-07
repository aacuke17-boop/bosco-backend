from django import template

from catalog.models import Product

register = template.Library()


@register.filter
def uah(value):
    try:
        return f'{float(value):,.2f}'.replace(',', ' ') + ' грн'
    except (TypeError, ValueError):
        return value


@register.simple_tag
def product_count():
    return Product.objects.count()