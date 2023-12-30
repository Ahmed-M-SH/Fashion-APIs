from apps.models import Favorite, Product, Promotion, Cart, Rate, Review, Category, Promotion_category, Review_Likes, User
from rest_framework import serializers

from apps.products.serializers import ProductSerializer


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializers Class
    Args:
        serializers (Category): Get, Add , Delete, Update Category for All Levels
    """
    sub_category = serializers.SerializerMethodField(read_only=True)

    def get_sub_category(self, obj):
        """Get All Three Levels in Category (Main Category - Category - Sub Category)

        Args:
            Object -> Category
        Returns:
            List of Categorys start with Main , end with Sub_category
        """
        result = {}
        data = Category.objects.filter(parent=obj)
        for item in data:
            t = {
                'id': item.id,
                'name': item.name,
                "level": item.level,
                'sub_category': Category.get_children(item).values(),

            }
            result[str(item.name)] = t
        # result = get_all_children(obj)
        return result

    class Meta:
        model = Category
        fields = "__all__"
