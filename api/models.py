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

    # define a string method that will give the full location 
    def __str__(self):
        return self.address + ', ' + self.city + ', ' + self.state + ', ' + self.zip_code

# 6 We will use the models to create the tables we need 
class Post(models.Model):
    title=models.TextField(null=True, blank=True)
    category=models.TextField(null=True, blank=True)
    postDesc=models.TextField(null=True, blank=True)
    upload = models.CharField(max_length=250) # the video will be uploaded to Azure 
    # Since its being uploaded to Azure, theres no need to define a specific data type , but we can use a URLfield or charfield to store the URL/ identifier of the video file in azure
    created = models.DateTimeField(auto_now_add=True) # only take the timestamp of the creation of the post
    updated = models.DateTimeField(auto_now=True) # take the timestamp with the UPDATE of the post
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # this means that when the referrenced object is deleted, the objects that have a foreign key pointing to it will also be deleted

    # override the default __str__ method to return the title and category of the post 
    def __str__(self): 
        return self.title + ', ' + self.category



 




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
    commentDesc = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    check = models.BooleanField(default = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE) # parent will refer to a parent comment. It is set to "self" because
    # Self referencing foreign keys are used to model nested relationships

    # 11 now we can add metadata to a model, we need the class Meta
    # Metadata is an optional entity within a model and it is anything that is not a field
    # Some helpful meta data can include how to order instances, providing db table name,etc 
    class Meta: 
        ordering = ['created'] # here we will order the comments for a particular by the date they were created 

    def is_Parent_Comment(self): 
        return self.parent
    
    # here we can get the comment count for the specific post
    def get_comment_count(self):
        return Comment.objects.filter(post=self.post).count()

#10 userprofile model
class UserProfile(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    beltLevel = models.TextField(null=True, blank=True)
    userDesc = models.TextField(null=True, blank=True)
    martialArt = models.TextField(null=True, blank=True) # user enters what martial arts they practice 

    # override the default __str__ method to return the first and last name of the user along with the martial art they practice
    def __str__(self): 
        return self.first_name + ' ' + self.last_name + f' (${self.martialArt})'