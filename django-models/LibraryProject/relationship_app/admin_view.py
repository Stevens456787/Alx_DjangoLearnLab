# relationship_app/admin_view.py
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render

def check_admin(user):
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(check_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin.html', {
        'message': 'Welcome to the Admin Dashboard'
    })