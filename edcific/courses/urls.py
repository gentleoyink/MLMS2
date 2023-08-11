from django.urls import path
from .views import AllCoursesListView, CourseCreateView, PopularCoursesView, FeaturedCoursesView
from .views import UserCoursesListView, CourseUpdateView, CourseDeleteView, CourseDetailView

app_name = 'courses'

urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path('popular/', PopularCoursesView.as_view(), name='popular-courses'),
    path('featured/', FeaturedCoursesView.as_view(), name='featured-courses'),
    # path('edit-course/<slug:slug>/', CourseUpdateView.as_view(), name='course_edit'), 
    # path('delete-course/<slug:slug>/', CourseDeleteView.as_view(), name='course_delete'),
    path('', AllCoursesListView.as_view(), name='all-courses'),
    # path('course-info/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('created/', UserCoursesListView.as_view(), name='user-courses'),
]