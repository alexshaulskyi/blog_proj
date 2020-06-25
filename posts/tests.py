from django.test import TestCase, Client
from .models import Post, User, Group, Follow
from .forms import PostForm
import datetime as dt
import os.path
import time
from django.test.utils import override_settings

TEST_CACHE = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

class PageCodes(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy', 'dummy@dummy.com', 'dummy')
        self.post = Post.objects.create(id=3, text='test post', author=self.user)
        self.client.post('/auth/login/', {'username': 'dummy', 'password': 'dummy'}, follow=True)

    def test_new_registered_user(self):
        """ Tests if a registered user can access post creation form. """
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
    
    def test_new_anonymous_user(self):
        """ Tests if it's forbidden for an anonymous user to access post creation form """
        self.client.logout()
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?next=/new/')
    
    def test_404(self):
        """ Tests if 404 is fired upon accessing an unexistant page"""
        response = self.client.get('/definitely/doesntexist')
        self.assertEqual(response.status_code, 404)

@override_settings(CACHES=TEST_CACHE)
class ElementsPresenceCacheAndSubs(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy_1', 'dummy_1@dummy.com', 'dummy_1')
        self.group = Group.objects.create(title='testgrp', slug='testgrp', description='testgrp')
        self.post = Post.objects.create(text='This is a post to test text presense and img tag', author=self.user, id=1, pub_date=dt.datetime.now(), group=self.group)
        self.client.post('/auth/login/', {'username': 'dummy_1', 'password': 'dummy_1'}, follow=True)

    def test_post_presence(self):
        """ Tests whether post text is present on all respective pages """
        urls = ('', '/dummy_1/', '/dummy_1/1/', '/group/testgrp/')
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'This is a post to test text presense and img tag')

    def test_post_edit(self):
        """ Tests if a registered user can access post editing form and the edited post text changes on all respective pages """
        response = self.client.get('/dummy_1/1/edit/')
        self.assertEqual(response.status_code, 200)
        self.post.text = 'This is an updated post'
        self.post.save()
        urls = ('', '/dummy_1/', '/dummy_1/1/', '/group/testgrp/')
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, 'This is an updated post')

class TestSubscription(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_two = User.objects.create_user('dummy_2', 'dummy_2@dummy.com', 'dummy_2')
        self.user_three = User.objects.create_user('dummy_3', 'dummy_3@dummy.com', 'dummy_3')
        self.user_four = User.objects.create_user('dummy_4', 'dummy_4@dummy.com', 'dummy_4')
        self.client.post('/auth/login/', {'username': 'dummy_2', 'password': 'dummy_2'}, follow=True)
        self.post = Post.objects.create(id=2, text='Post to test subscription', author=self.user_two, pub_date=dt.datetime.now())
        self.client.post('/auth/login/', {'username': 'dummy_3', 'password': 'dummy_3'}, follow=True)
        

    def test_registered_subscription(self):
        """ Tests if a registered user can subscribe to another user """
        response = self.client.get('/dummy_2/follow/')
        self.assertRedirects(response, '/dummy_2/')
        self.assertTrue(Follow.objects.filter(user=self.user_three, author=self.user_two).exists())

    def subscriber_sees_post(self):
        response = self.client.get('/follow/')
        self.assertContains(response, 'Post to test subscription')
        self.client.logout()
        self.client.post('/auth/login/', {'username': 'dummy_4', 'password': 'dummy_4'}, follow=True)
        self.assertNotContains(response, 'Post to test subscription')
    
    def test_unsubscribe(self):
        """ Tests if a registered user can unsubscribe from another user """
        response = self.client.get('/dummy_2/unfollow/')
        self.assertRedirects(response, '/dummy_2/')
        self.assertFalse(Follow.objects.filter(user=self.user_three, author=self.user_two).exists())

    def test_comment(self):
        """ Tests if anonymouse user is prohibited from commenting posts """
        self.client.logout()
        response = self.client.get('/dummy_2/2/comment')
        self.assertEqual(response.status_code, 302)
    
    def test_anonymous_subscription(self):
        """ Tests if an anonymous user is being redirected to login page upon an attempt to subscribe """
        self.client.logout()
        response = self.client.get('/dummy_2/follow/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/auth/login/?next=/dummy_2/follow/')

@override_settings(CACHES=TEST_CACHE)
class ImagePresenceTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy_6', 'dummy_6@dummy_two.com', 'dummy_6')
        self.client.post('/auth/login/', {'username': 'dummy_6', 'password': 'dummy_6'}, follow=True)
        self.group = Group.objects.create(id=2, title='testgrp2', slug='testgrp2', description='testgrp2')
        self.post = Post.objects.create(id=4, text='text', author=self.user, group=self.group)
        
    def test_img_presence(self):
        """ Tests if an image appears on respective pages """
        with open('static\\default.jpg', 'rb') as tp:
            self.client.post('/dummy_6/4/edit/', {'text': 'test text', 'image': tp})
        urls = ('', '/dummy_6/', '/dummy_6/4/')
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, '<img')