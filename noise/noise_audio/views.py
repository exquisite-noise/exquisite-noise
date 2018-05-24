from .models import Audio, AudioAdd
from django.conf import settings
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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

        prev_object = Audio.objects.filter(id=self.kwargs['clip_id']).first()
        prev_path = settings.BASE_DIR + prev_object.audio_file.url

        audio_prev = open(prev_path, 'rb').read()
        audio_new = open(new_path, 'rb').read()
        audio_join = audio_prev + audio_new
        audio_final = open(prev_path, 'wb').write(audio_join)

        return audio_final

    def get_form_kwargs(self):
        """Get form kwargs."""
        kwargs = super().get_form_kwargs()
        kwargs['clip_id'] = self.kwargs['clip_id']
        return kwargs

    def post(self, request, *args, **kwargs):
<<<<<<< HEAD
        """Replace post method."""
        filename = "story.mp3" # received file name
        file_obj = request.FILES['audio_file']
        with default_storage.open(settings.MEDIA_ROOT + filename, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        new_clip_path = settings.MEDIA_ROOT + filename

        record = Audio.objects.filter(id=self.kwargs['clip_id']).first()
        story = settings.MEDIA_ROOT + record.audio_file.url

        # new_clip = request.FILES['audio_file']
        # print('****', new_clip)
        # new_clip_path = str(os.path.join(settings.MEDIA_ROOT, new_clip))
        # print(new_clip)

        story = concat_clips(story, new_clip_path)
        return
=======
        """Adding to post method."""
        kwargs.pop('clip_id')
        return super().post(request, *args, **kwargs)
>>>>>>> 40371eb843865c352e9be1fe5402797617f3d504

    def get_context_data(self, **kwargs):
        """Customize context data."""
        context = super().get_context_data(**kwargs)
        context['story'] = Audio.objects.get(id=self.kwargs['clip_id'])
        return context
