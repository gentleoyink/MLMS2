from django.contrib import admin

# Register your models here.
from .models import CustomUser, UserActivity, Notification

admin.site.register(CustomUser)
admin.site.register(UserActivity)
admin.site.register(Notification)