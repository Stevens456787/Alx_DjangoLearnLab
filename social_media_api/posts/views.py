from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import generics, get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from accounts.models import CustomUser
from notifications.models import Notification

class UserFeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Get posts from the users the current user is following
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    def get(self, request):
        # Use the get_queryset method to get the filtered posts
        posts = self.get_queryset()

        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)