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
        self.assertEqual(p.userid, Post.objects.get(userid=1).userid)
        self.assertEqual(p.text, Post.objects.get(userid=1).text)

    def test_post_length(self):
        #from pdb import set_trace; set_trace()        
        try:
            Post.objects.create(userid=1, text="BLBLBLBLBLBLBLBLBLBLBLBLB")
        except ValueError:
            pass
        else:
            self.fail("Didn't get expected")
