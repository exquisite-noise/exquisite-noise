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



# class HomeView(TemplateView):
#     """Renders home view."""
#     template_name = 'generic/home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         photos = Photo.objects.filter(published='PUBLIC')

#         if photos.count():
#             image = photos.order_by('?').first()
#             image_url = image.image.url
#             image_title = image.title

#         else:
#             image = None
#             image_url = 'http://via.placeholder.com/250x250'
#             image_title = 'Placeholder'

#         context['image'] = image
#         context['image_url'] = image_url
#         context['image_title'] = image_title

#         return context
