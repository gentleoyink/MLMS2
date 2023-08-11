import pytz
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django_countries.fields import CountryField
#from django_countries.data import countries

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        (1, 'Student'),
        (2, 'Instructor'),
        (3, 'Staff'),
        (4, 'Admin'),
    ]

    TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.all_timezones]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # makes sure email is required, removes username from required

    objects = CustomUserManager()
    
    # Basic Fields
    bio = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    # Suggested Fields
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='default_image.jpg')
    social_links = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    specialization = models.CharField(max_length=50, blank=True)
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default='UTC')
    preferred_language = models.CharField(max_length=7, choices=settings.LANGUAGES, default='en')
    groups = models.ManyToManyField(Group, related_name="customuser_set")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set")
    contact_address1 = models.CharField(max_length=100, blank=True, verbose_name=_('Address Line 1'))
    contact_address2 = models.CharField(max_length=100, blank=True, verbose_name=_('Address Line 2'))
    contact_state = models.CharField(max_length=50, blank=True, verbose_name=_('State'))
    contact_country = CountryField(blank=True, null=True, verbose_name=_('Country'))
    contact_zipcode = models.CharField(max_length=10, blank=True, verbose_name=_('Zip/Post Code'))
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name=_('Phone Number'))
    show_email = models.BooleanField(default=False)
    show_courses = models.BooleanField(default=False)

    def __str__(self):
        return self.email
    
class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

