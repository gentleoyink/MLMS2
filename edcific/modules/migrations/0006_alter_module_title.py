# Generated by Django 4.2.2 on 2023-07-17 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0005_delete_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Module Title'),
        ),
    ]
