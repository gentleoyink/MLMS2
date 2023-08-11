from django import forms
from .models import Course, CourseCategory, CourseSubcategory

class CourseForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=CourseCategory.objects.all(), required=True)
    subcategory = forms.ModelChoiceField(queryset=CourseSubcategory.objects.all(), required=True)

    class Meta:
        model = Course
        exclude = ['instructor', 'video_hours', 'num_files', 'students', 'total_enrolled_students', 'students', 'is_featured', 'created_at', 'updated_at', 'slug']

    def save(self, commit=True):
        # get the instance but don't save yet
        instance = super().save(commit=False)
        
        # if category is not set, set it to default
        if not instance.category:
            instance.category = CourseCategory.objects.get(name='other')
            
        # if subcategory is not set, set it to default
        if not instance.subcategory:
            instance.subcategory = CourseSubcategory.objects.get(name='other')
        
        # now save the instance with all fields correctly set
        if commit:
            instance.save()
        
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = CourseCategory.objects.first()
        self.fields['subcategory'].initial = CourseSubcategory.objects.first()
        self.fields['category'].queryset = CourseCategory.objects.all()
        self.fields['subcategory'].queryset = CourseSubcategory.objects.all()
