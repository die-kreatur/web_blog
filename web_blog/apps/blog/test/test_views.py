from django.core.exceptions import PermissionDenied
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
        self.post1 = Post.objects.create(
            title='test_post',
            content='blabla',
            author=self.user
        )
        self.post2 = Post.objects.create(
            title='test_post2',
            content='blablablabla',
            author=self.user
        )
        
    def test_get_queryset(self):
        """Testing get_queryset function"""
        url = reverse('user-posts', kwargs={'username': self.user.username})
        request = self.factory.get(url)
        request.user = AnonymousUser()

        view = UserPostListView()
        view.setup(request, username=self.user.username)

        queryset = view.get_queryset()
        result = Post.objects.filter(author=self.user).order_by('-date_posted')
        self.assertQuerysetEqual(queryset, result)

    def test_if_author_in_context(self):
        """Testing if author_profile is in context dict"""
        url = reverse('user-posts', kwargs={'username': self.user.username})
        request = self.factory.get(url)
        request.user = AnonymousUser()

        response = UserPostListView.as_view()\
            (request, username=self.user.username)
        
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('author_profile', response.context_data)


class TestPostDetailView(TestCase):
    """Testing PostDetailView"""
    def setUp(self):

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
        self.comment1 = Comment.objects.create(
            post = self.post,
            comment_author = self.user,
            comment_text = 'lololol'
        )

    def test_if_comments_displayed_under_post(self):
        """Testing get_context_data function"""
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        request = self.factory.get(url)
        request.user = AnonymousUser()

        response = PostDetailView.as_view()\
            (request, pk=self.post.id)
        
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('comments', response.context_data)


class TestPostCreateView(TestCase):
    """Testing PostCreateView"""
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('post-create')

    def test_create_post_by_anonymous(self):
        """Testing if we get redirect if anonymous user tries to create a new post"""        
        request = self.factory.post(self.url)
        request.user = AnonymousUser()

        # if Anonymous tries to create post he should be 
        # redirected to the login page
        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)


class TestPostUpdateView(TestCase):
    """Testing PostUpdateView"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test_user',
            email='testuser@example.com',
            password='fhhewo87539275'
        )
        self.author = User.objects.create_user(
            username='testautor',
            email='testauthor@example.com',
            password='fhhedfsdljru7492'
        )
        self.post = Post.objects.create(
            title='test', content='blabla', author=self.author
        )
        self.url = reverse('post-update', kwargs={'pk': self.post.id})

    def test_update_post_by_anonymous(self):
        """Testing if updating posts is forbidden for not author"""
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = PostUpdateView.as_view()(request, pk=self.post.id)

        # if Anonymous tries to update post he should be 
        # redirected to the login page.
        self.assertEqual(response.status_code, 302)

    def test_update_post_by_not_author(self):
        """Testing if updating posts is forbidden for not author"""
        request = self.factory.get(self.url)
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            PostUpdateView.as_view()(request, pk=self.post.id)
