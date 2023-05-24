# Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them
from rest_framework.serializers import ModelSerializer
from .models import Post, UserProfile, Comment




# Comment serializer - to serialize the comment model 
class CommentSerializer(ModelSerializer):
    class Meta: 
        model = Comment
        fields = '__all__'

# postserializer - to serialize the post models
class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) #here we want to be able to get the actual comments. It needs to be outside the meta class
    class Meta: 
        model = Post #specify the model we will serialize 
        fields = '__all__' # here we specified that we want to serialize ALL the fields in the model, BUT we can list out certain ones  
       

#userprofile serializer - to serialize the user profile model
class UserProfileSerializer(ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = '__all__'

