from django.contrib import admin
from .models import Client, Courier, Order, Notification

admin.site.register(Client)
admin.site.register(Courier)
admin.site.register(Order)
admin.site.register(Notification)