from django.db import models
from django.utils import timezone

class Client(models.Model):
    name = models.CharField(max_length=255)
    representative_name = models.CharField(max_length=255)
    representative_surname = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=50)
    addresses = models.TextField()

    def __str__(self):
        return self.name

class Courier(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Order(models.Model):
    GREEN = 'GR'
    YELLOW = 'YL'
    RED = 'RD'
    BLACK = 'BK'

    ORDER_STATUS_CHOICES = [
        (GREEN, 'Delivered'),
        (YELLOW, 'Delivery Failed - Will Retry'),
        (RED, 'Cannot be Delivered'),
        (BLACK, 'Refund'),
    ]

    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default=GREEN)
    addressee_full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    comment = models.TextField(blank=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    courier_fee = models.DecimalField(max_digits=10, decimal_places=2)
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_orders')
