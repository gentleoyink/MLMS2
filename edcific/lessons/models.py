from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from djmoney.models.fields import MoneyField
import os
from modules.models import Module  # Import Course from courses app
from users.models import CustomUser  # Import CustomUser from users app
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField

def validate_file_extension(value):
    if not value.name.endswith('.zip'):
        raise ValidationError("Only ZIP files are allowed.")
    
class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Lesson Topic"))
    content = models.TextField()  # you can modify this to handle different content types
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE, verbose_name=_("Module Title"))
    is_preview = models.BooleanField(default=False, verbose_name=_("Mark as preview"))
    instructor = models.ForeignKey(CustomUser, related_name='created_lessons', null=True, on_delete=models.SET_NULL, verbose_name=_("Instructor"))  # new line
    is_marketplace = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Last Updated"))
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name=_("Video Length"))  # in hours
    file = models.FileField(upload_to='uploads/', validators=[validate_file_extension], default='nofile.zip', verbose_name=_("Supporting Files"))
    slug = AutoSlugField(populate_from='title', editable=False, unique=True, verbose_name=_("URL Slug"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__original_title = self.title
        self.__original_content = self.content
        super(Lesson, self).__init__(*args, **kwargs)
        self.__original_module = self.module if self.pk else None

    def save(self, *args, **kwargs):
        if (self.title != self.__original_title or 
            self.content != self.__original_content or
            self.module != self.__original_module):
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        self.__original_title = self.title
        self.__original_content = self.content
        self.__original_module = self.module

    def get_absolute_url(self):
        return reverse('lesson_detail', kwargs={'slug': self.slug})
   
    def __str__(self):
        return f'{self.title} ({self.module.title if self.module else "No module"})'