from rest_framework import serializers

from apps.models import City, Currency, Order, Order_item


class Order_itemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'


class CitySerializers(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class CurrencySerializers(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):

    order_item = Order_itemSerializers(many=True, read_only=True)
    currency = CurrencySerializers(read_only=True)
    city = CitySerializers(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']

# class OrderDtailSerializers(serializers.Serializer):
#     currency=serializers.SerializerMethodField(read_only=True)
#     city=serializers.SerializerMethodField(read_only=True)
