from rest_framework import serializers

from apps.models import City, Currency, Order, Order_item, Payment_type, Product


class Order_itemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'


class CitySerializers(serializers.ModelSerializer):
    def to_representation(self, instance: City):
        return instance.name

    class Meta:
        model = City
        fields = '__all__'


class CurrencySerializers(serializers.ModelSerializer):

    def to_representation(self, instance: Currency):
        return instance.currency_name

    class Meta:
        model = Currency
        fields = '__all__'


class Payment_TypeSerializers(serializers.ModelSerializer):

    def to_representation(self, instance: Payment_type):
        return instance.name

    class Meta:
        model = Payment_type
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    qty = serializers.IntegerField()

    class Meta:
        model = Order_item
        fields = ['product', 'qty']


class GetOrderSerializers(serializers.ModelSerializer):
    currency = CurrencySerializers()
    city = CitySerializers()
    payment_type = Payment_TypeSerializers()
    item_count = serializers.SerializerMethodField(read_only=True)

    def get_item_count(self, obj):
        return obj.order_item.all().count()

    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']


class OrderSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=None)
    order_items = OrderItemSerializer(many=True, write_only=True)

    def validate(self, attrs):
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for order_item_data in order_items_data:
            Order_item.objects.create(order=order, **order_item_data)

        return order

    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']


# class PaymentDetailSerializers(serializers.ModelSerializer):
#     order_item = Order_itemSerializers(many=True, read_only=True)
#     currency = CurrencySerializers(many=True, read_only=True)
#     city = CitySerializers(many=True, read_only=True)
#     payment_Type = Payment_TypeSerializers(many=True, read_only=True)


    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']

# class OrderDtailSerializers(serializers.Serializer):
#     currency=serializers.SerializerMethodField(read_only=True)
#     city=serializers.SerializerMethodField(read_only=True)
