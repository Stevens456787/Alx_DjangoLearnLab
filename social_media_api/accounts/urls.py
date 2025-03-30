from django.urls import path
from .views import register, login, follow_user, unfollow_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
]