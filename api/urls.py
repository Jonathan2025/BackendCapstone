# 3 here will be the urls that can be accessed by the user

from django.urls import path
from . import views 

urlpatterns = [
    path('', views.getRoutes, name="routes"), # this will be like the home page route 

    # the Posts routes
    path('posts/', views.getPosts, name="posts"), # get posts route
    path('posts/<str:id>', views.getPost, name="post"), # get post (get a specific post) route

    # UserProfile Routes
    path('userProfiles/', views.getUserProfiles, name="userProfiles"), # get userProfiles route

]