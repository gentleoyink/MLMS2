"""
URL configuration for edcific project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from courses.views import CourseDetailView, CourseUpdateView, CourseDeleteView
from modules.views import ModuleDetailView, ModuleUpdateView, ModuleDeleteView, ModuleCreateView
from lessons.views import LessonDetailView, LessonUpdateView, LessonDeleteView, UserLessonsListView, LessonCreateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('course/<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/edit/<slug:slug>/', CourseUpdateView.as_view(), name='course_edit'), 
    path('course/delete/<slug:slug>/', CourseDeleteView.as_view(), name='course_delete'),

    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


    path('modules/', include(('modules.urls', 'modules'), namespace='modules')),
    path('module/<slug:slug>/', ModuleDetailView.as_view(), name='module_detail'), 
    path('module/create/<str:course_slug>/', ModuleCreateView.as_view(), name='module_create'),   
    path('module/edit/<slug:slug>/', ModuleUpdateView.as_view(), name='module_update'),
    path('module/delete/<slug:slug>/', ModuleDeleteView.as_view(), name='module_delete'),

    # Paths for lessons
    #path('lessons/', include(('modules.urls', 'modules'), namespace='lessons')),
    path('lessons/', UserLessonsListView.as_view(), name='lessons'),
    path('lesson/create/<str:module_slug>/', LessonCreateView.as_view(), name='lesson_create'),
    path('lesson/<slug:slug>/', LessonDetailView.as_view(), name='lesson_detail'),    
    path('lesson/edit/<slug:slug>/', LessonUpdateView.as_view(), name='lesson_update'),
    path('lesson/delete/<slug:slug>/', LessonDeleteView.as_view(), name='lesson_delete'),



    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

