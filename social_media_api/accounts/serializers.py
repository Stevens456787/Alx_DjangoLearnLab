from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


User = get_user_model() 

class UseSerializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'bio', 'profile_picture','followers']
        

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        User = get_user_model()  # Explicitly call get_user_model
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Create a token for the new user
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user:
            return {'user': user}
        raise serializers.ValidationError("Invalid credentials")