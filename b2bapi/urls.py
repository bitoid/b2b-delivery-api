from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from delivery import views

router = DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'couriers', views.CourierViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
