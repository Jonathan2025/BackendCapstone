from django.db import models
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USStateField, USZipCodeField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

# 6 We will use the models to create the tables we need 
class Post(models.Model):
    title=models.TextField(null=True, blank=True)
    category=models.TextField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    upload # this will be where the video is uploaded 
    
    created = models.DateTimeField(auto_now_add=True) # only take the timestamp of the creation of the post
    updated = models.DateTimeField(auto_now=True) # take the timestamp with the UPDATE of the post
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this means that when the referrenced object is deleted, the objects that have a foreign key pointing to it will also be deleted
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user_description = models.TextField(null=True, blank=True)

# 7 We will create a location model
class Location(models.Model):
    address = models.CharField(_("address"), max_length=128) # the getlazy text marks the strings for translation
    city = models.CharField(_("city"), max_length=64, default="")
    state = USStateField(_("state"), default="")
    zip_code = USZipCodeField(_("zip code"), default="")

# 8 User Model
# We will be using the default USER model that comes with django.contrib.auth¶
# The user model has the following fields, the ones that we need are 
# Username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
# Optional (blank=True). Email address.
# Password - Required. A hash of, and metadata about, the password.
# with this model also comes some attributes like is_authenticated, and methods like get_username, set_password, etc 




# 9 Comments Model 
