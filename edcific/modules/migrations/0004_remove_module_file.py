# Generated by Django 4.2.2 on 2023-07-15 22:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0003_rename_video_hours_module_videos_length_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='file',
        ),
    ]
