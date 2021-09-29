from django.test import TestCase, RequestFactory, Client, client
from django.urls import reverse
from django.contrib.auth.models import User
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
        client = Client()
        response = client.get(reverse('latest-posts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/latest_posts.html')
