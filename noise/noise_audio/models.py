from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from audio_recorder.models import AudioFileMixin


class Audio(AudioFileMixin, models.Model):
    """Audio model."""

    contributor = models.ManyToManyField(User, related_name='audio')
    topic = models.CharField(max_length=100, blank=True, null=True)
    path = models.FileField(upload_to='clips/')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL,
                                related_name='creator', null=True)
    date_published = models.DateField(blank=True, null=True)
    published = models.CharField(
        max_length=12,
        default='UNPUB',
        choices=(
            ('PUB', 'Published'),
            ('UNPUB', 'Unpublished'),
        )
    )

    def __str__(self):
        """String."""
        return f'{self.topic}'


@receiver(models.signals.post_save, sender=Audio)
def set_published_date(sender, instance, **kwargs):  # pragma: no cover
    """Set published date when story completed and published."""
    if instance.published == 'PUB' and not instance.date_published:
        instance.date_published = timezone.now()
        instance.save()


class AudioAdd(AudioFileMixin, models.Model):
    """Model to hold temporary clip to add to existing story."""

    user = models.ForeignKey(User, related_name='new_clips', on_delete=models.SET_NULL, null=True)
    audio_file = models.FileField(upload_to='temp/')
    pk_master = models.ForeignKey(Audio, on_delete=models.SET_NULL,
                                  related_name='new_audio_files', null=True)
