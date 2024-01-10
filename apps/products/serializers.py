from apps.models import Favorite, Image, Product, Promotion, Cart, Rate, Review, Category, Review_Likes, User
from rest_framework import serializers
from ..orders.serializers import Order_itemSerializers, OrderSerializers


class PromotionSerializers(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M', read_only=True)
    end_date = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Promotion
        fields = "__all__"


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    def to_representation(self, instance):
        return instance.image.url

    class Meta:
        model = Image
        fields = ['id', 'image', ]


class ProductSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)
    # image = serializers.SerializerMethodField(read_only=True)
    image = ImageSerializer(read_only=True, many=True)
    new_price = serializers.SerializerMethodField(read_only=True)
    promotion = serializers.SerializerMethodField(read_only=True)

    def get_promotion(self, obj):
        promotion = obj.promotion_product.filter(
            is_active=True).first() or None

        return promotion.promotion.discount_rate if promotion else 0

    def get_new_price(self, obj):
        promotion = obj.promotion_product.filter(
            promotion__is_active=True).first()
        if promotion and promotion.promotion.is_active and promotion.promotion.discount_rate > 0:
            discount_rate = float(promotion.promotion.discount_rate)
            discounted_amount = (float(obj.price) * discount_rate) / 100.0
            new_price = float(obj.price) - discounted_amount
            # Round to 2 decimal places for currency
            return round(new_price, 2)
        else:
            return float(obj.price)

    def get_image(self, obj):
        return obj.image.first() or None

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
    user = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        # self.user = self.context.get('user').id
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

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
        formatted_review_date = instance.review_date.strftime('%Y-%m-%d %H:%M')

        date = {
            'id': instance.id,
            'user': f"{instance.user.get_full_name()}",
            'review_date': formatted_review_date,
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
    image = ImageSerializer(read_only=True, many=True)
    new_price = serializers.SerializerMethodField(read_only=True)
    promotion = serializers.SerializerMethodField(read_only=True)

    def get_promotion(self, obj):
        promotion = obj.promotion_product.filter(
            is_active=True).first() or None

        return promotion.promotion.discount_rate if promotion else 0

    def get_new_price(self, obj):
        promotion = obj.promotion_product.filter(
            promotion__is_active=True).first()
        if promotion and promotion.promotion.is_active and promotion.promotion.discount_rate > 0:
            discount_rate = float(promotion.promotion.discount_rate)
            discounted_amount = (float(obj.price) * discount_rate) / 100.0
            new_price = float(obj.price) - discounted_amount
            # Round to 2 decimal places for currency
            return round(new_price, 2)
        else:
            return float(obj.price)

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


class ReviewLikeSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        # self.user = self.context.get('user').id
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

    class Meta:
        model = Review_Likes
        fields = '__all__'


class RateSerializers(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        # self.user = self.context.get('user').id
        attrs['user'] = self.context.get('user')
        return super().validate(attrs)

    class Meta:
        model = Rate
        fields = '__all__'


class DeleteReviewLikeSerializers:
    user = serializers.IntegerField

    class Meta:
        model = Review_Likes
        fields = ('user', 'review')
