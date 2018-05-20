from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class NoiseProfile(models.Model):
    """Profile model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        """Show username in admin console."""
        return self.user.username


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, **kwargs):
    """Create an empty profile anytime a new user is created."""
    if kwargs['created']:
        profile = NoiseProfile(user=kwargs['instance'])
        profile.save()
