from django.urls import path, include
from rest_framework.routers import DefaultRouter
from delivery.views import ClientViewSet, CourierViewSet, OrderViewSet, UserViewSet, LoginView, ExcelUploadView
from django.contrib import admin
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'couriers', CourierViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/upload-excel/', ExcelUploadView.as_view(), name='upload-excel'),
]

urlpatterns += doc_urls