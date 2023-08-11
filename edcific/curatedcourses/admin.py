from django.contrib import admin

# Register your models here.

from .models import CuratedCourse, CuratedModule, LessonBucket, ModuleBucket

admin.site.register(CuratedCourse)
admin.site.register(CuratedModule)
admin.site.register(ModuleBucket)
admin.site.register(LessonBucket)

