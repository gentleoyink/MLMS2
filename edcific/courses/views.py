from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.db.models import Count  # <-- add this
from django.views.generic.detail import DetailView
from .models import Course
from django.urls import reverse
from .forms import CourseForm

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class PopularCoursesView(generic.ListView):
    model = Course
    template_name = 'courses/popular.html'
    
    def get_queryset(self):
        # ordering by the number of students enrolled in each course
        return Course.objects.all().annotate(num_students=Count('students')).order_by('-num_students')

class FeaturedCoursesView(generic.ListView):
    model = Course
    template_name = 'courses/featured.html'
    
    def get_queryset(self):
        return Course.objects.filter(is_featured=True)


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    # fields = ['title', 'description', 'category', 'fee', 'level', 'is_active', 'start_date', 'expiry_date', 'video_url', 'video_file', 'resources']
    
    def form_valid(self, form):
        course = form.save(commit=False)
        course.instructor = self.request.user
        course.category = form.cleaned_data.get('category')
        course.subcategory = form.cleaned_data.get('subcategory')
        course.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)  
    
    def get_success_url(self):
        #return reverse('course_detail', kwargs={'slug': self.object.slug})
        return reverse('courses:user-courses')

class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm
    # fields = ['title', 'subtitle', 'information', 'description', 'category', 'subcategory', 'fee', 'level', 'is_active', 'video_url', 'video_file', 'is_marketplace']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.instructor = self.request.user
        course.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse('course_detail', kwargs={'slug': self.object.slug})
        return reverse('courses:user-courses')
    
    def test_func(self):
        course = self.get_object()
        if self.request.user == course.instructor:
            return True
        return False

class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('courses:user-courses')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.instructor:
            return True
        return False

class UserCoursesListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = 'courses/user_courses.html'
    
    def get_queryset(self):
        courses = Course.objects.filter(instructor=self.request.user)
        for course in courses:
            print(course.title, course.slug, course.category, course.subcategory )
        return courses


class AllCoursesListView(generic.ListView):
    model = Course
    template_name = 'courses/all_courses.html'
    
    def get_queryset(self):
        return Course.objects.all()

