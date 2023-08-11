# views.py
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Review
from .forms import ReviewForm

class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'reviews/review_list.html'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
