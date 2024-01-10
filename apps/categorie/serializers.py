from apps.models import Favorite, Product, Promotion, Cart, Rate, Review, Category, Review_Likes, User
from rest_framework import serializers

from apps.products.serializers import ProductSerializer


def get_all_children(obj):
    result = {
        'id': obj.id,
        'name': obj.name,
        "level": obj.level,
        'category_image': obj.category_image.url,
        'sub_category': []
    }
    if Category.get_children(obj).exists():
        children = []
        for item in Category.get_children(obj):
            children.append(get_all_children(item))
        result['sub_category'] = children
    # sub_categories = Category.objects.filter(parent=obj)

    # for sub_category in sub_categories:
    #     sub_category_info = {
    #         'id': sub_category.id,
    #         'name': sub_category.name,
    #         'level': sub_category.level,
    #         'sub_category': Category.get_children(sub_category).values(),
    #         'category_image': sub_category.category_image.url,
    #         'lft': sub_category.lft,
    #         "rght": sub_category.rght,
    #         "tree_id": sub_category.tree_id,
    #         "parent_id": sub_category.parent_id,
    #     }
    #     result.append(sub_category_info)

    return result


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializers Class
    Args:
        serializers (Category): Get, Add , Delete, Update Category for All Levels
    """
    # sub_category = serializers.SerializerMethodField(read_only=True)
    have_children = serializers.SerializerMethodField(read_only=True)

    def get_have_children(self, obj: Category):

        return obj.get_children().exists()

    def get_sub_category(self, obj):
        """
        Get all three levels in Category (Main Category - Category - Sub Category)

        Args:
            obj (Category): Object representing the category.

        Returns:
            list: List of dictionaries containing information about subcategories.
        """
        # result = []

        # result = {
        #     'id': obj.id,
        #     'name': obj.name,
        #     "level": obj.level,
        #     'children': []
        # }

        # if Category.get_children(obj).exists():
        #     children = []
        #     for item in Category.get_children(obj):
        #         children.append(get_all_children(item))
        #     result['children'] = children
        # sub_categories = Category.objects.filter(parent=obj)

        # for sub_category in sub_categories:
        #     sub_category_info = {
        #         'id': sub_category.id,
        #         'name': sub_category.name,
        #         'level': sub_category.level,
        #         'sub_category': Category.get_children(sub_category).values(),
        #         'category_image': sub_category.category_image.url,
        #         'lft': sub_category.lft,
        #         "rght": sub_category.rght,
        #         "tree_id": sub_category.tree_id,
        #         "parent_id": sub_category.parent_id,
        #     }
        #     result.append(sub_category_info)

        return get_all_children(obj=obj)

    class Meta:
        model = Category
        # fields = ('id', 'name', "category_image", "sub_category", "level",)
        fields = '__all__'
