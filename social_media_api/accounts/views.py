from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token  # Fixed typo in import
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')

CustomUser = get_user_model()

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]
    
    
    # Fixed typo (IsAuthenticated)
    
    @permissions.IsAuthenticated

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Fixed typo (data-request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'user': serializer.data}, status=status.HTTP_201_CREATED)  # Fixed quote
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)  # Fixed bracket
        return Response({'error': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)  # Fixed bracket and quote

class UserListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]  # Fixed brackets
        return Response(user_data, status=status.HTTP_200_OK)

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_to_follow_id = kwargs.get('user_id')
        try:
            user_to_follow = CustomUser.objects.get(id=user_to_follow_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.user.following.filter(id=user_to_follow_id).exists():
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_to_unfollow_id = kwargs.get('user_id')
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_to_unfollow_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.following.filter(id=user_to_unfollow_id).exists():
            return Response({'error': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)