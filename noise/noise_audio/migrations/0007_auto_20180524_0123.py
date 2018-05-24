# Generated by Django 2.0.5 on 2018-05-24 01:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('noise_audio', '0006_auto_20180524_0027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audioadd',
            name='username',
        ),
        migrations.AddField(
            model_name='audioadd',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_clips', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='audioadd',
            name='pk_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_audio_files', to='noise_audio.Audio'),
        ),
    ]