from django.db import models

# Create your models here.
class Post(models.Model):
	userid = models.IntegerField()
	text = models.TextField()
	time = models.DateTimeField(auto_now_add = True)


# class User(models.Model):
# 	username = models.CharField(max_length = 30, unique = True)
# 	password = models.CharField(max_length = 30)
# 	first_name = models.CharField(max_length = 30)
# 	last_name = models.CharField(max_length = 30)