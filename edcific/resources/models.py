
from django.db import models

class ResourceType(models.Model):
    name = models.CharField(max_length=255)

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(ResourceType, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resources/')
