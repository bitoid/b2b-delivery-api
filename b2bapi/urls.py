from django.urls import path, include
from rest_framework.routers import DefaultRouter
from delivery.views import ClientViewSet, CourierViewSet, OrderViewSet, UserViewSet, LoginView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'couriers', CourierViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
]
