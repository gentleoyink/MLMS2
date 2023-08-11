from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Lesson
from modules.models import Module
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import LessonForm


class LessonDetailView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verbose_names'] = {
            field.name: field.verbose_name 
            for field in Lesson._meta.get_fields()
            if not field.auto_created
        }
        context['module_verbose_names'] = {
            field.name: field.verbose_name
            for field in Module._meta.get_fields()
            if not field.auto_created  # Exclude reverse relation fields
        }
        return context



class LessonCreateView(LoginRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm  # you need to use the custom form here
    template_name = 'lessons/lesson_form.html'
    
    def get_form_kwargs(self):
        kwargs = super(LessonCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'module_slug': self.kwargs.get('module_slug')})  # get module_slug from the URL
        return kwargs 
    
    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.instructor = self.request.user
        if 'module' in form.cleaned_data:
            lesson.module = form.cleaned_data.get('module')
        lesson.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)  
    
    def get_success_url(self):
        return reverse('lesson_detail', kwargs={'slug': self.object.slug})


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'lessons/lesson_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs 
 
    def form_valid(self, form):
        lesson = form.save(commit=False)
        lesson.instructor = self.request.user
        lesson.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse('lesson_detail', kwargs={'slug': self.object.slug})
        return reverse('user-lessons')
    
    def test_func(self):
        lesson = self.get_object()
        if self.request.user == lesson.instructor:
            return True
        return False


class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Lesson
    success_url = reverse_lazy('lessons')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        lesson = self.get_object()
        if self.request.user == lesson.instructor:
            return True
        return False

class UserLessonsListView(LoginRequiredMixin, generic.ListView):
    model = Lesson
    template_name = 'lessons/user_lessons.html'
    
    def get_queryset(self):
        lessons = Lesson.objects.filter(instructor=self.request.user)
        for lesson in lessons:
            print(lesson.title, lesson.slug, lesson.module )
        return lessons

class AllLessonsListView(generic.ListView):
    model = Lesson
    template_name = 'lessons/all_lessons.html'
    
    def get_queryset(self):
        return Lesson.objects.all()

