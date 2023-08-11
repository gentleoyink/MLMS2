from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import CuratedCourse, CuratedModule, LessonBucket, ModuleBucket
from django.urls import reverse_lazy

# For CuratedCourse
class CuratedCourseListView(ListView):
    model = CuratedCourse
    template_name = 'curatedcourses/curatedcourse_list.html'

class CuratedCourseDetailView(DetailView):
    model = CuratedCourse
    template_name = 'curatedcourses/curatedcourse_detail.html'

class CuratedCourseCreateView(CreateView):
    model = CuratedCourse
    template_name = 'curatedcourses/curatedcourse_form.html'
    fields = ('course', 'description', 'modules')  # Use 'fields' or define a form_class with a ModelForm

    def form_valid(self, form):
        form.instance.curator = self.request.user
        return super().form_valid(form)

class CuratedCourseUpdateView(UpdateView):
    model = CuratedCourse
    template_name = 'curatedcourses/curatedcourse_form.html'
    fields = ('course', 'description', 'modules')

class CuratedCourseDeleteView(DeleteView):
    model = CuratedCourse
    template_name = 'curatedcourses/curatedcourse_confirm_delete.html'
    success_url = reverse_lazy('curatedcourse_list')

# Similar views for CuratedModule
