from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Home view class."""

    template_name = 'generic/home.html'
