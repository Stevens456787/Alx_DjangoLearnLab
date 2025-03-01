from django.http import HttpResponseForbidden
from functools import wraps

def admin_required(view_func):
    """Decorator to restrict access to Admin users only."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'userprofile'):
            if request.user.userprofile.role == 'Admin':
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page.")
    return _wrapped_view
