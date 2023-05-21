from django.db import models
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USStateField, USZipCodeField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# 7 We will create a location model
class Location(models.Model):
    address = models.CharField(_("address"), max_length=128) # the getlazy text marks the strings for translation
    city = models.CharField(_("city"), max_length=64, default="")
    state = USStateField(_("state"), default="")
    zip_code = USZipCodeField(_("zip code"), default="")



# 6 We will use the models to create the tables we need 
class Post(models.Model):
    title=models.TextField(null=True, blank=True)
    category=models.TextField(null=True, blank=True)
    postDesc=models.TextField(null=True, blank=True)
    upload = models.CharField(max_length=300) # the video will be uploaded to Azure 
    # Since its being uploaded to Azure, theres no need to define a specific data type , but we can use a URLfield or charfield to store the URL/ identifier of the video file in azure
    created = models.DateTimeField(auto_now_add=True) # only take the timestamp of the creation of the post
    updated = models.DateTimeField(auto_now=True) # take the timestamp with the UPDATE of the post
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this means that when the referrenced object is deleted, the objects that have a foreign key pointing to it will also be deleted
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user_description = models.TextField(null=True, blank=True)



# 8 User Model
# We will be using the default USER model that comes with django.contrib.auth¶
# The user model has the following fields, the ones that we need are 
# Username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
# Email address - Optional (blank=True). 
# Password - Required. A hash of, and metadata about, the password.
# first_name - Optional (blank=True). 150 characters or fewer.
# last_name - Optional (blank=True). 150 characters or fewer.
# with this model also comes some attributes like is_authenticated, and methods like get_username, set_password, etc 

# 9 Comments Model 
class Comment(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commentDesc = models.TextField(null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    check = models.BooleanField(default = True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE) # parent will refer to a parent comment. It is set to "self" because
    # Self referencing foreign keys are used to model nested relationships

#10 userprofile model
class UserProfile(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    userDesc = models.TextField(null=True, blank=True)