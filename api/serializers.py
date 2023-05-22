# Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them
from rest_framework.serializers import ModelSerializer
from .models import Post, UserProfile

# postserializer - to serialize the post models
class PostSerializer(ModelSerializer):
    class Meta: 
        model = Post #specify the model we will serialize 
        fields = '__all__' # here we specified that we want to serialize ALL the fields in the model, BUT we can list out certain ones  


## userprofile serializer - to serialize the user profile model
class UserProfileSerializer(ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = '__all__'