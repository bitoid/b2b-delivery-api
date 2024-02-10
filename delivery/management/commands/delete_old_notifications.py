from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from delivery.models import Notification

class Command(BaseCommand):
    help = 'Deletes notifications that are 2 days old or older'

    def handle(self, *args, **options):
        # Calculate the date 2 days ago from now
        two_days_ago = timezone.now() - timedelta(days=2)

        old_notifications = Notification.objects.filter(created_at__lte=two_days_ago)
        count = old_notifications.count()
        old_notifications.delete()

        self.stdout.write(self.style.SUCCESS(f'წარმატებით წაიშალა {count} ძველი შეტყობინება'))
