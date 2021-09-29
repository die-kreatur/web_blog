from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from .. views import *


class TestHomePage(TestCase):
    """Test HomePageView"""
    def test_get_home_page(self):
        """Checking if the home page is displayed properly"""
        client = Client()
        response = client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class TestAboutView(TestCase):
    """Test AboutPageView"""
    def test_get_about_page(self):
        """Checking if the about page is displayed properly"""
        client = Client()
        response = client.get(reverse('blog-about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')


class TestLatestPostView(TestCase):
    """Test LatestPostView"""
    def test_get_latest_posts(self):
        """Checking if the page with latest post is displayed properly"""
        client = Client()
        response = client.get(reverse('latest-posts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/latest_posts.html')


class TestUserPostListView(TestCase):
    """Test UserPostListView"""

    def setUp(self):
        """Creating a test user and his post to see if the certain
        user's page with posts is displayed properly"""

        self.factory = RequestFactory()
        
        self.user = User.objects.create_user(
            username='test_user',
            email='testuser@example.com',
            password='fhhewo87539275'
        )
        self.post = Post.objects.create(
            title='test_post',
            content='blabla',
            author=self.user
        )
        
    def test_get_queryset(self):
        """Testing get_queryset function"""
        url = reverse('user-posts', kwargs={'username': self.user.username})
        request = self.factory.get(url)
        request.user = AnonymousUser()
        
        view = UserPostListView()
        view.setup(request)

        queryset = view.get_queryset()
        self.assertIn(self.post, queryset)
