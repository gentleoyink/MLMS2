from django.urls import path
from .views import (
    AllLessonsListView
)

app_name = 'lessons'

urlpatterns = [
   
    # Paths for lessons
    path('all-lessons/', AllLessonsListView.as_view(), name='all-lessons'),
]
