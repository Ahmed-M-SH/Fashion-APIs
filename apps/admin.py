from django.contrib import admin
from django.contrib.admin import ModelAdmin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Promotion, Cart, Category, Promotion_category, Order, Order_item, Rate, Review
# Register your models here.


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'
# Register your models here.


admin.site.register(Product)

admin.site.register(Category, CategoryAdmin)

admin.site.register([
    Order_item,
    Promotion,
    Promotion_category,
    Cart,
    Rate,
])

admin.site.register(Review, ModelAdmin)


class OrderItemInline(admin.TabularInline):
    model = Order_item
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'customer_name',
                    'customer_phone', 'total_paid', 'date')
    search_fields = ['customer_name', 'customer_phone']


admin.site.register(Order, OrderAdmin)
