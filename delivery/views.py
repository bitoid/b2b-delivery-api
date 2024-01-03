from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Client, Courier, Order
from .serializers import ClientSerializer, CourierSerializer, OrderSerializer, UserSerializer
from .permissions import IsSuperuser, IsOwnerOrReadOnly
from .filters import OrderFilter
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

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

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        elif hasattr(user, 'client'):
            return Order.objects.filter(client=user.client)
        elif hasattr(user, 'courier'):
            return Order.objects.filter(courier=user.courier)
        else:
            return Order.objects.none()

    def get_permissions(self):
        if self.request.user.is_superuser:
            return [permissions.IsAuthenticated()]


        if self.action == 'destroy':
            return [IsSuperuser()]
        elif self.action in ['list', 'create', 'retrieve']:
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwnerOrReadOnly()]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'client'):
            serializer.save(client=self.request.user.client)
        elif self.request.user.is_superuser:
            serializer.save()

    def perform_update(self, serializer):
        if hasattr(self.request.user, 'courier'):
            instance = serializer.instance
            instance.comment = serializer.validated_data.get('comment', instance.comment)
            instance.status = serializer.validated_data.get('status', instance.status)
            instance.save()
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['delete'], detail=False, url_path='delete-batch', permission_classes=[IsSuperuser])
    def delete_batch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        order_ids = request.data.get('ids', [])
        if not order_ids:
            return Response({'detail': 'No order IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        Order.objects.filter(id__in=order_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data

            if user.is_superuser:
                user_data['profile'] = "Admin User"
                user_data['user_type'] = "admin"
            elif hasattr(user, 'client'):
                client_data = ClientSerializer(user.client).data
                user_data['profile'] = client_data
                user_data['user_type'] = "client"
            elif hasattr(user, 'courier'):
                courier_data = CourierSerializer(user.courier).data
                user_data['profile'] = courier_data
                user_data['user_type'] = "courier"
            else:
                user_data['user_type'] = "unknown"

            return Response({"token": token.key, "user_data": user_data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)
