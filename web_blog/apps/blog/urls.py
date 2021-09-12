from django.urls import path
from .views import (
    HomePageView, PostDetailView,
    PostCreateView, PostUpdateView,
    PostDeleteView, UserPostListView,
    LatestPostView, CommentCreateView,
    AboutView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='blog-home'),
    path('posts/', LatestPostView.as_view(), name='latest-posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:post_id>/add_comment/', CommentCreateView.as_view(), name='add-comment'),
    path('users/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', AboutView.as_view(), name='blog-about'),
]