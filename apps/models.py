from PIL import Image as PImage
from xmlrpc.client import TRANSPORT_ERROR
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class MyUserManager(BaseUserManager):
    """
    Custom User Manager
    """

    def _create_user(self,  email, username,  password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        # GlobalUserModel = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        # username = GlobalUserModel.normalize_username(username)
        user = self.model(email=email,  username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None,  password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)


# ==========


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custome User to create and login user with email and auth_provider like google, facebook or Email.\n
    Auth_provider is default by email.\n

    To Use Choices in auth_provider use  User.EMAIL or User.GOOGLE etc...\n

    AUTHENTICATION:\n
        We use JWT auth for this project
    """
    # Choices
    EMAIL = 'email'
    GOOGLE = 'google'
    FACEBOOB = 'facebook'
    username = models.CharField(
        _("username"),
        max_length=150,
        # unique=True,
        null=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        blank=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    # auth_provider = models.CharField(
    #     max_length=20, blank=True, null=False, default=EMAIL)
    name = models.CharField(
        _('Full name'), max_length=60, default='', blank=True)
    # first_name = models.CharField(
    #     _("first name"), max_length=55, blank=True, default='')
    # last_name = models.CharField(
    #     _("last name"), max_length=55, blank=True, default='')
    # age = models.IntegerField(_('age'), blank=True, null=True)
    # =============
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(
        _("phone number"),  max_length=50, default='', null=True)
    register_data = models.CharField(max_length=20, default='')
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_deleted = models.BooleanField(_('Deleted'), default=False,)
    date_joined = models.DateTimeField(
        _("date joined"), default=timezone.now, )
    image = models.ImageField(
        upload_to='user_image',
        # default='user_image/MicrosoftTeams-image.png',
        blank=True,
        null=True
    )

    ########## ManyToMAny Fileds ###########
    # product_view = models.ManyToManyField("Product_item", through='View')
    # wishlist = models.ManyToManyField(
    #     'Product_item', through='Wishlist')
    # favorite = models.ManyToManyField('Product_item', through='Favorite')
    # cart = models.ManyToManyField('Product_item', through='Cart')
    # add_rate = models.ManyToManyField('Product_item', through='Rate')

    objects = MyUserManager()
    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        """
        Return the name, with a space in between.
        """
        full_name = "%s " % (self.name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.name

    def delete(self, *args, **kwargs):
        """
        Overrid delete method to delete Image first then delete user
        not will be show in admin panle and aothre thinks like auth

        """

        try:
            self.image.delete()
            self.is_deleted = True
            self.is_active = False
            self.is_superuser = False
            self.save()
            return True
        except:
            self.is_deleted = True
            self.save()
            return True

        # return super().delete(*args, **kwargs)
    def get(self,  **kwargs):
        user = self.objects.get(**kwargs, is_delete=False) or None
        if user:
            return user
        raise self.DoesNotExist()

    def __str__(self) -> str:
        return f" {self.pk} |{self.email}:{self.name}"

    # Start Method for Class

    def add_cart(self, item_id: int, count: int):
        try:
            return self.cart.create(product_id=item_id, qty=count)
        except:
            ins = self.cart.get(product_id=item_id)
            ins.qty = count
            return ins.save()

    def add_favorite(self, item_id: int):
        try:
            data = self.favorites.get_or_create(product_id=item_id)
            return data[0]
        except:
            return False

    def remove_favorite(self, item_id: int):
        pass
        # End Method for Class

    class Meta:
        # swappable = "AUTH_USER_MODEL"
        db_table = 'User'
        verbose_name = 'إدارة المسنخدمين'


# Create your models here.

class Notification(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    text = models.TextField(default='')
    # type = models.CharField(max_length=30, default='')
    # user = models.ManyToManyField(User, through='User_notification',)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification', )
    time_created = models.DateTimeField(
        _("وقت الانشاء"), auto_now=False, auto_now_add=True)
    is_readed = models.BooleanField(
        _("حالة القرائة"), editable=False, default=False)
    is_pushed = models.BooleanField(_("حالة التلقي"))

    class Meta:
        db_table = 'Notification'
        verbose_name = 'إدارة الاشعارات'


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(_("موعد بدء العرض"))
    end_date = models.DateTimeField(
        _("موعد انتهاء العرض"))
    discount_rate = models.FloatField(_("قيمة الخصم"))
    is_active = models.BooleanField(_("Is Active"), default=True, blank=True)
    image = models.ImageField(
        _("صورة العرض"), upload_to="promotion-imag/", null=True, blank=True)

    def save(self, *args, **kwargs):
        # Update is_active based on current date
        current_date = timezone.now()
        # self.is_active = self.start_date <= current_date <= self.end_date

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'Promotion'
        verbose_name = 'إدارة العروض'


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self', on_delete=models.CASCADE, blank=True, related_name='children', null=True, default=0)
    name = models.CharField(_("اسم الصنف"), max_length=50)
    category_image = models.ImageField(
        _("صورة الصنف"), upload_to="category_image",)

    class MPTTMeta:
        # level_attr = 'parint'
        order_insertion_by = ['name']

    def __str__(self):
        return f" {self.name} مشتق من {self.parent.name} "

    # @property
    # def image_dimensions(self):
    #     """
    #     Get the dimensions of the category image.
    #     """

    #     img = Image.open(self.category_image.path)
    #     return img.size  # Return a tuple (width, height)

    # @image_dimensions.setter
    # def image_dimensions(self, dimensions):
    #     """
    #     Set the width of the category image.
    #     """
    #     self.image_width_field = dimensions[0]
    #     # Optionally, you may want to resize the image here

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = PImage.open(self.category_image.path)

        # Resize the image to the desired dimensions (200px width, 140px height)
        output_size = (200, 140)
        img.thumbnail(output_size)

        # Save the resized image
        img.save(self.category_image.path)

    class Meta:
        db_table = 'Category'
        verbose_name = 'إدارة لأصناف'


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name=_("الصنف"), related_name='category')
    name = models.CharField(_("اسم المنتج"), max_length=50, default="")
    price = models.DecimalField(
        _("سعر المنتج"), decimal_places=2, max_digits=8)
    description = models.TextField(_("وصف المنتج"))
    # image = models.ImageField(_("Image"), upload_to="products_image",)
    # promotion = models.ManyToManyField(
    #     Promotion, verbose_name=_("Promotions"), through='Promotion_product')

    def get_promotion(self):
        promotion = self.promotion_product.filter(
            is_active=True).first() or None
        return promotion.promotion.discount_rate if promotion else 0

    def get_new_price(self):
        promotion = self.promotion_product.filter(
            promotion__is_active=True).first()
        if promotion and promotion.promotion.is_active and promotion.promotion.discount_rate > 0:
            discount_rate = float(promotion.promotion.discount_rate)
            discounted_amount = (float(self.price) * discount_rate) / 100.0
            new_price = float(self.price) - discounted_amount
            # Round to 2 decimal places for currency
            return round(new_price, 2)
        else:
            return float(self.price)

    def get_qty_cart(self, user: User):
        if self.cart.get(user=user):
            return self.cart.get(user=user).qty
        else:
            return 0

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'Product'
        verbose_name = 'إدارة المنتجات'


class Promotion_product(models.Model):
    promotion = models.ForeignKey(
        Promotion, verbose_name=_("العرض"), on_delete=models.DO_NOTHING, related_name='promotion_product')
    product = models.ForeignKey(Product, verbose_name=_(
        "المنتج"), on_delete=models.DO_NOTHING, related_name='promotion_product')
    created_date = models.DateTimeField(
        _("تم الانشائ في "), auto_now=False, auto_now_add=True)
    updated_date = models.DateTimeField(
        _("اخر تعديل في"), auto_now=True, auto_now_add=False)
    is_active = models.BooleanField(_("حالة التفعيل"), default=True)

    class Meta:
        db_table = 'Promotion_Product'
        unique_together = ("product", "promotion")
        verbose_name = 'إدارة خصومات العروض'


class Image(models.Model):
    image = models.ImageField(_("الصورة"), upload_to="products_image",)
    product = models.ForeignKey(Product, verbose_name=_(
        "المنتج"), on_delete=models.CASCADE, related_name="image")

    class Meta:
        db_table = 'Product_image'

    def __str__(self) -> str:
        return self.product.name


class Review(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "المستخدم"), on_delete=models.CASCADE, related_name='review')
    product = models.ForeignKey(Product, verbose_name=_(
        "المنتج"), on_delete=models.CASCADE, related_name='review')
    review_date = models.DateTimeField(auto_now_add=True)
    review_text = models.TextField()

    class Meta:
        db_table = 'Review'
        verbose_name = 'إدارة التعليقات'


class Review_Likes(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='review_likes')
    review = models.ForeignKey(Review, verbose_name=_(
        "Review"), on_delete=models.CASCADE, related_name='review_likes')

    class Meta:
        db_table = 'Review_Likes'
        unique_together = ("review", "user")
        verbose_name = 'إدارة اعجابات المستخدمين'


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "المستخدم"), on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, verbose_name=_(
        "المنتج"), on_delete=models.CASCADE, related_name='cart')
    qty = models.IntegerField(_("الكمية"), default=1)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        unique_together = ("product", "user")


class Favorite(models.Model):
    """
    Favorite model <ManyTOMany> betowen User and Prodect
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='favorites')
    time_created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Product- {self.product.id } - User- {self.user.id}"

    class Meta:
        db_table = 'Favorite'
        unique_together = ("product", "user")


class Rate(models.Model):
    rating_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    rating_no = models.FloatField(_("التقييم"), max_length=5, default=0.0)
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE, related_name='rate')
    product = models.ForeignKey(Product, verbose_name=_(
        "Product"), on_delete=models.CASCADE, related_name='rate')

    class Meta:
        db_table = 'Rate'
        unique_together = ("product", "user")
        verbose_name = 'إدارة تقييمات المستخدمين'


class City(models.Model):
    name = models.CharField(_("اسم المدينة"), max_length=50)
    is_active = models.BooleanField(_("تفعيل المدينة"), default=True)

    class Meta:
        db_table = 'City'
        verbose_name = 'إدارة المحافضات والمدن'

    def __str__(self) -> str:
        return str(self.name)


class Currency (models.Model):
    currency_name = models.CharField(_("اسم العملة"), max_length=50)
    conversion_factor = models.DecimalField(
        _("Conversion Factor (معامل التحويل)"), max_digits=12, decimal_places=2)
    is_active = models.BooleanField(_("تفعيل العملة"), default=True)

    class Meta:
        db_table = 'Currency'
        verbose_name = 'إدارة العملات'

    def __str__(self) -> str:

        return str(self.currency_name)


class Payment_type(models.Model):
    name = models.CharField(_("اسم طريقة الدفع"), max_length=50)
    is_active = models.BooleanField(_("تفعيل طريقة الدفع"), default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Payment_type'
        verbose_name = 'إدارة طرق الدفع'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "المستخدم"), on_delete=models.DO_NOTHING, related_name='order')
    city = models.ForeignKey(City, verbose_name=_(
        "المدينة"), on_delete=models.DO_NOTHING, related_name='order')
    currency = models.ForeignKey(Currency, verbose_name=_(
        "العملة"), on_delete=models.DO_NOTHING, related_name='order',)
    proof_of_payment_image = models.ImageField(
        _("صورة اثبات الدفع"), upload_to="proof_of_payment_image", blank=True, null=True)
    payment_type = models.ForeignKey(Payment_type, verbose_name=_(
        "طريقة الدفع"), on_delete=models.DO_NOTHING)
    customer_name = models.CharField(
        _("اسم العميل"), max_length=100, blank=True, null=True)
    customer_phone = models.CharField(
        _("رقم هاتف العميل"), max_length=50)
    customer_phone2 = models.CharField(
        _("رقم هاتف بديل"), max_length=50, null=True, blank=True)
    total_paid = models.DecimalField(
        _("اجمالي المدفوع"), max_digits=12, decimal_places=2, blank=True, null=True, default=0.0)
    date = models.DateTimeField(_("Date"), auto_now=False, auto_now_add=True)
    is_delivered = models.BooleanField(
        _("حالة التوصيل"), default=False, blank=True)
    address = models.TextField(_("العنوان"), blank=True, default="")
    is_proof = models.BooleanField(_("حالة الاثبات"), default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.customer_name = self.user.name
        if self.proof_of_payment_image and not self.is_proof:
            self.is_proof = True
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'Order'
        verbose_name = 'إدارة الطلبات'


class Order_item(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(
        "المنتج"), on_delete=models.DO_NOTHING, related_name="order_item")
    order = models.ForeignKey(Order, verbose_name=_(
        "الطلب"), on_delete=models.DO_NOTHING, related_name="order_item")
    qty = models.IntegerField(_("الكمية"))
    date = models.DateTimeField(_("Date"), auto_now=False, auto_now_add=True)
    price = models.DecimalField(
        _("السعر"), decimal_places=2, max_digits=12, blank=True)
    total_price = models.DecimalField(
        _("السعر الاجمالي"), decimal_places=2, max_digits=12, blank=True, editable=False,)

    def save(self, *args, **kwargs):
        # Calculate the total price based on the quantity and price of the product
        self.qty = self.product.get_qty_cart(self.order.user)
        self.price = self.product.get_new_price()
        self.total_price = self.qty * self.price
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"المنتج {self.product.name} الكمية {self.qty}"

    class Meta:
        db_table = 'Order_item'


# ------------------------- Signals ------------------
@receiver(post_save, sender=Promotion_product)
def send_promotion_notification(sender, instance, created, **kwargs):
    """
    Signal handler to send notifications when a promotion is added for a product.
    """
    if created:
        try:
            users = User.objects.all()
            notification_text = f"New promotion '{instance.promotion.name}' added for product '{instance.product.name}'."

            with transaction.atomic():
                for user in users:
                    Notification.objects.create(
                        title="New Promotion Added",
                        text=notification_text,
                        user=user,
                    )
        except ObjectDoesNotExist:
            pass
