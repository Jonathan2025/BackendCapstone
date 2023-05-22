from django.shortcuts import render
from rest_framework.response import Response # now we will begin to use the django rest framework which will streamline the process of building APIs and endpoints
from rest_framework.decorators import api_view
from .models import Post, UserProfile, Comment, User # import our models so then in the routes we can render the data 
from .serializers import PostSerializer, UserProfileSerializer, CommentSerializer # import the serializer
from rest_framework import status # import status so we can use the status codes 
# Create your views here.

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
def getPost(request, id):  #in django id You will be able to access a specific post because id is the params in the url
    post = Post.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = PostSerializer(post) # here we will use the serializer. We pass in the posts object
    return Response(serializer.data)


# PUT post - UPDATE a specific post 
@api_view(['PUT'])
def updatePost(request, id):
    data = request.data # similar to req.body
    post = Post.objects.get(id=id)
    serializer = PostSerializer(instance = post, data = data) # we pass in the instance of the note that we are serializing and then we are passing in the new data
    

    #is_valid perform validation of input data and confirm that this data contain all required fields and all fields have correct types.
    # This is then used to update the data in the DB
    if serializer.is_valid():
        serializer.save()
    
    return Response(serializer.data)

#----------------------------------------------------------------------------------

# GET UserProfile - get all of the user profiles that have been made 
@api_view(['GET'])
def getUserProfiles(request):  
    userProfiles = UserProfile.objects.all() # query for all of the user profiles that have been made
    serializer = UserProfileSerializer(userProfiles, many=True) # here we will use the serializer. We pass in the userProfiles object
    return Response(serializer.data)

# GET user profile - get a SINGULAR user profile that have been made 
@api_view(['GET'])
def getUserProfile(request, id):  #in django id You will be able to access a specific userprofile because id is the params in the url
    userProfile = UserProfile.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = UserProfileSerializer(userProfile, many=False) # here we will use the serializer. We pass in the user profile object
    return Response(serializer.data)

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

# get Post Comment - get the specific comment for a specific post 