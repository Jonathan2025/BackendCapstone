# 3 here will be the urls that can be accessed by the user

from django.urls import path
from . import views 

urlpatterns = [
    path('', views.getRoutes, name="routes"), # this will be like the home page route 

    # the Posts routes
    path('posts/', views.getPosts, name="posts"), # get posts route
   
    path('posts/<str:id>/update', views.updatePost, name="update-post"), # update a specific post
    path('posts/<str:id>/delete', views.deletePost, name="delete-post"), # delete a specific post
    path('posts/<str:id>', views.getPost, name="post"), # get post (get a specific post) route


    # UserProfile Routes
    path('userProfiles/', views.getUserProfiles, name="userProfiles"), # get userProfiles route
    path('userProfiles/<str:id>', views.getUserProfile, name="userProfile"), # get a specific user profile

    # Comment Routes
    path('comments/', views.getComments, name="comments"), # get all the comments for the ENTIRE APP
    path('posts/<str:id>/comments/', views.getPostComments, name="postComments"), # get all the comments for a specific post 
]