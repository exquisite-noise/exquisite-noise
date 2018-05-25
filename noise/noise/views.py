from django.views.generic import TemplateView, DetailView
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


# class ProfileView(DetailView):
#     """Detail of a profile."""

#     template_name = 'generic/profile.html'
#     context_object_name = 'profile'

#     def get_object(self):
#         """Get object."""
#         return Audio.objects.filter(creator__username=username).first()

#     def get_context_data(self, **kwargs):
#         """Customize context data."""
#         context = super().get_context_data(**kwargs)
#         return context


class AboutUsView(TemplateView):
    """About Us view class."""

    template_name = 'generic/about-us.html'

    # def get_context_data(self, **kwargs):
    #     """Get context."""
    #     context = super().get_context_data(**kwargs)

    #     context['beverly'] = 'static/beverly.png'
    #     context['brandon'] = 'static/brandon.jpg'
    #     context['tyler'] = 'static/tyler.jpg'
    #     # context['github'] = 'static/githubicon.png'
    #     context['linkedin'] = 'static/linkedinicon.png'

    #     return context
