from django.contrib import admin

# Register your models here.
from .models import CourseCategory, Course, CourseRating, CourseSubcategory

admin.site.register(CourseCategory)
admin.site.register(Course)
admin.site.register(CourseRating)
admin.site.register(CourseSubcategory)



