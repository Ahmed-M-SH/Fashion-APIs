from rest_framework import serializers

from apps.models import Order, Order_item, Product, Promotion, Cart, Rate, Review, Category,  User


class Order_itemSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):

    order_item = Order_itemSerializers(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'  # ['__all__', 'order_item']


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)

    def get_review(self, obj):
        # user = self.context.get('user' or None)
        return obj.review.filter(product__id=obj.pk).count()
        # return user.review.filter(item=obj).count() if isinstance(user, User) else False

    def get_rate(self, obj):
        # user = self.context.get('user' or None)
        rat = obj.rate.all()
        sub = 0.0
        if rat.exists():
            try:
                for s in rat:
                    sub += s.rating_no
                return sub / rat.count()
            except:
                sub = 0
                return sub
        else:
            return sub
        # return user.review.filter(item=obj).count() if isinstance(user, User) else False

    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def to_representation(self, instance):

        r = 0.0
        image = instance.user.image.url if instance.user.image else ''
        if instance.user.rate.filter(product=instance.product).exists():
            r = instance.user.rate.get(
                product=instance.product).rating_no
        date = {
            'user': f"{instance.user.get_full_name()}",
            'review_date': instance.review_date,
            'review_text': instance.review_text,
            'rating': r,
            'profile': image
        }
        return date


class SingleProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    review_no = serializers.SerializerMethodField(read_only=True)
    review = ReviewSerializers(many=True, read_only=True)

    def get_review_no(self, obj):
        # user = self.context.get('user' or None)
        return obj.review.filter(product=obj).count() or 0
        # return user.review.filter(item=obj).count() if isinstance(user, User) else False

    def get_rate(self, obj):
        # user = self.context.get('user' or None)
        rat = obj.rate.all()
        sub = 0.0
        if rat.exists():
            try:
                for s in rat:
                    sub += s.rating
                return sub / rat.count()
            except:
                sub = 0
                return sub
        else:
            return sub
        # return user.review.filter(item=obj).count() if isinstance(user, User) else False

    class Meta:
        model = Product
        fields = '__all__'


# class CreateReviewserializers:
