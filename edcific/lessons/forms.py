from django import forms
from .models import Lesson
from modules.models import Module


class LessonForm(forms.ModelForm):
    module = forms.ModelChoiceField(queryset=Module.objects.none())  # initially no choices
    
    class Meta:
        model = Lesson
        exclude = ['video_length', 'updated_at', 'created_at', 'instructor', 'slug']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # get current user from passed kwargs, default to None
        module_slug = kwargs.pop('module_slug', None)  # get module_slug from passed kwargs, default to None
        super(LessonForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['module'].queryset = Module.objects.filter(instructor=user)  # set queryset for module field
        if module_slug is not None:
            self.fields['module'].initial = Module.objects.get(slug=module_slug)  # pre-select the module

    def save(self, commit=True):
        # get the instance but don't save yet
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
        
        return instance