from rest_framework import serializers
from .models import Client, Courier, Order, Notification
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'user', 'name', 'representative_full_name', 'phone_number', 'addresses', 'role']

    def get_role(self, obj):
        return "client"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        client = Client.objects.create(user=user, **validated_data)
        return client

class CourierSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = '__all__'

    def get_role(self, obj):
        return "courier"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        courier = Courier.objects.create(user=user, **validated_data)
        return courier


class OrderSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request_user = self.context['request'].user 
        if request_user.is_superuser or (instance.courier and request_user == instance.courier.user):
            ret['status'] = instance.status if instance.status_approved else 'Pending Approval'
        else:
            ret['status'] = instance.status if instance.status_approved else 'DF'
        return ret


    def get_client_name(self, obj):
        if obj.client:
            return obj.client.name
        return None

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'