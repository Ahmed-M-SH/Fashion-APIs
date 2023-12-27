from django import template
from apps.models import Order, Order_item
from django.db.models import Sum
from apps.utils import all_sales, last_day_sales, total_orders, total_orders_deleverd, total_products, total_categorys, total_customer, total_users, active_promotion


register = template.Library()


@register.simple_tag
def get_all_sales():

    return all_sales


@register.simple_tag
def get_last_day_sales():

    return last_day_sales


@register.simple_tag
def get_total_products():

    return total_products


@register.simple_tag
def get_total_categorys():

    return total_categorys


@register.simple_tag
def get_total_user():

    return total_users


@register.simple_tag
def get_total_customer():

    return total_customer


@register.simple_tag
def get_active_promotion():

    return active_promotion


@register.simple_tag
def get_total_orders():

    return total_orders


@register.simple_tag
def get_total_orders_deleverd():

    return total_orders_deleverd


@register.simple_tag
def get_all_oreders():
    return Order.objects.all()
