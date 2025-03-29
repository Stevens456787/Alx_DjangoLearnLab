from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers')
        read_only_fields = ('followers',)

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture')
        extra_kwargs = {
            'password': {'write_only': True},
            'bio': {'required': False},
            'profile_picture': {'required': False}
        }

    def create(self, validated_data):
        # Create the user with create_user to properly hash the password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        # Create an auth token for the new user
        Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            # Get or create token for authenticated user
            token, created = Token.objects.get_or_create(user=user)
            return {'user': user, 'token': token}
        raise serializers.ValidationError("Incorrect Credentials")