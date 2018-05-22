from .models import Audio
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from audio_recorder.views import AudioFileCreateViewMixin
from .forms import AudioFileForm


class NewStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    form_class = AudioFileForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    # fields = ['topic', 'path']

    # def post(self, request, *args, **kwargs):
    #   import pdb; pdb.set_trace()
    #   return super().post(request, *args, **kwargs)

    def create_object(self, audio_file):
        # import pdb; pdb.set_trace()
        #  create your model instance
        new = Audio.objects.create(**{
          self.create_field: audio_file,
          'topic': self.request.POST['topic'],
          'creator': self.request.user,
          # 'contributor': self.request.user,
          })
        new.contributor.add(self.request.user)

        return new  # new model instance

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        """Validate form."""
        import pdb; pdb.set_trace()
        form.instance.creator = self.request.user
        form.save()
        form.instance.contributor.add(self.request.user)
        return super().form_valid(form)

