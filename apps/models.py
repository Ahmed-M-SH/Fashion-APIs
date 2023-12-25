from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(_("Start Date"))
    end_date = models.DateTimeField(
        _("End Date"), auto_now=False, auto_now_add=False)
    discount_rate = models.FloatField(_("discount rate"))
    # class Meta:
    #     table_name = "Promotion"


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, related_name='children', null=True, default=0)
    name = models.CharField(max_length=50)
    category_image = models.ImageField(
        _("category image"), upload_to="category_image",)

    class MPTTMeta:
        # level_attr = 'parint'
        order_insertion_by = ['name']

    def __str__(self):
        return f"name: {self.name} parent {self.parent} id {self.id} "


class Promotion_category(models.Model):
    promotion = models.ForeignKey(
        Promotion, verbose_name=_("Promotion"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_(
        "category"), on_delete=models.CASCADE)
    created_date = models.DateTimeField(
        _("created at"), auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(
        _("Updated at"), auto_now=True, auto_now_add=False)


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    name = models.CharField(max_length=50, default="")
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=8)
    description = models.TextField()
    image = models.ImageField(_("Image"), upload_to="products_image",)


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE)
    review_date = models.DateTimeField(auto_now_add=True)
    review_text = models.TextField()


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE)
    qty = models.IntegerField(_("qty"))
    date = models.DateTimeField(auto_now=False, auto_now_add=True)


class Rate(models.Model):
    rating_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating_no = models.FloatField(_("rating_no"), max_length=5)
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE)


class Order(models.Model):
    proof_of_payment_image = models.ImageField(
        _("proof_of_payment_image"), upload_to="proof_of_payment_image")
    payment_type = models.CharField(_(""), max_length=50)
    customer_name = models.CharField(_("customer name"), max_length=100)
    customer_phone = models.CharField(_("customer phone"), max_length=50)
    total = models.DecimalField(_("total"), max_digits=10, decimal_places=2)
    date = models.DateTimeField(_("Date"), auto_now=False, auto_now_add=True)


class Order_item(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "Products"), on_delete=models.DO_NOTHING)
    order_id = models.ForeignKey(Order, verbose_name=_(
        "Order"), on_delete=models.DO_NOTHING)
    qty = models.IntegerField(_("qty"))
    date = models.DateTimeField(_("Date"), auto_now=False, auto_now_add=True)
    price = models.DecimalField(_("Price"), decimal_places=2, max_digits=8)
    total_price = models.DecimalField(
        _("Total Price"), decimal_places=2, max_digits=8)
