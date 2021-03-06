import os
from .models import Audio, AudioAdd
from django.conf import settings
from django.views.generic import CreateView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from audio_recorder.views import AudioFileCreateViewMixin
from .forms import AudioFileForm, AudioAddForm
from pydub import AudioSegment


class NewStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    form_class = AudioFileForm
    success_url = reverse_lazy('link')
    login_url = reverse_lazy('auth_login')

    def create_object(self, audio_file):  # pragma: no cover
        """
        Create the audio model instance and save in database.

        This function overwrites the function in the AudioFileCreateViewMixin.
        """
        new = Audio.objects.create(**{
          self.create_field: audio_file,
          'topic': self.request.POST['topic'],
          'creator': self.request.user,
          })
        new.contributor.add(self.request.user)

        return new

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        return kwargs


class ContinueStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, CreateView):
    """Add to existing story."""

    template_name = 'noise_audio/add_clip.html'
    model = AudioAdd
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    form_class = AudioAddForm
    context_object_name = 'story'
    pk_url_kwargs = 'clip_id'

    def create_object(self, audio_file):  # pragma: no cover
        """
        Combine the unfinished story with an additional clip and update in the database.

        This function overwrites the function in the AudioFileCreateViewMixin.
        """
        new = AudioAdd.objects.create(**{
            self.create_field: audio_file,
            'pk_master': Audio.objects.get(id=self.kwargs['clip_id']),
            'user': self.request.user,
        })
        new.pk_master.contributor.add(self.request.user)
        new.save()

        # concat clips
        new_object = AudioAdd.objects.filter(pk_master=self.kwargs['clip_id']).last()
        new_path = new_object.audio_file.path

        prev_object = Audio.objects.filter(id=self.kwargs['clip_id']).first()
        prev_path = prev_object.audio_file.path

        with open(prev_path, 'rb') as f:
            audio_prev = f.read()

        with open(new_path, 'rb') as f:
            audio_new = f.read()

        audio_join = audio_prev + audio_new

        with open(prev_path, 'wb') as f:
            audio_final = f.write(audio_join)

        return audio_final

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs['clip_id'] = self.kwargs['clip_id']
        return kwargs

    def post(self, request, *args, **kwargs):  # pragma: no cover
        """Adding to post method."""
        kwargs.pop('clip_id')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Customize context data."""
        context = super().get_context_data(**kwargs)
        context['story'] = Audio.objects.get(id=self.kwargs['clip_id'])
        snippet = AudioSegment.from_file(context['story'].audio_file.path)[-5000:]
        snippet_root = os.path.join(settings.MEDIA_ROOT, 'snippets')
        try:
            os.mkdir(snippet_root)
        except IOError:
            pass
        snippet.export(os.path.join(snippet_root, context['story'].audio_file.name))
        context['snippet_url'] = '{}snippets/{}'.format(
            settings.MEDIA_URL, context['story'].audio_file.name)
        return context


class LinkView(TemplateView):
    """View for link to share story."""

    template_name = 'noise_audio/link.html'
    model = Audio

    def get_context_data(self, **kwargs):
        """Customize context data."""
        context = super().get_context_data(**kwargs)
        id = Audio.objects.all().last().id
        context['story_link'] = 'https://{}/audio/add/{}'.format(self.request.META['HTTP_HOST'], id)
        context['story_id'] = id
        context['story_topic'] = Audio.objects.all().last().topic
        return context


class DetailStoryView(DetailView):
    """Detail of a story."""

    template_name = 'noise_audio/detail.html'
    context_object_name = 'story'

    def get_object(self):
        """Get object."""
        return Audio.objects.filter(id=self.kwargs['clip_id']).first()

    def get_context_data(self, **kwargs):
        """Customize context data."""

        context = super().get_context_data(**kwargs)
        context.update({'host': self.request.META['HTTP_HOST']})
        return context
