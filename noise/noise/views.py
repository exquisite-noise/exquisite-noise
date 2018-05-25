from django.views.generic import TemplateView, ListView
from noise_audio.models import Audio


class HomeView(TemplateView):
    """Home view class."""

    template_name = 'generic/home.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        """Customize context."""
        context = super().get_context_data(**kwargs)

        clips = Audio.objects.all()[:3]

        context = {
            'clips': clips,
        }

        return context


class ProfileView(ListView):
    """Detail of a profile."""

    template_name = 'generic/profile.html'
    context_object_name = 'profile'

    def get_queryset(self):
        """Get object."""
        return Audio.objects.filter(creator=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        """Customize context data."""
        context = super().get_context_data(**kwargs)
        return context


class AboutUsView(TemplateView):
    """About Us view class."""

    template_name = 'generic/about-us.html'
