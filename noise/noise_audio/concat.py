import os

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from pydub import AudioSegment


def concat_clips(prev_clip, new_clip):
    """
    Concat previous clip with new clip.
    """
    # import pdb; pdb.set_trace()
    prev = AudioSegment.from_file(prev_clip)
    new = AudioSegment.from_file(new_clip)

    combo = prev + new

    os.remove(prev_clip)
    import pdb; pdb.set_trace()

    print('printing prev_clip', prev_clip)
    combined_clip = combo.export(prev_clip, format='mp3', codec='libmp3lame')

    # new_combined_clip = SimpleUploadedFile(
    #     name=combo,
    #     content=combined_clip.read(),
    #     content_type='audio/mpeg'
    # )
    return combined_clip
