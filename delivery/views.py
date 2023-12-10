from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Client, Courier, Order
from .serializers import ClientSerializer, CourierSerializer, OrderSerializer, UserSerializer
from .permissions import IsSuperuser, IsClient, IsCourier

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuser]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsSuperuser | IsClient]

class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsSuperuser | IsCourier]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsSuperuser | IsClient | IsCourier]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'client'):
            serializer.save(client=self.request.user.client)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_type": "admin" if user.is_superuser else "client" if hasattr(user, 'client') else "courier" if hasattr(user, 'courier') else "unknown"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
