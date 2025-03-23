from django import forms
from .models import Post
from .models import Comment
from taggit.forms import TagWidget
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