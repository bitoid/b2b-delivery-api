from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    representative_full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    addresses = models.TextField()

    def __str__(self):
        return self.name

class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    GREEN = 'GR'
    YELLOW = 'YL'
    RED = 'RD'
    BLACK = 'BK'
    DEFAULT = 'DF'

    ORDER_STATUS_CHOICES = [
        (DEFAULT, 'DEFAULT'),
        (GREEN, 'GREEN'),
        (YELLOW, 'YELLOW'),
        (RED, 'RED'),
        (BLACK, 'BLACK'),
    ]

    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=DEFAULT)
    staged_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='DF', blank=True)
    status_approved = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    addressee_full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    courier_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
    order_position = models.IntegerField(default=0)

    class Meta:
        ordering = ['order_position']


class Notification(models.Model):
    TYPE_CHOICES = [
        ('order_added', 'Order Added'),
        ('order_updated', 'Order Updated'),
        ('status_updated', 'Status Updated'),
    ]
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - Order ID: {self.order.id}"
