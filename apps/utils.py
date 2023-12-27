from datetime import timezone
from django.db.models import Sum
from .models import Order_item, Order, Product, Promotion, Category, User
import datetime


def all_sales():
    # Retrieve all order items
    all_order_items = Order_item.objects.all()

    # Calculate total sales for all orders
    total_all_sales = all_order_items.aggregate(
        total_sales=Sum('total_price'))['total_sales'] or 0

    # You can also include additional information or filtering based on your requirements
    return total_all_sales


def last_day_sales():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=1)

    # Retrieve orders and order items for the last day
    orders_last_day = Order.objects.filter(date__range=(start_date, end_date))
    order_items_last_day = Order_item.objects.filter(
        order_id__in=orders_last_day)

    # Calculate total sales for the last day
    total_sales_last_day = order_items_last_day.aggregate(
        total_sales=Sum('total_price'))['total_sales'] or 0

    # You can also include additional information or filtering based on your requirements
    return total_sales_last_day


def total_products():
    total = Product.objects.all().count()
    return total


def total_categorys():
    total = Category.objects.all().count()
    return total


def total_users():
    return User.objects.all().count()


def total_customer():

    return User.objects.filter(is_superuser=False, is_staff=False).count()


def active_promotion():
    return Promotion.objects.filter(is_active=True).count()


def total_orders():
    return Order.objects.all().count()


def total_orders_deleverd():
    return Order.objects.filter(is_deleverd=False).count()
