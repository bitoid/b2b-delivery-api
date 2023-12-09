from django.contrib import admin
from .models import Client, Courier, Order

admin.site.register(Client)
admin.site.register(Courier)
admin.site.register(Order)
