from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers  # Import serializers from DRF
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'This username is already taken.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already associated with an existing account.'})

        return attrs

    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']
