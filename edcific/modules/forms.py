from django import forms
from .models import Module
from courses.models import Course


class ModuleForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.none())  # initially no choices
    
    class Meta:
        model = Module
        exclude = ['videos_length', 'updated_at', 'created_at', 'instructor', 'slug']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get current user from passed kwargs, default to None
        course_slug = kwargs.pop('course_slug', None)  # get course_slug from passed kwargs, default to None
        super(ModuleForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['course'].queryset = Course.objects.filter(instructor=user)  # set queryset for course field
            
        if course_slug is not None:
            self.fields['course'].initial = Course.objects.get(slug=course_slug)  # pre-select the course



    def save(self, commit=True):
        # get the instance but don't save yet
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
        
        return instance