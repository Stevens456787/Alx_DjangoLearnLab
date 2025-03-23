from django import forms
from .models import Post
from .models import Comment
from taggit.forms import TagWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={'class': 'form-control', "rows": 3}),
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets = {
            "tags": TagWidget(),
        }
        
class RegistrationsForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password"]
