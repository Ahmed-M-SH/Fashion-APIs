from sqlite3 import IntegrityError
from apps.models import Favorite, Product, Promotion, Cart, Rate, Review, Category, Review_Likes, User
from rest_framework import serializers

from apps.products.serializers import ProductSerializer
from ..orders.serializers import Order_itemSerializers, OrderSerializers


# from rest_framework import serializers
# from apps.models import Product_item, Cart, Store, Image, User
# from django.conf import settings


class CartListSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    new_price = serializers.SerializerMethodField(read_only=True)
    promotion = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    def get_image(self, obj):
        image = obj.product.image.first()
        return image.image.url if image else ""

    def get_name(self, obj):
        return obj.product.name

    def get_promotion(self, obj):
        return obj.product.get_promotion()

    def get_new_price(self, obj):

        return obj.product.get_new_price()

    def get_price(self, obj):
        return obj.product.price

    class Meta:
        model = Cart
        fields = ('id', 'name', 'price', 'new_price', 'qty',
                  'promotion', 'product', 'image', 'date')


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


# class ProductSerialier(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     dic = 0.0
    #     image = None
    #     try:
    #         dic = Product_Discount.objects.filter(
    #             product=instance, is_active=True).first().discount.discount_value
    #         image = Image.objects.filter(product=instance).first().image.url
    #     except:
    #         dic = 0.00
    #     data = {
    #         'id': instance.id,
    #         'name': instance.product_name,
    #         'discount': dic,
    #         'price_per_unit': instance.price_per_unit,
    #         'image': image
    #     }
    #     return data
        # discount = Product_Discount.objects.filter(
        #     product=instance, is_active=True).first().discount.discount_value
        # data = {
        #     'name': instance.date,
        #     'discount': discount,
        #     'price_per_unit': instance.price_per_unit
        # }
        # return data

#     class Meta:
#         model = Product
#         fields = '__all__'


class CartViewSerializer(ProductSerializer):
    """
    instance form Product Item Serializer Class

    extre fields :
    - count
    - cart_id
    """
    # product = ProductSerialier(read_only=True)
    # product = serializers.SerializerMethodField(read_only=True)

    product_name = serializers.SerializerMethodField(read_only=True)
    # count = serializers.SerializerMethodField(read_only=True)
    cart_id = serializers.SerializerMethodField(read_only=True)

    def get_count(self, obj) -> int:
        user = self.context.get('user')
        return obj.item_Cart.get(user_id=user.id).qty

    # def get_product_name(self, obj) -> str:
    #     return obj.product.product_name

    # def get_cart_id(self, obj) -> int:
    #     user = self.context.get('user')
    #     return obj.item_Cart.get(user_id=user.id).id
        # stor = obj.item.product.store
        # data = {
        #     'id': stor.pk,
        #     'name': stor.store_name,
        #     'image': stor.image.url
        # }
        # return data
    # class Meta:
    #     model = Cart
    #     fields = ('id', 'time_created', 'count', 'store')


class CartSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField()
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    # user = serializers.HiddenField(default=None)

    def create(self, validated_data):
        user = self.context['user']
        product_id = validated_data['product']
        qty = validated_data.get('qty') or 1

        # Check if the Cart object already exists for the given product and user
        cart, created = Cart.objects.get_or_create(
            user=user, product_id=product_id)

        # Update the quantity if the Cart object already exists
        if not created:
            cart.qty = qty
            cart.save()

        return cart

    class Meta:
        model = Cart
        fields = ('product', 'qty', 'date')


class AddToCartSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ('product_id', 'qty')


# class TestCartSerializer(serializers.ModelSerializer):
#     # product_store = serializers.RelatedField(read_only=True, many=True)
#     product_store = ProductSerialier(read_only=True, many=True)
#     # product = serializers.SerializerMethodField(read_only=True)
#     # store = serializers.SerializerMethodField(read_only=True)

#     # def get_product(self, obj):
#     #     product = Product.objects.filter(
#     #         Product_Cart__user=settings.AUTH_USER_MODEL, store=obj)

#     # def validate(self, attrs):
#     #     store = Store.objects.get(id=attrs.get('id'))
#     #     product = Product.objects.filter(store=store)
#     #     return super().validate(attrs)

#     # def get_store(self, obj):
#     #     stor = obj.product.store
#     #     data = {
#     #         'id': stor.pk,
#     #         'name': stor.store_name,
#     #         'image': stor.image.url
#     #     }
#     #     return data

#     class Meta:
#         model = Store
#         # fields = ('id', 'time_created', 'count', 'product', 'store')
#         fields = ('id', 'store_name', 'product_store')
