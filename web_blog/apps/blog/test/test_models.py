from django.test import TestCase
from .help_functions import testPost, testComment, testUser


class TestModels(TestCase):
    """Testing Post and Comment models methods"""
    
    def setUp(self):
        self.user = testUser('test_user')
        self.post = testPost('test_post', self.user)
        self.comment = testComment(self.post, self.user)

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
