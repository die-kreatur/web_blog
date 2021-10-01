from django.core.exceptions import PermissionDenied
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from .. views import *


def _test_user(username):
    """Creating test user to run tests"""
    user = User.objects.create_user(
        username=username,
        email='test@example.com',
        password='testing12345'
    )
    return user

def _test_post(title, content, author):
    """Creating test post by some user to run test"""
    post = Post.objects.create(
        title=title,
        content=content,
        author=author
    )
    return post

def _test_comment(post, author, text):
    """Creating test comment to run tests"""
    comment = Comment.objects.create(
        post=post,
        comment_author=author,
        comment_text=text
    )
    return comment


class TestHomePage(TestCase):
    """Test HomePageView"""
    def test_get_home_page(self):
        """Checking if the home page is displayed properly"""
        response = self.client.get(reverse('blog-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')


class TestAboutView(TestCase):
    """Test AboutPageView"""
    def test_get_about_page(self):
        """Checking if the about page is displayed properly"""
        response = self.client.get(reverse('blog-about'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')


class TestLatestPostView(TestCase):
    """Test LatestPostView"""
    def test_get_latest_posts(self):
        """Checking if the page with latest post is displayed properly"""
        response = self.client.get(reverse('latest-posts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/latest_posts.html')


class TestUserPostListView(TestCase):
    """Test UserPostListView"""

    def setUp(self):
        """Creating a test user and his post to see if the certain
        user's page with posts is displayed properly"""       
        self.user = _test_user('test_user')
        self.post = _test_post('test_post', 'blabla', self.user)
        self.url = reverse('user-posts',
            kwargs={'username': self.user.username})
        
    def test_get_queryset(self):
        """Testing get_queryset function"""
        request = RequestFactory().get(self.url)
        request.user = AnonymousUser()

        view = UserPostListView()
        view.setup(request, username=self.user.username)

        queryset = view.get_queryset()
        result = Post.objects.filter(author=self.user).order_by('-date_posted')
        self.assertQuerysetEqual(queryset, result)

    def test_if_author_in_context(self):
        """Testing if author_profile is in context dict"""
        request = RequestFactory().get(self.url)
        request.user = AnonymousUser()

        response = UserPostListView.as_view()\
            (request, username=self.user.username)
        
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('author_profile', response.context_data)


class TestPostDetailView(TestCase):
    """Testing PostDetailView"""

    def setUp(self):
        self.user = _test_user('test_user')
        self.post = _test_post('test_post', 'blabla', self.user)
        self.comment = _test_comment(self.post, self.user, 'lololo')

    def test_if_comments_displayed_under_post(self):
        """Testing get_context_data function"""
        url = reverse('post-detail', kwargs={'pk': self.post.id})
        request = RequestFactory().get(url)
        request.user = AnonymousUser()

        response = PostDetailView.as_view()\
            (request, pk=self.post.id)
        
        self.assertIsInstance(response.context_data, dict)
        self.assertIn('comments', response.context_data)


class TestPostCreateView(TestCase):
    """Testing PostCreateView"""
    
    def setUp(self):
        self.url = reverse('post-create')
        self.user = _test_user('test_user')

    def test_create_post_by_anonymous(self):
        """Testing if we get redirect if anonymous user tries to create a new post"""        
        request = RequestFactory().post(self.url)
        request.user = AnonymousUser()

        # if Anonymous tries to create post he should be 
        # redirected to the login page
        response = PostCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_create_post_by_user(self):
        request = RequestFactory().post(self.url,
            {'title': 'test', 'content': 'blabla'}
        )
        request.user = self.user
        PostCreateView.as_view()(request)
        
        self.assertIn(Post.objects.get(title='test'), Post.objects.all())


class TestPostUpdateView(TestCase):
    """Testing PostUpdateView"""

    def setUp(self):
        self.user = _test_user('test_user')
        self.author = _test_user('test_author')
        self.post = _test_post('test_post', 'blabla', self.author)
        self.url = reverse('post-update', kwargs={'pk': self.post.id})

    def test_update_post_by_anonymous(self):
        """Testing if updating posts is forbidden for not author"""
        request = RequestFactory().get(self.url)
        request.user = AnonymousUser()
        response = PostUpdateView.as_view()(request, pk=self.post.id)

        # if Anonymous tries to update post he should be 
        # redirected to the login page.
        self.assertEqual(response.status_code, 302)

    def test_update_post_by_not_author(self):
        """Testing if updating posts is forbidden for not author"""
        request = RequestFactory().get(self.url)
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            PostUpdateView.as_view()(request, pk=self.post.id)

    def test_update_by_author(self):
        """Testing if author can update post properly"""
        request = RequestFactory().post(self.url,
        {'title': 'test_update', 'content': 'content_update'})
        request.user = self.author

        response = PostUpdateView.as_view()(request, pk=self.post.id)
        self.assertEqual(response.status_code, 302)

        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'test_update')


class TestPostDeleteView(TestCase):
    """Test PostDeleteView"""

    def setUp(self):
        self.user = _test_user('test_user')
        self.author = _test_user('test_author')
        self.post = _test_post('test_post', 'blabla', self.author)
        self.url = reverse('post-delete', kwargs={'pk': self.post.id})

    def test_delete_post_by_anonymous(self):
        """Testing if deleting posts is forbidden for not author"""
        request = RequestFactory().get(self.url)
        request.user = AnonymousUser()
        response = PostDeleteView.as_view()(request, pk=self.post.id)

        # if Anonymous tries to delete post he should be 
        # redirected to the login page.
        self.assertEqual(response.status_code, 302)

    def test_delete_post_by_not_author(self):
        """Testing if deleting posts is forbidden for not author"""
        request = RequestFactory().get(self.url)
        request.user = self.user

        with self.assertRaises(PermissionDenied):
            PostDeleteView.as_view()(request, pk=self.post.id)

    def test_delete_post_by_author(self):
        """Testing if the author is able to delete his post"""
        request = RequestFactory().delete(self.url)
        request.user = self.author

        response = PostDeleteView.as_view()(request, pk=self.post.id)
        self.assertEquals(response.status_code, 302)
        self.assertNotIn(self.post, Post.objects.all())
