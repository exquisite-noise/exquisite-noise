# Generated by Django 2.0.5 on 2018-05-21 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('noise_audio', '0002_auto_20180521_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audio',
            old_name='user',
            new_name='contributor',
        ),
    ]
