from django import forms
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
