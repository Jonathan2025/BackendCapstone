# Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them
from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField
from .models import Post, UserProfile, Comment, Likes

# imports needed for the register serializer
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


# Comment serializer - to serialize the comment model 
class CommentSerializer(ModelSerializer):
    replies = SerializerMethodField() # since replies is not a field explicitly in the comments model, its created in the frontend and then its added to the serializer 
    class Meta: 
        model = Comment
        fields = '__all__'

    def get_replies(self, comment): # takes a comment instance to be serialized
        replies = comment.replies.all() # Fetch the related replies for the comment
        reply_serializer = self.__class__(replies, many=True)  # Serialize the replies
        return reply_serializer.data
    


# Likes serializer - to serialize the likes model
class LikesSerializer(ModelSerializer):
    class Meta: 
        model = Likes
        fields = '__all__'

# postserializer - to serialize the post models
class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True) #here we want to be able to get the actual comments. It needs to be outside the meta class
    likes = LikesSerializer(many=True, read_only=True)

    class Meta: 
        model = Post #specify the model we will serialize 
        fields = '__all__' # here we specified that we want to serialize ALL the fields in the model, BUT we can list out certain ones  
    
#userprofile serializer - to serialize the user profile model
class UserProfileSerializer(ModelSerializer):
    class Meta: 
        model = UserProfile
        fields = '__all__'


# Login Register serializer 
class RegisterSerializer(ModelSerializer):
    # here we are creating new attributes email, pw1 and pw2
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name') # these are the attributes that our registration form will contain 
        # we then set extra validations with the extra_kwargs option
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # here we validate that the passwords are the same 
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    # we send a POST request to the register endpoint 
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user