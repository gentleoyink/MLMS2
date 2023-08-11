from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django import forms
from .models import CustomUser

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'email',
            'bio',
            'birthdate',
            'role',
            'profile_image',
            'social_links',
            'specialization',
            'timezone',
            'preferred_language',
            'contact_address1',
            'contact_address2',
            'contact_state',
            'contact_country',
            'contact_zipcode',
            'contact_phone',
            'show_email',
            'show_courses',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [
            (1, 'Student'),
            (2, 'Instructor')
        ]



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add email validation logic if needed
        return email       
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
