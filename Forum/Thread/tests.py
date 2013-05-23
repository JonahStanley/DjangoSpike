"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from Thread.models import Post


class ModelTest(TestCase):
    def test_create_post(self):
        p = Post.objects.create(userid=1, text="HI")
        p.save()
        self.assertEqual(p.userid, Post.objects.get(userid=1).userid)
        self.assertEqual(p.text, Post.objects.get(userid=1).text)
