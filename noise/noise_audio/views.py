from django.shortcuts import render
from pydub import AudioSegment
import os
from .models import Audio, AudioAdd
from django.conf import settings
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from .convert import convert
from .concat import concat_clips
from audio_recorder.views import AudioFileCreateViewMixin
from .forms import AudioFileForm, AudioAddForm

import ffmpeg


class NewStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, CreateView):
    """Add new story."""

    template_name = 'noise_audio/new_story.html'
    model = Audio
    form_class = AudioFileForm
    success_url = reverse_lazy('add')
    login_url = reverse_lazy('auth_login')

    def create_object(self, audio_file):
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

    def create_object(self, audio_file):
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
        new_path = settings.BASE_DIR + new_object.audio_file.url
        # new_path = os.path.join(settings.MEDIA_ROOT, new_object.audio_file.url)
        # print(new_object.audio_file.url)
        # print(settings.BASE_DIR)
        # print(new_path)
        # new_path = '/Users/brandonholderman/Codefellows/python/exquisite-noise/noise/MEDIA/temp/story_Dru1dZI.mp3'

        prev_object = Audio.objects.filter(id=self.kwargs['clip_id']).first()
        prev_path = settings.BASE_DIR + prev_object.audio_file.url

        audio_prev = open(prev_path, 'rb').read()
        audio_new = open(new_path, 'rb').read()

        audio_join = audio_prev + audio_new
        # os.remove(prev_path)
        audio_final = open(prev_path, 'wb').write(audio_join)

        return audio_final
        # concatenated_clip = concat_clips(prev_path, new_path)

        # with open(prev_path, 'wb') as f:
        #     f.write(concatenated_clip.read())

        # return new

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['clip_id'] = self.kwargs['clip_id']
        return kwargs

    def post(self, request, *args, **kwargs):
        """Replace post method."""
        kwargs.pop('clip_id')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        context['story'] = Audio.objects.get(id=self.kwargs['clip_id'])
        return context
