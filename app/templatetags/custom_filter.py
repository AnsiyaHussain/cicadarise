from django import template
from ..models import Products   # Correct import

register = template.Library()

# Currency filter
@register.filter(name='currency')
def currency(number):
    return "₹" + str(number)

# Multiply filter (used in cart calculations)
@register.filter(name='multiply')
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

# Get product object from ID (used in side cart)
@register.filter
def product_from_id(product_id):
    try:
        return Products.objects.get(id=int(product_id))
    except (Products.DoesNotExist, ValueError, TypeError):
        return None