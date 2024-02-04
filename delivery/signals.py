from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User

@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        previous = Order.objects.get(pk=instance.pk)
        if instance.status != previous.status:
            instance._status_changed = True

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    admin_users = User.objects.filter(is_superuser=True)
    if created:
        for admin in admin_users:
            Notification.objects.create(
                notification_type='order_added',
                admin_user=admin,
                order=instance
            )
    else:
        if hasattr(instance, '_status_changed') and instance._status_changed:
            for admin in admin_users:
                Notification.objects.create(
                    notification_type='status_updated',
                    admin_user=admin,
                    order=instance
                )
        else:
            for admin in admin_users:
                Notification.objects.create(
                    notification_type='order_updated',
                    admin_user=admin,
                    order=instance
            )
