from apps.models import Product, Promotion, Cart, Rate, Review, Category, Promotion_category, User
from rest_framework import serializers
from ..orders.serializers import Order_itemSerializers, OrderSerializers


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
        user = self.context.get('user' or None)
        is_likes = instance.review_likes.filter(
            user=user).exists()
        likes = instance.review_likes.all().count()
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
            'profile': image,
            'likes_count': likes,
            'is_liked': is_likes

        }
        return date


class SingleProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    review_count = serializers.SerializerMethodField(read_only=True)
    review = ReviewSerializers(many=True, read_only=True)
    in_favorite = serializers.SerializerMethodField(read_only=True)
    in_cart = serializers.SerializerMethodField(read_only=True)

    def validate(self, attrs):
        self.review.context = self.context
        return super().validate(attrs)

    def get_review_count(self, obj):
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

    def get_in_favorite(self, obj) -> bool:
        user = self.context.get('user' or None)
        # if isinstance(user, User) else False
        return obj.favorites.filter(user=user).exists()

    def get_in_cart(self, obj) -> bool:
        user = self.context.get('user' or None)
        # if isinstance(user, User) else False
        return obj.cart.filter(user=user).exists()

    class Meta:
        model = Product
        fields = '__all__'


# class CreateReviewserializers:
