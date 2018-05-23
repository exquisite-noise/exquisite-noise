import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from pydub import AudioSegment


def convert(clip):
    """
    Convert files to mp3 and saves in media directory.
    """
    og_clip = AudioSegment.from_file(clip)

    _, sliced_clip = os.path.split(clip.url[:-3])
    convert_clip = og_clip.export(
        os.path.join(settings.MEDIA_ROOT, sliced_clip + 'mp3'), format='mp3'
    )

    new_clip = SimpleUploadedFile(
        name=sliced_clip + 'mp3',
        content=convert_clip.read(),
        content_type='audio/mpeg'
    )
    os.remove(os.path.join(settings.MEDIA_ROOT, sliced_clip + 'mp3'))
    return new_clip
