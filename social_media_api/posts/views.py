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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user == user_to_follow:
        return Response({'detail': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Add the user to the following list
    user.following.add(user_to_follow)
    user_to_follow.followers.add(user)

    return Response({'detail': 'Followed successfully'}, status=status.HTTP_200_OK)

#unfollow user function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user = request.user

    if user == user_to_unfollow:
        return Response({'detail': 'You cannot unfollow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    # Remove the user from the following list
    user.following.remove(user_to_unfollow)
    user_to_unfollow.followers.remove(user)

    return Response({'detail': 'Unfollowed successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    # user = CustomUser
    user = request.user    
    # Get posts from the users the current user is following
    followed_users = user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)