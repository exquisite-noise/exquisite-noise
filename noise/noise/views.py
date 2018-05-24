from django.views.generic import TemplateView
from noise_audio.models import Audio


class HomeView(TemplateView):
    """Home view class."""

    template_name = 'generic/home.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clips = Audio.objects.all()

        context = {
            'clips': clips,
        }

        return context
