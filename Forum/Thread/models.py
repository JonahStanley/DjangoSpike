from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import *


# Create your models here.
class Post(models.Model):
    userid = models.IntegerField()
    text = models.CharField(max_length=5)
    time = models.DateTimeField(auto_now_add=True)

    def save(self):
        try:
            self.clean_fields()
            super(submit_post, self).sav()
        except:
            raise ValueError('text too long!!!')

# class User(models.Model):
#      username = models.CharField(max_length = 30, unique = True)
#      password = models.CharField(max_length = 30)
#      first_name = models.CharField(max_length = 30)
#      last_name = models.CharField(max_length = 30)
