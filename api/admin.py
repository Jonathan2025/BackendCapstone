from django.contrib import admin

# Register your models here.
# In other words, if we want to use our models in the admin panel then we need to register them

from .models import UserProfile, Comment, Post

admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Post)
