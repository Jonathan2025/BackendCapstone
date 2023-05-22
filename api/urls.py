# 3 here will be the urls that can be accessed by the user

from django.urls import path
from . import views 

urlpatterns = [
    path('', views.getRoutes, name="routes"), # this will be like the home page route 
    path('posts/', views.getPosts, name="posts"), # get posts route
    path('posts/<str:id>', views.getPost, name="post"), # get post (get a specific post) route
]