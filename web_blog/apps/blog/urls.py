from django.urls import path
from .views import (
    HomePageView, PostDetailView,
    PostCreateView, PostUpdateView,
    PostDeleteView, UserPostListView,
    LatestPostView
)
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='blog-home'),
    path('posts/', LatestPostView.as_view(), name='latest-posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name='blog-about'),
]