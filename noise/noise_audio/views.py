from django.shortcuts import render
from pydub import AudioSegment
import os
from .models import Audio
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .convert import convert
from .concat import concat_clips
from audio_recorder.views import AudioFileCreateViewMixin
from .forms import AudioFileForm


class NewStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    form_class = AudioFileForm
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')

    def create_object(self, audio_file):
        """Create the audio model instance and save in database. This function overwrites the function in the AudioFileCreateViewMixin."""
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

    # def form_valid(self, form):
    #     """Validate form."""
    #     import pdb; pdb.set_trace()
    #     form.instance.creator = self.request.user
    #     form.save()
    #     form.instance.contributor.add(self.request.user)
    #     return super().form_valid(form)


class ContinueStoryForm(LoginRequiredMixin, UpdateView):
    """Add to existing story."""

    template_name = 'noise_audio/add_clip.html'
    model = Audio
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    fields = ['path', 'concat_path']
    context_object_name = 'story'
    slug_url_kwarg = 'clip_id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """Validate form."""
        # import pdb; pdb.set_trace()
        form.instance.creator = self.request.user

        new_clip = form.instance.concat_path
        form.instance.concat_path = concat_clips(form.instance.path,
                                                 convert(new_clip))

        form.instance.contributor.add(self.request.user)
        form.save()
        return super().form_valid(form)
