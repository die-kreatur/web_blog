# Django blog
Full-featured Django web blog is available via [http://95.217.188.56/](http://95.217.188.56/). In case the link is expired there is a brief demonstration of blog functionality:

![django_blog](django_blog.gif)

## Used technologies

- Python 3.9
- Django 3.2.7
- Pillow (for managing profile images)
- Bootstrap4
- HTML5
- CSS3
- Gmail smtp server
- Postgesql
- Ubuntu Server 21.10, Gunicorn and Nginx for deployment

Design patterns including **main.css** file were borrowed from [there](https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/snippets).

All the dependencies may be found in **requirements.txt**.

## Project description

Web blog is a full featured Django app. It has the following functionality:
- login and logout system;
- password reset (if a user wants to reset his or her password, he or she gets an email to approve it);
- every user has a profile that can be updated;
- users are able to upload their personal profile pictures, but after registration new users get default profile picture;
- users are able to change their profiles information such as email address, name, last name;
- logged in users can write their posts and leave comments bellow posts, update and delete both posts and comments they wrote;
- logged in users have access to personal information of other users (i.e. email address, first name, last name).
