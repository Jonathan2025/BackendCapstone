# 3 here will be the urls that can be accessed by the user

from django.urls import path
from . import views 
from .views import MyTokenObtainPairView, RegisterView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path('', views.getRoutes, name="routes"), # this will be like the home page route 

    # URL patterns for the web tokens/login/registeration
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    

    # the Posts routes
    path('posts/', views.getPosts, name="posts"), # get posts route
    path('posts/create', views.createPost, name="create-post"), # create a post
    path('posts/<str:id>/update', views.updatePost, name="update-post"), # update a specific post
    path('posts/<str:id>/delete', views.deletePost, name="delete-post"), # delete a specific post
    path('posts/<str:id>', views.getPost, name="post"), # get post (get a specific post) route


    # UserProfile Routes
    path('userProfiles/', views.getUserProfiles, name="userProfiles"), # get userProfiles route
    path('userProfiles/create', views.createUserProfile, name="create-userProfile"), 
    path('userProfiles/<str:id>/update', views.updateUserProfile, name="update-userProfile"), 
    path('userProfiles/<str:id>/delete', views.deleteUserProfile, name="delete-userProfile"), 
    path('userProfiles/<str:id>', views.getUserProfile, name="userProfile"), # get a specific userprofile
    

    # Comment Routes
    path('comments/', views.getComments, name="comments"), # get all the comments for the ENTIRE APP
    path('posts/<str:id>/comments/', views.getPostComments, name="postComments"), # get all the comments for a specific post
    path('posts/<str:id>/createComment', views.createPostComment, name="create-comment"),
    path('posts/<str:id>/updateComment', views.updatePostComment, name="update-comment"),
    path('posts/<str:id>/deleteComment', views.deletePostComment, name="delete-comment")


    # lets create some video routes


]