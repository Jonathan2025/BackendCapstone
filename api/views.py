from django.shortcuts import render
from rest_framework.response import Response # now we will begin to use the django rest framework which will streamline the process of building APIs and endpoints
from rest_framework.decorators import api_view
from .models import Post, UserProfile, Comment, User # import our models so then in the routes we can render the data 
from .serializers import PostSerializer # import the serializer

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
    posts = Post.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = PostSerializer(posts, many=False) # here we will use the serializer. We pass in the posts object
    return Response(serializer.data)




    return Response(routes)