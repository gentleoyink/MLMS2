from django.urls import path
from .views import register, profile, profile_edit, UserLoginView, MeView
from .api import LoginView, LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/me/', MeView.as_view(), name='me'),
    path('users/api/logout/', LogoutView.as_view(), name='logout'),
]

