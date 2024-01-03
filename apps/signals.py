from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import Promotion_product, User, Notification


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
