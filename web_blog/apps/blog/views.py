from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic.base import TemplateView
from .models import Post, Comment


class HomePageView(TemplateView):
    """View to display home page"""
    template_name = 'blog/home.html'


class AboutView(TemplateView):
    """View to display about page"""
    template_name = 'blog/about.html'


class LatestPostView(ListView):
    """Displaying a page with latest posts by all the users"""
    model = Post
    template_name = 'blog/latest_posts.html'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    """Displaying a page with a certain user's posts"""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        """Dynamic filtering to get posts by a chosen user"""
        queryset = super().get_queryset()
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return queryset.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        """Adding some information about selected user to the template"""
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs.get('username'))
        context['author_profile'] = user
        return context


class PostDetailView(DetailView):
    """Displaying selected post"""
    model = Post

    def get_context_data(self, **kwargs):
        """Displaying comments to the post"""
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('pk'))
        context['comments'] = Comment.objects.filter(post=post).\
            order_by('-date_commented')
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """Creating a new post"""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """Setting current user as a post's author"""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Changing context of the post"""
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        """Setting current user as a post's author"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Verifying if the current user is the post's author"""
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deleting post"""
    model = Post
    success_url = reverse_lazy('latest-posts')

    def test_func(self):
        """Verifying if the current user is the post's author"""
        post = self.get_object()
        return self.request.user == post.author
        

class CommentCreateView(LoginRequiredMixin, CreateView):
    """"Adding a comment to some post"""
    model = Comment
    fields = ['comment_text']

    def form_valid(self, form):
        """Setting post_id and current user as a comment's author"""
        form.instance.post_id = self.kwargs.get('post_id')
        form.instance.comment_author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adding post to display above comment"""
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        context['post'] = post
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Changing comment context"""
    model = Comment
    fields = ['comment_text']

    def form_valid(self, form):
        """Setting post_id and current user as a comment's author"""
        form.instance.post_id = self.kwargs.get('post_id')
        form.instance.comment_author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adding post to display above comment"""
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        context['post'] = post
        return context

    def test_func(self):
        """Verifying if the current user is a comments's author"""
        comment = self.get_object()
        return self.request.user == comment.comment_author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deleting comment"""
    model = Comment

    def test_func(self):
        """Verifying if the current user is a comments's author"""
        comment = self.get_object()
        return self.request.user == comment.comment_author

    def get_context_data(self, **kwargs):
        """Adding post to display above comment"""
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(id=self.kwargs.get('post_id'))
        context['post'] = post        
        return context

    def get_success_url(self):
        """Providing a url to redirect after successful deletion"""
        post = self.get_object().post_id
        return reverse_lazy('post-detail', kwargs={'pk': post})
