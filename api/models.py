from django.db import models
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USStateField, USZipCodeField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Post(models.Model):
    title=models.CharField(max_length=50, null=True, blank=True)
    category=models.CharField(max_length=25, null=True, blank=True)
    postDesc=models.TextField(null=True, blank=True)
    upload = models.CharField(max_length=250) # Since media will upload to Azure, theres no need to define a specific data type , but we can use a URLfield or charfield to store the URL/ identifier of the media file in azure
    created = models.DateTimeField(auto_now_add=True) # only take the timestamp of the creation of the post
    updated = models.DateTimeField(auto_now=True) # take the timestamp with the UPDATE of the post
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # this means that when the referrenced object is deleted, the objects that have a foreign key pointing to it will also be deleted

    # Class Metadata is an optional entity within a model and it is anything that is not a field. Some helpful meta data can include how to order instances, providing db table name,etc 
    class Meta:
        ordering = ['created'] # here we will order the posts by the date they were created 

    # override the default __str__ method to return the title and category of the post 
    def __str__(self): 
        return self.title + ', ' + self.category

# User Model
# We will be using the default USER model that comes with django.contrib.auth¶
# The user model has the following fields, the ones that we need are 
# Username - Required. 150 characters or fewer. Usernames may contain alphanumeric, _, @, +, . and - characters.
# Email address - Optional (blank=True). 
# Password - Required. A hash of, and metadata about, the password.
# first_name - Optional (blank=True). 150 characters or fewer.
# last_name - Optional (blank=True). 150 characters or fewer.
# with this model also comes some attributes like is_authenticated, and methods like get_username, set_password, etc 

class Comment(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    commentDesc = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # Foreign key establishes a relationship between comments with the post, thats why we set related name to comments
    checked = models.BooleanField(default = True) #This determins to show the comment or not, but not automatically, again when it is used we will also need to use some method/logic to see if something should be visible
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies') # parent will refer to a parent comment. It is set to "self" to refer to another instance of the comment model. with the related name replies, we can specify that a comment will be accessible via the "replies" attribute
    username = models.CharField(max_length=50, default='Default Username') #The username will be passed through the frontend when the user creates a comment 
    # Self referencing foreign keys are used to model nested relationships. behind the scenes, DJANGO will create an id field "parent_id" to store the ID of the parent comment 

    class Meta: 
        ordering = ['created'] # here we will order the comments for a particular fund by the date they were created 

    # If we have a reply comment, its going to have a parent comment --> so we can get the parent id
    def parent_comment_id(self): 
        return self.parent_id

    # Return a boolean whether or not the comment is a parent OR a reply 
    def isReply_or_parent(self):
        return self.parent_id is not None
    
    # For the comment, return the post id that it belongs too 
    def post_comment_id(self):
        return self.post_id

    # here we can get the comment count for the specific post
    def get_comment_count(self):
        return Comment.objects.filter(post=self.post).count()


class UserProfile(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile_username', null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    beltLevel = models.CharField(max_length=25, null=True, blank=True)
    userDesc = models.TextField(null=True, blank=True)
    martialArt = models.CharField(max_length=25, null=True, blank=True) # user enters what martial arts they practice 

    address = models.CharField(_("address"), max_length=128, default="") # the getlazy text marks the strings for translation
    city = models.CharField(_("city"), max_length=64, default="")
    state = USStateField(_("state"), default="")
    zip_code = USZipCodeField(_("zip code"), default="")

    # override the default __str__ method to return the first and last name of the user along with the martial art they practice
    def __str__(self): 
        return self.first_name + ' ' + self.last_name + f' (${self.martialArt})'
    
    # define a string method that will give the full location of the user
    def user_location(self):
        return self.address + ', ' + self.city + ', ' + self.state + ', ' + self.zip_code
