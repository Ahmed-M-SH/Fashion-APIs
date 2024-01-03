from django.db import models
from .models import City, Currency, Favorite, Image, Notification, Product, Promotion, Cart, Category,  Order, Order_item, Promotion_product, Rate, Review, User, Review_Likes
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.admin import UserAdmin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
    ReadOnlyPasswordHashField,
    UsernameField,
)  # Register your models here.


class CustomUserChangeForm(forms.ModelForm):
    """
    Custom UserChangForm For AdminUser registertions
    """
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = User
        fields = ("name", "phone_number", "email", "is_active", "is_staff",
                  "is_superuser",  "groups", "username",)
        # field_classes = {"email": forms.EmailField}


class CustomUserCreationForm(UserCreationForm):
    """
        Custom UserChangForm For AdminUser registertions
    """
    class Meta:
        model = User
        fields = ("name", "phone_number", "email", "is_active", "is_staff",
                  "is_superuser",  "groups", "username",)
        # field_classes = {'email': forms.EmailField}


class CustomAdminUser(UserAdmin):
    """
        Custom CustomUSerAdmin For User registertions to add grops and Custom Disgan

    """
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {
         "fields": ("name", "phone_number", "email", 'image')}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "is_deleted"
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", 'name', 'phone_number'),
            },
        ),
    )
    form = CustomUserChangeForm
    # add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("username", "email", "name",
                    "is_staff", 'is_deleted', 'is_active')
    list_filter = ("is_staff", "is_superuser",
                   "is_active", "groups",  'is_deleted', 'is_active')
    search_fields = ("username",
                     "phone_number", "name", "email")
    ordering = ("id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):

        qs = self.model._default_manager.get_queryset()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.all()
        return qs


admin.site.register(User, CustomAdminUser)


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


# admin.site.register(Product)

admin.site.register(Category, CategoryAdmin)

admin.site.register([
    Order_item,
    # Promotion,
    # Promotion_product,
    Cart,
    Rate,
    Review_Likes,
    Favorite,
    City,
    Currency,
    # Image
    Notification

])

admin.site.register(Review, admin.ModelAdmin)


class OrderItemInline(admin.TabularInline):
    model = Order_item
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'customer_name',
                    'customer_phone', 'total_paid', 'date')
    search_fields = ['customer_name', 'customer_phone']


admin.site.register(Order, OrderAdmin)


class CustomPromotionProductForm(forms.ModelForm):
    class Meta:
        model = Promotion_product
        fields = '__all__'


class CustomPromotionProductAdmin(admin.ModelAdmin):
    form = CustomPromotionProductForm


# admin.site.register(Promotion_product, CustomPromotionProductAdmin)


# class CustomPromotionProductAdmin(admin.ModelAdmin):
#     form = CustomPromotionProductForm

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         # Add additional customization to the form if needed
#         return form


admin.site.register(Promotion_product, CustomPromotionProductAdmin)


class PromotionProductInline(admin.StackedInline):
    model = Promotion_product
    extra = 1


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1


class CustomProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, PromotionProductInline]
    list_display = ('name', 'price')


admin.site.register(Product, CustomProductAdmin)
