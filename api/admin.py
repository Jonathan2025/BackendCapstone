from django.contrib import admin
from .models import UserProfile, Comment, Post, Likes # If we want to use our models in the admin panel then we need to register them

admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Likes)
