# Django blog
Full-featured web blog on Django.

## Used technologies

- Django 3
- Pillow (for managing profile images)
- Bootstrap
- Gmail smtp server
- SQLite (default Django database)

Design patterns including **main.css** file were borrowed from [there](https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/snippets)

All the dependencies may be found in **requirements.txt**.

## Project description

Web blog is a full featured Django app. It has the following functionality:
- login and logout system;
- password reset (if a user wants to reset his or her password, he or she gets an email to approve it);
- users are able to upload their personal profile pictures;
- users are able to change their profiles information such as email address, name, last name;
- logged in users can write their posts and leave comments bellow posts, update and delete both posts and comments they wrote;
- logged in users have access to personal information of other users (i.e. email address, first name, last name).
