from django.shortcuts import render, get_object_or_404  # Import get_object_or_404

# Create your views here.
from rest_framework import viewsets, permissions, filters
from .models import Post, Comment, Like, Notification  # Import Like and Notification models
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Fetch the post using get_object_or_404
        post = get_object_or_404(Post, pk=pk)
        
        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # Create a notification for the post author
            Notification.objects.create(
                user=post.author,
                message=f"{request.user.username} liked your post '{post.title}'."
            )
            return Response({"message": "Post liked successfully."}, status=201)
        else:
            return Response({"message": "You have already liked this post."}, status=400)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)