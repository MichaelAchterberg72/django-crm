from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from users.models import CustomUser, UserProfile


SOURCE_CHOICES = (
    ('YT', 'Youtube'),
    ('GG', 'Google'),
    ('NL', 'Newsletter'),
)

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey("Category", related_name="leads", null=True, blank=True, on_delete=models.SET_NULL)

    phoned = models.BooleanField(default=False)
    source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

#    profile_picture = models.ImageField(blank=True, null=True)
    special_files = models.FileField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
