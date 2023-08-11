# models.py
from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course
from django.db.models.signals import post_save
from django.dispatch import receiver

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.course.title}'

@receiver(post_save, sender=Review)
def update_course_rating(sender, instance, **kwargs):
    reviews = Review.objects.filter(course=instance.course)
    total_rating = sum(review.rating for review in reviews)
    instance.course.average_rating = total_rating / reviews.count()
    instance.course.save()
