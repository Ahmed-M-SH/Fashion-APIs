from apps.models import Favorite, Product, Promotion, Cart, Rate, Review, Category, Review_Likes, User
from rest_framework import serializers

from apps.products.serializers import ProductSerializer
from ..orders.serializers import Order_itemSerializers, OrderSerializers


class FavoriteSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)
    product = ProductSerializer(many=True, read_only=True)

    def validate(self, attrs):
        # self.user = self.context.get('user').id
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

    class Meta:
        model = Favorite
        fields = '__all__'


class CreateFavoriteSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=None)
    # product = ProductSerializer(many=True, read_only=True)

    def validate(self, attrs):
        # self.user = self.context.get('user').id
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

    class Meta:
        model = Favorite
        fields = '__all__'
