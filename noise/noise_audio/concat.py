import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from pydub import AudioSegment


def concat_clips(prev_clip, new_clip):
    """
    Concat previous clip with new clip.
    """
    # import pdb; pdb.set_trace()
    new = AudioSegment.from_mp3(str(new_clip))
    prev = AudioSegment.from_mp3(str(prev_clip))

    combo = prev + new

    combined_clip = combo.export(
        os.path.join(settings.MEDIA_ROOT), format='mp3'
    )

    # new_combined_clip = SimpleUploadedFile(
    #     name=combo,
    #     content=combined_clip.read(),
    #     content_type='audio/mpeg'
    # )
    return combined_clip
