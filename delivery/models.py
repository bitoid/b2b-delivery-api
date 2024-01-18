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
