from django.shortcuts import render
from rest_framework.response import Response # now we will begin to use the django rest framework which will streamline the process of building APIs and endpoints
from rest_framework.decorators import api_view, permission_classes # import permission classes
from .models import Post, UserProfile, Comment # import our models so then in the routes we can render the data 
from .serializers import PostSerializer, UserProfileSerializer, CommentSerializer, RegisterSerializer # import the serializer
from rest_framework import status # import status so we can use the status codes 


# Import these for UserAuthentication/ tokens/ Login/ Register 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics







# Create your views here.


# Here we can customize the token claim
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username # the username will also be encrypted into the token 
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Set up the registerview 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer








# The api_view decorator is part of the Django REST framework and is used to define the view function or method as an API endpoint
# long story short, it allows us to create routes for the Django API endpoints
@api_view(['GET'])
def getRoutes(request): 
    # Now we will create some sample routes for now 
    routes = [
        {
            'Endpoint': '/posts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of posts(videos and pictures)'
        },
        {
            'Endpoint': '/posts/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single note object'
        },
        {
            'Endpoint': '/posts/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new post with data sent in post request'
        },
        {
            'Endpoint': '/posts/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing post with data sent in post request'
        },
        {
            'Endpoint': '/posts/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes an existing post'
        },
    ]
    return Response(routes)
#----------------------------------------------------------------------------------

# GET posts - get all the posts that have been made 
@api_view(['GET'])
def getPosts(request):  
    posts = Post.objects.all() # query for all of the posts that have been made
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = PostSerializer(posts, many=True) # here we will use the serializer. We pass in the posts object
    return Response(serializer.data)

# GET post - get a SINGULAR post that have been made 
@api_view(['GET'])
# @permission_classes([IsAuthenticated]) # ONLY if the user is authenticated then they can access a certain post 
def getPost(request, id):  #in django id You will be able to access a specific post because id is the params in the url
    post = Post.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = PostSerializer(post) # here we will use the serializer. We pass in the posts object
    return Response(serializer.data)

#CREATE Post - create a singular post 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPost(request):
    data = request.data
    post = Post.objects.create(**data) # when we create the post, we want to pass in all the attributes
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


# PUT post - UPDATE a specific post 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePost(request, id):
    data = request.data # similar to req.body
    post = Post.objects.get(id=id)
    serializer = PostSerializer(instance = post, data = data) # we pass in the instance of the note that we are serializing and then we are passing in the new data
    

    #is_valid perform validation of input data and confirm that this data contain all required fields and all fields have correct types.
    # This is then used to update the data in the DB
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE POST
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deletePost(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return Response('Post has been deleted')


#----------------------------------------------------------------------------------

# GET UserProfile - get all of the user profiles that have been made 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfiles(request):  
    userProfiles = UserProfile.objects.all() # query for all of the user profiles that have been made
    serializer = UserProfileSerializer(userProfiles, many=True) # here we will use the serializer. We pass in the userProfiles object
    return Response(serializer.data)

# GET user profile - get a SINGULAR user profile that have been made 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request, id):  #in django id You will be able to access a specific userprofile because id is the params in the url
    userProfile = UserProfile.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = UserProfileSerializer(userProfile, many=False) # here we will use the serializer. We pass in the user profile object
    return Response(serializer.data)

#CREATE userProfile - create a user Profile
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createUserProfile(request):
    data = request.data
    userProfile = UserProfile.objects.create(**data) # when we create a userProfile, we want to pass in all the attributes
    serializer = UserProfileSerializer(userProfile, many=False)
    return Response(serializer.data)

# PUT userProfile - UPDATE a userProfile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, id):
    data = request.data # similar to req.body
    userProfile = UserProfile.objects.get(id=id)
    serializer = UserProfileSerializer(instance = userProfile, data = data) 
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE User Profile
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUserProfile(request, id):
    userProfile = UserProfile.objects.get(id=id)
    userProfile.delete()
    return Response('User Profile has been deleted')

#----------------------------------------------------------------------------------

# Comments are actually going to be a bit different because we will be accessing them with a specific post 
# They will be shown, made, edited and deleted on the post page 

# GET Comments - get all of the comments that have been made for the ENTIRE APP
@api_view(['GET'])
def getComments(request):  
    comments = Comment.objects.all() 
    serializer = CommentSerializer(comments, many=True) 
    return Response(serializer.data)

# GET Post Comments - get all the comments for a specific post
@api_view(['GET'])
def getPostComments(request, id):
    try:
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

#Create Comment - create a comment on the post 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPostComment(request, id):
    try: 
        post = Post.objects.get(id=id)

        #Extract the data from the request 
        data = request.data 
        data['post'] = post 

        # When the comment is created, the user has to be logged in. So the username will be the person logged in 
        data['username'] = request.user.username
        

        # Create a new comment instance
        new_comment = Comment.objects.create(**data)

        # Serialize the comment and return the serialized data 
        serializer = CommentSerializer(new_comment, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


#Update an Existing Comment 
@api_view(['PUT'])
def updatePostComment(request, id): 
    data = request.data # similar to req.body
    comment = Comment.objects.get(id=id)
    data['post'] = comment.post.id # the post value will be from the retrieved comment
    serializer = CommentSerializer(instance = comment, data = data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else: 
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete an existing comment 
@api_view(['DELETE'])
def deletePostComment(request, id):
    # the comment id that is being deleted is going to be from the request
    comment_id = request.data.get('id')
    # there should be a comment ID but in the instance there isnt one, then return an error
    if comment_id is None:
        return Response({'error': 'Comment ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    # now if there is a comment ID we will delete it
    try: 
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({'message': 'Comment has been deleted'})
    except Comment.DoesNotExist:
        return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)





  
