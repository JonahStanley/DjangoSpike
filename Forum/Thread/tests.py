"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from Thread.models import Post
from django.test.client import Client


class ModelTest(TestCase):
    def test_create_post(self):
        p = Post.objects.create(userid=1, text="HI")
        self.assertEqual(p.userid, Post.objects.get(userid=1).userid)
        self.assertEqual(p.text, Post.objects.get(userid=1).text)

    def test_post_length(self):
        #from pdb import set_trace; set_trace()
        try:
            Post.objects.create(userid=1, text="This is a test of the emergency long post system.  Please stand by as this sentence becomes increasingly larger so that an error gets thrown.  AHHAHAHAHAHHAHAHAHAHAHHA :P")
        except ValueError:
            pass
        else:
            self.fail("Didn't get expected")


class IntegrationTest(TestCase):
    def test_empty_forum(self):
        c = Client()
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
        response = c.post("/forum/", {'userid': 1, 'text': "hi", 'todo': 'add'})
        if not "Nobody has written anything yet!" in response.content:
            pass
        else:
            self.fail("EMPTY")
        if "hi" in response.content:
            pass
        else:
            self.fail("NOT Posted")
        self.assertEqual(response.context['posts'][0].userid, 1)

    def test_two_posts(self):
        c = Client()
        c.post("/forum/", {'userid': 1, 'text': "hi", 'todo': 'add'})
        response = c.post("/forum/", {'userid': 2, 'text': "goodbye", 'todo': 'add'})
        if "hi" in response.content:
            pass
        else:
            self.fail("First post not here")
        if "goodbye" in response.content:
            pass
        else:
            self.fail("Second post not here")
        self.assertEqual(response.context['posts'][0].username, 'AnonymousUser')
        self.assertEqual(response.context['posts'][1].username, 'AnonymousUser')

    def test_remove_one_post(self):
        c = Client()
        r = c.post("/forum/", {'userid': 1, 'text': "hi", 'todo': 'add'})
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
        r = c.post("/forum/", {'userid': 1, 'text': "hi", 'todo': 'add'})
        c.post("/forum/", {'userid': 2, 'text': "goodbye", 'todo': 'add'})
        response = c.post("/forum/", {'todo': 'del', 'del_id': r.context['posts'][0].id})
        if "goodbye" in response.content:
            pass
        else:
            self.fail("Second post not here")
        if not response.context['posts'][0].text == "hi":
            pass
        else:
            self.fail("First post is here")
