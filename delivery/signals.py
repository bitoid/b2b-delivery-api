from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User

@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    if instance.pk:
        previous_instance = Order.objects.get(pk=instance.pk)
        if instance.status != previous_instance.status:
            instance._status_changed = True
        if instance.staged_status != previous_instance.staged_status:
            instance._staged_status_changed = True

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
        if hasattr(instance, '_staged_status_changed') and instance._staged_status_changed:
            for admin in admin_users:
                notification, _ = Notification.objects.update_or_create(
                    notification_type='status_updated',
                    order=instance,
                    defaults={
                        'admin_user': admin,
                        'new_status': instance.staged_status,
                        'is_read': False
                    }
                )
        elif hasattr(instance, '_status_changed') and instance._status_changed:
            for admin in admin_users:
                Notification.objects.create(
                    notification_type='status_updated',
                    admin_user=admin,
                    order=instance,
                    new_status=instance.status
                )
        else:
            for admin in admin_users:
                Notification.objects.update_or_create(
                    notification_type='order_updated',
                    order=instance,
                    defaults={'admin_user': admin, 'is_read': False}
                )
