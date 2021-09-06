from django.contrib import admin
from django.urls import path, include
from web_blog.apps.users import views as users_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', users_views.register, name='register'),
]
