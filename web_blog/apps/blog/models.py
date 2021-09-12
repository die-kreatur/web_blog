from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # if the default object is callable it will be called everytime
    # a new instace of Post created!
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_commented = models.DateTimeField(default=timezone.now)
    comment_text = models.TextField()
    
    def __str__(self):
        return f"Comment of '{self.post}' post"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post_id})
        