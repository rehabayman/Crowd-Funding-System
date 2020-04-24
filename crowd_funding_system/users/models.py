from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator


from django.urls import reverse
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=70, null=False, blank=False)
    last_name = models.CharField(max_length=70, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    username = models.CharField(max_length=70, null=False, blank=False, unique=True)

    password = models.CharField(max_length=254, null=False, blank=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{12,13}$', message="Phone number must be entered in the format: '+20 111 111 1111'. Up to 13 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True) # validators should be a list

    # phone = models.CharField(max_length=13) # user can write it as +20 111 111 1111
    profile_pic = models.ImageField(upload_to='images/users/')
    fb_link = models.URLField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    country = CountryField(null=True, blank=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name
    # to test reverse.  it will be reversed to the user's profile page
    # def get_absolute_url(self):
    #     return reverse("users:home")
