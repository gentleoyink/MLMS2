from django.contrib import admin

# Register your models here.

from .models import ResourceType, Resource

admin.site.register(ResourceType)
admin.site.register(Resource)




