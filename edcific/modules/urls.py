from django.urls import path
from .views import (
    ModuleCreateView, UserModulesListView, AllModulesListView
)

app_name = 'modules'

urlpatterns = [
    # Paths for modules
    #path('create/', ModuleCreateView.as_view(), name='module_create'),
    path('', UserModulesListView.as_view(), name='user-modules'),
    path('all-modules/', AllModulesListView.as_view(), name='all-modules'),
    
]
