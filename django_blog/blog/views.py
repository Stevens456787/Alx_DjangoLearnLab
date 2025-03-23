from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import PostForm
from taggit.models import Tag
from .forms import CommentForm

# Display all blog posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]  # Display latest posts first

# Show individual blog post details
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

# Create a new post (Only for logged-in users)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Assign the logged-in user as the author
        return super().form_valid(form)

# Update an existing post (Only the author can edit)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    form_class = PostForm
    template_name = "blog/post_form.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  # Allow only the post author to edit

# Delete a post (Only the author can delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")  # Redirect to post list after deletion

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author # Allow only the post author to delete

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'  # Ensure you have this template

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])  # Link to the post
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user  # Only allow owners to edit

    def get_success_url(self):
        return self.object.post.get_absolute_url()

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user  # Only allow owners to delete

    def get_success_url(self):
        return self.object.post.get_absolute_url()
    

def search_posts(request):
    query = request.GET.get('q')
    results = []
    
    if query:
        results = Post.objects.filter(
            title__icontains=query
        ) | Post.objects.filter(
            tags__name__icontains=query
        ) | Post.objects.filter(
            content__icontains=query
        ).distinct()

    return render(request, 'blog/search_results.html', {'results': results, 'query': query})


class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Change this to your template
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags__in=[tag])