from django.shortcuts import render

# Create your views here.
# notifications/views.py
from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications.all()

# posts/views.py - Add to PostViewSet
@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if created:
        # Create notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
    return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

@action(detail=True, methods=['post'])
def unlike(self, request, pk=None):
    post = self.get_object()
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)