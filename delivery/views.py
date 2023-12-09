from rest_framework import viewsets, permissions
from .models import Client, Courier, Order
from django.contrib.auth.models import User
from .serializers import ClientSerializer, CourierSerializer, OrderSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
