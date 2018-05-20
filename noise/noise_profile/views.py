from django.views.generic import ListView
from .models import NoiseProfile


class ProfileView(ListView):
    """Profile view."""

    template_name = 'noise_profile/profile.html'

    def get(self, *args, **kwargs):
        """Get."""
        return super().get(*args, **kwargs)

    def get_queryset(self):
        """Get queryset."""
        pass
