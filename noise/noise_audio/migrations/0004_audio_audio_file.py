# Generated by Django 2.0.5 on 2018-05-22 20:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('noise_audio', '0003_auto_20180521_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='audio_file',
            field=models.FileField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]
