from django.contrib.auth.models import User
from .. models import Post, Comment

"""Functions to create test models that are used in tests"""

def testUser(username, email='test@example.com', password='testing12345'):
    """Creating test user to run tests"""
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return user

def testPost(title, author, content='blabla'):
    """Creating test post by some user to run test"""
    post = Post.objects.create(
        title=title,
        content=content,
        author=author
    )
    return post

def testComment(post, author, text='ololol'):
    """Creating test comment to run tests"""
    comment = Comment.objects.create(
        post=post,
        comment_author=author,
        comment_text=text
    )
    return comment
