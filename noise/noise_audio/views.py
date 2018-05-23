from django.shortcuts import render
from pydub import AudioSegment
import os
from .models import Audio
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from .convert import convert
from .concat import concat_clips
from audio_recorder.views import AudioFileCreateViewMixin
from .forms import AudioFileForm, AudioAddForm


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

    # def form_valid(self, form):
    #     """Validate form."""
    #     import pdb; pdb.set_trace()
    #     form.instance.creator = self.request.user
    #     form.save()
    #     form.instance.contributor.add(self.request.user)
    #     return super().form_valid(form)


class ContinueStoryForm(LoginRequiredMixin, AudioFileCreateViewMixin, UpdateView):
    """Add to existing story."""

    template_name = 'noise_audio/add_clip.html'
    model = Audio
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('auth_login')
    form_class = AudioAddForm
    context_object_name = 'story'
    pk_url_kwarg = 'clip_id'

    def create_object(self, audio_file):
        """
        Combine the unfinished story with an additional clip and update in the database.

        This function overwrites the function in the AudioFileCreateViewMixin.
        """
        import pdb; pdb.set_trace()
        record = Audio.objects.filter(id=self.kwargs['clip_id']).first()
        story = 'noise' + record.audio_file.url
        updated_story = concat_clips(story, audio_file)

        record.audio_file.file = SimpleUploadedFile(
            name='test.mp3',
            content=updated_story.read(),
            content_type='audio/mpeg'
            )
        record.save()
        return record

    def post(self, request, *args, **kwargs):
    #     """Replace post method."""
    #     # new_clip = request.FILES.get('audio_file', None)
    #     # import pdb; pdb.set_trace()
    #     # record = Audio.objects.filter(id=kwargs.pop('clip_id')).first()
        kwargs.pop('clip_id')
    #     # story = 'noise' + record.audio_file.url
    #     # updated_story = concat_clips(story, new_clip)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super().get_context_data(**kwargs)
        return context

    # def form_valid(self, form):
    #     """Validate form."""
    #     # import pdb; pdb.set_trace()
    #     form.instance.creator = self.request.user
    #     prev_clip = form.instace.path

    #     new_clip = form.instance.concat_file
    #     form.instance.concat_file = concat_clips(prev_clip, new_clip)

    #     form.instance.contributor.add(self.request.user)
    #     form.save()
    #     return super().form_valid(form)
