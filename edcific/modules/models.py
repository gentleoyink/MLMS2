from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from djmoney.models.fields import MoneyField
import os
from courses.models import Course  # Import Course from courses app
from users.models import CustomUser  # Import CustomUser from users app
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from autoslug import AutoSlugField

def validate_file_extension(value):
    if not value.name.endswith('.zip'):
        raise ValidationError("Only ZIP files are allowed.")
    
class Module(models.Model):
    BEGINNER = 'BG'
    INTERMEDIATE = 'IT'
    ADVANCED = 'AD'
    
    LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
    ]
    title = models.CharField(max_length=255, verbose_name=_("Module Title"))
    description = models.TextField()
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    instructor = models.ForeignKey(CustomUser, related_name='instructed_courses', on_delete=models.CASCADE)
    fee = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Last Udated"))
    is_marketplace = models.BooleanField(default=False)
    videos_length = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    # file = models.FileField(upload_to='uploads/', validators=[validate_file_extension], default='nofile.zip')
    slug = AutoSlugField(populate_from='title', editable=False, unique=True, verbose_name=_("URL Slug"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__original_title = self.title
        self.__original_description = self.description
        super(Module, self).__init__(*args, **kwargs)
        self.__original_course = self.course if self.pk else None

    def save(self, *args, **kwargs):
        if (self.title != self.__original_title or 
            self.description != self.__original_description or
            self.course != self.__original_course):
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        self.__original_title = self.title
        self.__original_description = self.description
        self.__original_course = self.course

    def get_absolute_url(self):
        return reverse('module_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return f'{self.title} ({self.course.title if self.course else "No course"})'

    def update_counts(self):
        # Sum up all the video durations, PDF counts and other file counts from associated lessons.
        self.videos_length = sum(lesson.video_duration for lesson in self.lessons.all())
        self.save()