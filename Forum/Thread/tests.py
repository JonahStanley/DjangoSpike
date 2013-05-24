"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from Thread.models import Post
from django.test.client import Client
from django.contrib.auth.models import User


class ModelTest(TestCase):
    def test_create_post(self):
        p = Post.objects.create(username=1, text="HI")
        self.assertEqual(p.username, Post.objects.get(username=1).username)
        self.assertEqual(p.text, Post.objects.get(username=1).text)

    def test_post_length(self):
        #from pdb import set_trace; set_trace()
        try:
            Post.objects.create(username=1, text=str(range(1,500)))
        except ValueError:
            pass
        else:
            self.fail("Didn't get expected error")


class IntegrationTest(TestCase):
    def test_empty_forum(self):
        c = Client()

        #register new user and log in
        c.post('/register/',{'username':'test','password':'test'})
        c.login(username='test', password='test')
        response = c.get("/forum/")

        if not response.context['posts']:
            pass
        else:
            self.fail("NOT EMPTY")
        if "Nobody has written anything yet!" in response.content:
            pass
        else:
            self.fail("NOT EMPTY")

    def test_one_post(self):
        c = Client()
        
        #register new user and log in
        c.post('/register/',{'username':'test','password':'test'})
        c.login(username='test', password='test')
        response = c.get("/forum/")

        response = c.post("/forum/", {'username': 'test', 'text': "hi", 'todo': 'add'})
        if not "Nobody has written anything yet!" in response.content:
            pass
        else:
            self.fail("STILL EMPTY")
        if "hi" in response.content:
            pass
        else:
            self.fail("NOT Posted")
        self.assertEqual(response.context['posts'][0].username, 'test')


    def test_two_posts(self):
        c = Client()
        u = User.objects.create_user('super', '', 'super')
        u.save()
        c.login(username='super', password='super')
        c.post("/forum/", {'text': "hi", 'todo': 'add'})
        response = c.post("/forum/", {'text': "goodbye", 'todo': 'add'})
        if response.context['posts'][0].text == "hi":
            pass
        else:
            self.fail("First post not here")
        if "goodbye" in response.content:
            pass
        else:
            self.fail("Second post not here")
        self.assertEqual(response.context['posts'][0].username, 'super')
        self.assertEqual(response.context['posts'][1].username, 'super')

    def test_remove_one_post(self):
        c = Client()
        u = User.objects.create_user('super', '', 'super')
        u.save()
        c.login(username='super', password='super')
        r = c.post("/forum/", {'text': "hi", 'todo': 'add'})
        response = c.post("/forum/", {'todo': 'del', 'del_id': r.context['posts'][0].id})
        if "Nobody has written anything yet!" in response.content:
            pass
        else:
            self.fail("NOT EMPTY")
        if not response.context['posts']:
            pass
        else:
            self.fail("First post is here")

    def test_remove_one_post_two(self):
        c = Client()
        u = User.objects.create_user('super', '', 'super')
        u.save()
        c.login(username='super', password='super')
        r = c.post("/forum/", {'text': "hi", 'todo': 'add'})
        c.post("/forum/", {'text': "goodbye", 'todo': 'add'})
        response = c.post("/forum/", {'todo': 'del', 'del_id': r.context['posts'][0].id})
        if "goodbye" in response.content:
            pass
        else:
            self.fail("Second post not here")
        if not response.context['posts'][0].text == "hi":
            pass
        else:
            self.fail("First post is here")

