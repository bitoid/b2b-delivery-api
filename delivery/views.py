from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Client, Courier, Order
from .serializers import ClientSerializer, CourierSerializer, OrderSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAdminUser]

class CourierViewSet(viewsets.ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [permissions.IsAdminUser]

# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     permission_classes = [IsSuperuser | IsClient]

# class CourierViewSet(viewsets.ModelViewSet):
#     queryset = Courier.objects.all()
#     serializer_class = CourierSerializer
#     permission_classes = [IsSuperuser | IsCourier]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

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
            user_data = UserSerializer(user).data

            if user.is_superuser:
                user_type = "admin"
                user_data['profile'] = "Admin User"
            elif hasattr(user, 'client'):
                user_type = "client"
                client_data = ClientSerializer(user.client).data
                user_data['profile'] = client_data
            elif hasattr(user, 'courier'):
                user_type = "courier"
                courier_data = CourierSerializer(user.courier).data
                user_data['profile'] = courier_data
            else:
                user_type = "unknown"

            return Response({"token": token.key, "user_type": user_type, "user_data": user_data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
