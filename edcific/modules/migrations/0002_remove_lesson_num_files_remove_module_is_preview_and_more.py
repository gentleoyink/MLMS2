# Generated by Django 4.2.2 on 2023-07-13 22:18

from django.db import migrations, models
import modules.models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='num_files',
        ),
        migrations.RemoveField(
            model_name='module',
            name='is_preview',
        ),
        migrations.RemoveField(
            model_name='module',
            name='num_files',
        ),
        migrations.AddField(
            model_name='lesson',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='file',
            field=models.FileField(default='nofile.zip', upload_to='uploads/', validators=[modules.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_preview',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='lesson',
            name='slug',
            field=models.SlugField(default='', editable=False, unique=True, verbose_name='URL Slug'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Last Udated'),
        ),
        migrations.AddField(
            model_name='module',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created At'),
        ),
        migrations.AddField(
            model_name='module',
            name='file',
            field=models.FileField(default='nofile.zip', upload_to='uploads/', validators=[modules.models.validate_file_extension]),
        ),
        migrations.AddField(
            model_name='module',
            name='slug',
            field=models.SlugField(default='', editable=False, unique=True, verbose_name='URL Slug'),
        ),
        migrations.AddField(
            model_name='module',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Last Udated'),
        ),
        migrations.DeleteModel(
            name='Resource',
        ),
    ]