from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *


# Create your models here.
class Post(models.Model):
    username = models.CharField(max_length=140)
    text = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            self.clean_fields()
            super(Post, self).save()
        except:
            raise ValueError()

# class User(models.Model):
#      username = models.CharField(max_length = 30, unique = True)
#      password = models.CharField(max_length = 30)
#      first_name = models.CharField(max_length = 30)
#      last_name = models.CharField(max_length = 30)
