from django import forms
from django.urls import reverse
from audio_recorder.widgets import AudioFileWidget
from .models import Audio


class AudioFileForm(forms.ModelForm):
    """Audio File Form."""

    class Meta:
        """Meta."""

        model = Audio
        fields = ['topic', 'path']
        widgets = {
            'path': AudioFileWidget(url='new'),
        }


class AudioAddForm(forms.ModelForm):
    """Audio Add Form."""

    class Meta:
        """Meta."""

        model = Audio
        fields = ['path']
        widgets = {
            'path': AudioFileWidget(),
        }

    def __init__(self, *args, **kwargs):
        # clip_id = kwargs['instance'].id
        clip_id = kwargs.pop('clip_id')
        super().__init__(*args, **kwargs)
        self.fields['path'].widget.attrs['data-url'] = reverse('add', kwargs={'clip_id': clip_id})
        self.fields['path'].widget.attrs['data-django-audio-recorder'] = True
