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
        """
        Get all three levels in Category (Main Category - Category - Sub Category)

        Args:
            obj (Category): Object representing the category.

        Returns:
            list: List of dictionaries containing information about subcategories.
        """
        result = []
        sub_categories = Category.objects.filter(parent=obj)

        for sub_category in sub_categories:
            sub_category_info = {
                'id': sub_category.id,
                'name': sub_category.name,
                'level': sub_category.level,
                'sub_category': Category.get_children(sub_category).values(),
            }
            result.append(sub_category_info)

        return result

    class Meta:
        model = Category
        fields = "__all__"
