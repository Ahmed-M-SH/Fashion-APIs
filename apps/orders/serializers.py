from rest_framework import serializers

from apps.models import Order, Order_item


class Order_itemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):

    order_item = Order_itemSerializers(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']
