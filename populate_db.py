import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_blog.settings')

import django
django.setup()

import json
from django.contrib.auth.models import User
from blog.models import Post


def populate_with_users():
    with open('users.json', 'r') as users:
        users = json.load(users)

    for user in users:
        User.objects.create_user(
            username=user['username'],
            email=user['email'],
            password=user['password']
        )


def populate_with_posts():
    with open('posts.json') as posts:
        posts = json.load(posts)

    for post in posts:
        Post.objects.create(
            title=post['title'],
            content=post['content'],
            author=User.objects.get(id=post['user_id'])
        )


if __name__ == '__main__':
    if not User.objects.all():
        populate_with_users()
    if not Post.objects.all():
        populate_with_posts()
