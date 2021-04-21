from django.db import models

from users.models import CustomUser, UserProfile

# Create your models here.
class Agent(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
