from django.db import models
from users.models import CustomUser
from courses.models import Course
from modules.models import Module
from lessons.models import Lesson
from datetime import timedelta
from django.utils import timezone

class CuratedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curated_courses', null=True)
    description = models.TextField()
    modules = models.ManyToManyField(Module, related_name='curated_in_courses')
    curator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='curated_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.title} curated by {self.curator.username}" if self.course else f"Module curated by {self.curator.username}"


class CuratedModule(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='curated_modules', null=True)
    description = models.TextField()
    lessons = models.ManyToManyField(Lesson, related_name='curated_in_modules')
    curator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='curated_modules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.module.title} curated by {self.curator.username}" if self.module else f"Module curated by {self.curator.username}"
    
class LessonBucket(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='in_user_buckets')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='lesson_buckets')
    added_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.lesson.title} in {self.user.username}'s bucket"

    def save(self, *args, **kwargs):
        if not self.id:
            self.expires_at = timezone.now() + timedelta(days=60)
        super().save(*args, **kwargs)

    @classmethod
    def add_to_bucket(cls, lesson, user):
        item, created = cls.objects.get_or_create(lesson=lesson, user=user)
        if not created:
            # Update the expires_at field if the item already exists
            item.expires_at = timezone.now() + timedelta(days=60)
            item.save()

    @classmethod
    def remove_from_bucket(cls, lesson, user):
        cls.objects.filter(lesson=lesson, user=user).delete()

class ModuleBucket(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='in_user_buckets')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='module_buckets')
    added_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.module.title} in {self.user.username}'s bucket"

    def save(self, *args, **kwargs):
        if not self.id:
            self.expires_at = timezone.now() + timedelta(days=60)
        super().save(*args, **kwargs)

    @classmethod
    def add_to_bucket(cls, module, user):
        item, created = cls.objects.get_or_create(module=module, user=user)
        if not created:
            # Update the expires_at field if the item already exists
            item.expires_at = timezone.now() + timedelta(days=60)
            item.save()

    @classmethod
    def remove_from_bucket(cls, module, user):
        cls.objects.filter(module=module, user=user).delete()