from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User
from .. models import *


class TestModels(TestCase):
    """Testing Post model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@ex.com',
            password='12345testing'
        )
        self.post = Post.objects.create(
            title='test_post',
            content='blablabla',
            author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post,
            comment_author=self.user,
            comment_text='ololo'
        )

    def test_get_absolute_url_post(self):
        """Testing if get_absolute_url of Post model returns valid url"""
        url = self.post.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_absolute_url_comment(self):
        """Testing if get_absolute_url of Comment model returns valid url"""
        url = self.comment.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
