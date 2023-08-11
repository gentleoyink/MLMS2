from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from djmoney.models.fields import MoneyField
from users.models import CustomUser
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from autoslug import AutoSlugField

class CourseCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Category"))
    description = models.TextField(null=True, default=None, verbose_name=_("Category Description"))

    def __str__(self):
        return self.name

class CourseSubcategory(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, verbose_name=_("Category"))
    name = models.CharField(max_length=255, verbose_name=_("Subcategory"))
    description = models.TextField(null=True, default=None, verbose_name=_("Subcategor Description"))

    def __str__(self):
        return self.name
    
class Course(models.Model):
    ALL_LEVELS = 'AL'
    BEGINNER = 'BG'
    INTERMEDIATE = 'IT'
    ADVANCED = 'AD'

    LEVEL_CHOICES = [
        (ALL_LEVELS, _('All Levels')),
        (BEGINNER, _('Beginner')),
        (INTERMEDIATE, _('Intermediate')),
        (ADVANCED, _('Advanced')),
    ]

    title = models.CharField(max_length=255, verbose_name=_("Course Title"))
    subtitle = models.CharField(max_length=255, null=True, default=None, verbose_name=_("Subtitle"))
    description = models.TextField(verbose_name=_("Course Description"))
    category = models.ForeignKey(CourseCategory, related_name='courses', null=True, on_delete=models.CASCADE, verbose_name=_("Category"))
    subcategory = models.ForeignKey(CourseSubcategory, null=True, on_delete=models.CASCADE, verbose_name=_("Subcategory"))
    learning_outcomes = models.TextField(verbose_name=_("Learning Outcomes"), null=True, default=None)  
    course_for = models.TextField(verbose_name=_("Course For"), null=True, default=None) 
    total_enrolled_students = models.IntegerField(default=0, verbose_name=_("Total Enrolled Students"))
    instructor = models.ForeignKey(CustomUser, related_name='instructed_modules', null=True, default=None, on_delete=models.SET_NULL, verbose_name=_("Instructor"))
    students = models.ManyToManyField(CustomUser, related_name='enrolled_modules', verbose_name=_("Students"))
    is_featured = models.BooleanField(default=False, verbose_name=_("Featured"))
    is_marketplace = models.BooleanField(default=False, verbose_name=_("Enable Marketplace"))
    fee = MoneyField(max_digits=14, decimal_places=2, default_currency='USD', verbose_name=_("Price"))
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=ALL_LEVELS, verbose_name=_("Course Level"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name=_("Last Udated"))
    video_url = models.URLField(blank=True, null=True, verbose_name=_("Video URL"))
    video_file = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name=_("Upload Video"))
    video_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name=_("Total Video Hours"))
    num_files = models.IntegerField(default=0, verbose_name=_("Number of Uploaded Files"))
    slug = AutoSlugField(populate_from='title', editable=False, unique=True, verbose_name=_("URL Slug"))
    @property
    def average_rating(self):
        avg_rating = self.ratings.all().aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating else 0
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__original_title = self.title
        self.__original_subtitle = self.subtitle
        self.__original_description = self.description
        self.__original_category = self.category
        self.__original_subcategory = self.subcategory
        self.__original_video_url = self.video_url
        self.__original_video_file = self.video_file

    def save(self, *args, **kwargs):
        if self.is_featured:
            # assuming that a featured course has is_featured=True
            num_featured = Course.objects.filter(is_featured=True).count()
            if num_featured >= 10:
                raise Exception("Cannot have more than 10 featured courses")
        if (self.title != self.__original_title or 
            self.subtitle != self.__original_subtitle or
            self.description != self.__original_description or
            self.category != self.__original_category or
            self.subcategory != self.__original_subcategory or
            self.video_url != self.__original_video_url or
            self.video_file != self.__original_video_file):
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        self.__original_title = self.title
        self.__original_subtitle = self.subtitle
        self.__original_description = self.description
        self.__original_category = self.category
        self.__original_subcategory = self.subcategory
        self.__original_video_url = self.video_url
        self.__original_video_file = self.video_file

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    def update_total_students(self):
        self.total_enrolled_students = self.students.count()
        self.save()

    def update_counts(self):
        # Sum up all the video durations, PDF counts and other file counts from associated lessons.
        self.total_video_hours = sum(lesson.video_duration for lesson in self.lessons.all())
        self.pdf_count = sum(lesson.pdf_count for lesson in self.lessons.all())
        self.other_files_count = sum(lesson.other_files_count for lesson in self.lessons.all())
        self.save()
    def __str__(self):
        return self.title
    
class CourseRating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE, verbose_name=_("Course"))
    user = models.ForeignKey(CustomUser, related_name='course_ratings', on_delete=models.CASCADE, verbose_name=_("User"))
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_("Rating"))  
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    