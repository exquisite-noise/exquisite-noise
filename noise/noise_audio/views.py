from .models import Audio
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class NewStoryForm(LoginRequiredMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    fields = ['topic', 'path']
    
    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        # import pdb; pdb.set_trace()
        return kwargs

    def form_valid(self, form):
        """Validate form."""
        form.instance.creator = self.request.user
        form.save()
        form.instance.contributor.add(self.request.user)
        # import pdb; pdb.set_trace()
        return super().form_valid(form)

