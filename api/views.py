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

from backend.custom_storage.custom_azure import PublicAzureStorage
from azure.storage.blob import BlobServiceClient
import os
import dotenv
from urllib.parse import urlparse

from azure.storage.blob._models import ContentSettings


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

@api_view(['POST'])
def createPost(request):
    file = request.FILES.get('upload')
    print("this is the file", file)
    blob_name = "uploads/" + file.name
   
    azure_container = os.getenv('AZURE_CONTAINER')
    azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')

    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_container_client = blob_service_client.get_container_client(azure_container)
    blob_client = blob_container_client.get_blob_client(blob_name)

    file_size = file.size # Get the size of the file
    chunk_size = 4 * 1024 * 1024  # Set the chunk size for uploading, 4MB is a good size for chunk
    content_settings = ContentSettings(content_type='video/mp4', content_disposition='inline') # Essentially we are telling Azure what file type it should expect

    blob_client.create_append_blob() # Create an empty blob for now

    # then into the blob we "append" the file in chunks
    for chunk_start_index in range(0, file_size, chunk_size):
        chunk = file.read(chunk_size)
        blob_client.upload_blob(chunk, blob_type='AppendBlob', length=len(chunk), content_settings=content_settings)

    data = {k: v for k, v in request.data.items() if k != 'upload'}
    upload_url = blob_client.url
    post = Post.objects.create(upload=upload_url, **data)
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
# @permission_classes([IsAuthenticated])
def deletePost(request, id):
    post = Post.objects.get(id=id)
    
    # Deleting a post requires 1) Deleting of the Post and then 2) File from Azure
    upload_url = post.upload.url # we get back the url of the file that was uploaded
    blob_name = "uploads/" + os.path.basename(upload_url) # Extracting the name of the blob/file which is in an uploads folder in azure
    azure_container = os.getenv('AZURE_CONTAINER')
    azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')
  
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_container_client = blob_service_client.get_container_client(azure_container)
    blob_client = blob_container_client.get_blob_client(blob_name)

    blob_exists = blob_client.exists()
    if blob_exists:
        blob_client.delete_blob()
    else:
        print("The specified blob does not exist.")

    post.delete() #Now comes deleting of the post
    return Response('Post has been deleted')


#----------------------------------------------------------------------------------

# GET UserProfile - get all of the user profiles that have been made 
@api_view(['GET'])
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

# CREATE Comment 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPostComment(request, id):
    try:
        post = Post.objects.get(id=id)
        data = request.data # Extract the data from the request
        data['post'] = post
        data['userId'] = request.user  # When the comment is created, the userId has to be the user that is logged in.
        parent_comment_id = data.get('parent')  # Get the parent comment ID if it exists

        if parent_comment_id:
            try:
                parent_comment = Comment.objects.get(id=parent_comment_id, post=post)
                data['parent'] = parent_comment  # Set the parent comment for the new comment
            except Comment.DoesNotExist:
                return Response({'error': 'Parent comment not found'}, status=status.HTTP_404_NOT_FOUND)

        new_comment = Comment.objects.create(**data)  # Create a new comment instance

        # Serialize the comment and return the serialized data
        serializer = CommentSerializer(new_comment, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

#Update an Existing Comment 
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePostComment(request, id): 
    data = request.data # similar to req.body
    comment_id = request.data.get('id')
    comment = Comment.objects.get(id=comment_id)
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
@permission_classes([IsAuthenticated])
def deletePostComment(request, id):
    comment_id = request.data.get('id') # the comment id that is being deleted is going to be from the request
   
    # there should be a comment ID but in the instance there isnt one, then return an error
    if comment_id is None:
        return Response({'error': 'Comment ID is missing'}, status=status.HTTP_400_BAD_REQUEST)
   
    # now if there is a comment ID we will delete it
    try: 
        comment = Comment.objects.get(id=comment_id) # search through all comments to match its id with comment being deleted
        comment.delete()
        return Response({'message': 'Comment has been deleted'})
    except Comment.DoesNotExist:
        return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
