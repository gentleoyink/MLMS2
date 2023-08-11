from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Module
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import generic
from django.db.models import Count  # <-- add this
from django.views.generic.detail import DetailView
from django.urls import reverse
from .forms import ModuleForm

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = 'modules/module_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'modules/module_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print("Current user: ", self.request.user)  # print the current user
        kwargs.update({'user': self.request.user})
        kwargs.update({'course_slug': self.kwargs.get('course_slug')})  # get course_slug from the URL
        return kwargs
       
    def form_valid(self, form):
        module = form.save(commit=False)
        module.instructor = self.request.user
        if 'course' in form.cleaned_data:
            module.course = form.cleaned_data.get('course')
        module.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)  
      
    def get_success_url(self):
        #return reverse('module_detail', kwargs={'slug': self.object.slug})
        return reverse('lessons')
    
class ModuleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'modules/module_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        print("Current user: ", self.request.user)  # print the current user
        kwargs.update({'user': self.request.user})
        return kwargs

 
    def form_valid(self, form):
        module = form.save(commit=False)
        module.instructor = self.request.user
        module.save()
        form.save_m2m()  # save many-to-many fields
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse('module_detail', kwargs={'slug': self.object.slug})
        return reverse('modules:user-modules')
    
    def test_func(self):
        module = self.get_object()
        if self.request.user == module.instructor:
            return True
        return False

class ModuleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Module
    success_url = reverse_lazy('modules:user-modules')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        module = self.get_object()
        if self.request.user == module.instructor:
            return True
        return False

class UserModulesListView(LoginRequiredMixin, generic.ListView):
    model = Module
    template_name = 'modules/user_modules.html'
    
    def get_queryset(self):
        modules = Module.objects.filter(instructor=self.request.user)
        for module in modules:
            print(module.title, module.slug, module.course )
        return modules

class AllModulesListView(generic.ListView):
    model = Module
    template_name = 'modules/all_modules.html'
    
    def get_queryset(self):
        return Module.objects.all()
