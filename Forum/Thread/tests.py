"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from Thread.models import Post
from django.test.client import Client
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ModelTest(TestCase):
    def test_create_post(self):
        p = Post.objects.create(username=1, text="HI")
        self.assertEqual(p.username, Post.objects.get(username=1).username)
        self.assertEqual(p.text, Post.objects.get(username=1).text)

    def test_post_length(self):
        #from pdb import set_trace; set_trace()
        try:
            Post.objects.create(username=1, text=str(range(1, 500)))
        except ValueError:
            pass
        else:
            self.fail("Didn't get expected error")


class IntegrationTest(TestCase):
    def test_empty_forum(self):
        c = Client()

        #create new user and log in
        User.objects.create_user(username='test', password='test')
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

        #create new user and log in
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')

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

    def test_register(self):
        c = Client()

        #register new user and log in
        r = c.post('/register/', {'username': 'test', 'password': 'test'})
        if c.login(username='test', password='test'):
            pass
        else:
            self.fail("Didn't Create User")
        self.assertRedirects(r, '/login/?reg=1', status_code=302)

    def test_duplicate_register(self):
        c = Client()
        u = User.objects.create_user('super', '', 'super')
        u.save()
        r = c.post('/register/', {'username': 'super', 'password': 'super'})
        if "That username already exists" in r.content:
            pass
        else:
            self.fail("DUPLICATES")

    def test_anonymous_user(self):
        c = Client()
        response = c.post("/forum")

        #make sure anon doesn't see post
        if "<form name=\"post\" action=\"\" method=\"post\">" in response:
            self.fail("Anon sees post option")

        #make sure anon can't actually post
        if not response.context['posts']:
            pass
        else:
            self.fail("ANON POSTED")

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


class MalUserTest(TestCase):
    def test_delete_other_post(self):
        """Tests if users can delete other users' posts"""
        c = Client()

        #create new user and log in
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')

        #create post in database with different username
        p = Post.objects.create(username='other', text='lols')

        #try to delete post
        c.post('/forum/', {'todo': 'del', 'del_id': p.id})

        #test that post is still there
        if not Post.objects.filter(username='other'):
            self.fail('deleted other post')


class LoginPageTest(TestCase):
    def test_login_fail(self):
        c = Client()
        r = c.post("/login/", {'username': 'super', 'password': 'super'})
        self.assertEqual(r.templates[0].name, 'login.html')
        if "INVALID USERNAME OR PASSWORD" in r.content:
            pass
        else:
            self.fail("Not invalid")

    def test_login_works(self):
        c = Client()
        u = User.objects.create_user('super', '', 'super')
        u.save()
        r = c.post("/login/", {'username': 'super', 'password': 'super'})
        self.assertRedirects(r, '/forum/', status_code=302)

    def test_logout_works(self):
        c = Client()
        r = c.get("/logout/")
        if "logged out successfully" in r.content:
            pass
        else:
            self.fail("not logged out")

    def test_login_redirection(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        r = c.post("/login/?next=/edit-profile", {'username': 'test', 'password': 'test'})
        self.assertRedirects(r, '/edit-profile', status_code=302)


class EditProfileTest(TestCase):
    def test_field_fill(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.get("/edit-profile/")
        if "test" in r.content:
            pass
        else:
            self.fail("Did not Populate")

    def test_password_needed(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test", 'oldpassword': '', 'password': '', 'firstname': '', 'lastname': '', 'email': ''})
        if "PASSWORDS DID NOT MATCH" in r.content:
            pass
        else:
            self.fail("Password wasn't needed")

    def test_password_correctness(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test", 'oldpassword': 'abcd', 'password': '', 'firstname': '', 'lastname': '', 'email': ''})
        if "PASSWORDS DID NOT MATCH" in r.content:
            pass
        else:
            self.fail("Password wasn't correct")

    def test_password_correctness2(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test", 'oldpassword': 'test', 'password': 'abcd', 'firstname': '', 'lastname': '', 'email': ''})
        if "PROFILE CHANGED" in r.content:
            pass
        else:
            self.fail("Password wasn't correct")

    def test_update(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        if "Jonah" in r.content:
            pass
        else:
            self.fail("Did not Change")

    def test_pass_update(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        c.post("/edit-profile/", {'username': "test", 'oldpassword': 'test', 'password': 'test2', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        c.logout()
        c.login(username='test', password='test2')
        r = c.get("/edit-profile/")
        self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_username_update(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test2", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        c.logout()
        c.login(username='test2', password='test')
        r = c.get("/edit-profile/")
        self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_missing_pass(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test2", 'oldpassword': 'test', 'password': '', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        c.logout()
        c.login(username='test2', password='test')
        r = c.get("/edit-profile/")
        self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_missing_pass2(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test", 'oldpassword': 'test', 'password': '', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        c.logout()
        c.login(username='test', password='test')
        r = c.get("/edit-profile/")
        self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_username_update_SUPER(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        for i in range(0, 1):
            r = c.post("/edit-profile/", {'username': "test2", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
            c.logout()
            c.login(username='test2', password='test')
            r = c.get("/edit-profile/")
            self.assertEqual(r.templates[0].name, 'edit-profile.html')

            r = c.post("/edit-profile/", {'username': "test", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
            c.logout()
            c.login(username='test', password='test')
            r = c.get("/edit-profile/")
            self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_username_dup_update(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        User.objects.create_user(username='test2', password='test')
        c.login(username='test', password='test')
        r = c.post("/edit-profile/", {'username': "test2", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        if "That username already exists" in r.content:
            pass
        else:
            self.fail("Duplicate allowed")
        c.logout()
        c.login(username='test', password='test')
        r = c.get("/edit-profile/")
        self.assertEqual(r.templates[0].name, 'edit-profile.html')

    def test_user_deletion(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        r = c.post('/edit-profile', {'delete': 'delete'})
        self.assertRedirects(r, '/login/', status_code=302)
        if not (User.objects.filter(username='test')):
            pass
        else:
            self.fail("User was not deleted")


class ChangePostTest(TestCase):
    def test_1(self):
        c = Client()
        User.objects.create_user(username='test', password='test')
        c.login(username='test', password='test')
        c.post("/forum/", {'username': 'test', 'text': "hi", 'todo': 'add'})
        c.post("/edit-profile/", {'username': "test2", 'oldpassword': 'test', 'password': 'test', 'firstname': 'Jonah', 'lastname': '', 'email': ''})
        r = c.get("/forum")
        if "test2" in r.content:
            pass
        else:
            self.fail("Username not updated")


class EditPostTest(TestCase):
    def test_edit_works(self):
        """basic test of the edit functionality"""

        c = Client()

        #create new user and log in
        uname = 'test'
        pword = 'test'
        text0 = 'old text'
        text1 = 'new text'
        User.objects.create_user(username=uname, password=pword)
        c.login(username=uname, password=pword)

        #create post for that user
        post = Post.objects.create(username=uname, text=text0)

        #edit the post and re-fetch it from database
        c.post("/edit-post/", {"edit_id": post.id, "new_text": text1})
        post = Post.objects.get(id=post.id)

        #see that edit happened
        self.assertEqual(post.text, text1)

    def test_edit_anon(self):
        """test that anonymous users cant edit others' posts"""

        c = Client()

        #create post for attempted edit
        uname = 'test'
        text0 = 'old text'
        text1 = 'new text'

        #create post for that user
        post = Post.objects.create(username=uname, text=text0)

        #attempt to edit the post and re-fetch it from database
        c.post("/edit-post/", {"edit_id": post.id, "new_text": text1})
        post = Post.objects.get(id=post.id)

        #see that edit didn't happen
        self.assertEqual(post.text, text0)

    def test_edit_other(self):
        """test that users can't edit each others' posts"""

        c = Client()

        #create post for some user and log in
        uname0 = 'test'
        text0 = 'old text'
        post = Post.objects.create(username=uname0, text=text0)

        #create new user and log in
        uname1 = 'name1'
        pword1 = 'pword1'
        c.login(username=uname1, password=pword1)

        #attempt to edit the post and re-fetch it from database
        text1 = 'new_text'
        c.post("/edit-post/", {"edit_id": post.id, "new_text": text1})
        post = Post.objects.get(id=post.id)

        #assert that edit didn't happen
        self.assertEqual(post.text, text0)

    def test_non_exist(self):
        """make sure it does nothing when the post doesn't exist"""

        c = Client()

        #create new user and log in
        uname = 'test'
        pword = 'test'
        text0 = 'old text'
        text1 = 'new text'
        User.objects.create_user(username=uname, password=pword)
        c.login(username=uname, password=pword)

        #create post for that user
        post = Post.objects.create(username=uname, text=text0)

        #edit the post but wuth wrong id and re-fetch it from database
        response = c.post("/edit-post/", {"edit_id": post.id + 1, "new_text": text1})
        post = Post.objects.get(id=post.id)

        #assert that edit didn't happen and that error was added to post data
        self.assertEqual(post.text, text0)
        self.assertEqual(response.content, 'error')


class SeleniumTests(LiveServerTestCase):
    fixtures = ['data.json']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(SeleniumTests, cls).setUpClass()
        User.objects.create_user(username='test', password='test')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(SeleniumTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()

    def test_false_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test1')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()
        self.selenium.find_element_by_xpath('//input[@value="login"]')

    def test_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test2')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test2')
        self.selenium.find_element_by_xpath('//input[@value="register"]').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test2')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test2')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()

    def test_false_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/register/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="register"]').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test2')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test2')
        self.selenium.find_element_by_xpath('//input[@value="register"]').click()

    def test_edit_page(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()
        self.selenium.find_element_by_partial_link_text('Edit Profile').click()
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test2')
        password_input = self.selenium.find_element_by_name("oldpassword")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="edit"]').click()
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test2')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()
        self.selenium.implicitly_wait(10)

    def test_post(self):
        #log in
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('test')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('test')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()

        #go to forum and make post and then delete post
        self.selenium.get('%s%s' % (self.live_server_url, '/forum/'))
        text_input = self.selenium.find_element_by_name("text")
        text_input.send_keys('test text!')
        post_button = self.selenium.find_element_by_name("post_button")
        post_button.click()
        delete_button = self.selenium.find_element_by_name("delete_button")
        delete_button.click()

    def test_edit_post(self):
        self.selenium.implicitly_wait(10)

        #login as super
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('super')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('super')
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()

        # go to forum and find post and edit post
        self.selenium.get('%s%s' % (self.live_server_url, '/forum/'))
        edit_button = self.selenium.find_element_by_xpath('//button[text() = "Edit"]')
        edit_button.click()
        text_area = self.selenium.find_element_by_name("new_text")
        text_area.send_keys('anyone lived in a pretty how town')
        confirm_button = self.selenium.find_element_by_xpath('//input[@value="Confirm"]')
        confirm_button.click()

        # confirm edit happened
        self.selenium.find_element_by_xpath('//p[contains(text(), "in a pretty")]')
