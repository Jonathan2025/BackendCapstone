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


from azure.storage.blob import BlobServiceClient
from azure.storage.blob._models import ContentSettings
import os
import json

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
@permission_classes([IsAuthenticated])
def getPost(request, id):  #in django id You will be able to access a specific post because id is the params in the url
    post = Post.objects.get(id=id) # query to get the post id from the url params
    # Now the important thing is that we need to take our python objects and then turn them into JSON format - so we need to serialize them 
    serializer = PostSerializer(post) # here we will use the serializer. We pass in the posts object
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) # ONLY if the user is authenticated then they create a post
def createPost(request):
    data = request.data
    file = request.FILES.get('upload')
    
    blob_name = "uploads/" + file.name # the blob will go inside an uploads folder in azure
   
    azure_container = os.getenv('AZURE_CONTAINER')
    azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')
    
    # Here we need to make a connection to the azure account information
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_container_client = blob_service_client.get_container_client(azure_container)
    blob_client = blob_container_client.get_blob_client(blob_name)

    file_size = file.size # Get the size of the file
    chunk_size = 4 * 1024 * 1024  # Set the chunk size for uploading, 4MB is a good size for chunk
    
    file_extension = os.path.splitext(file.name)[1].lower() # We just want to extract the file extension 

    # Set the content type based on the file extension, limiting them to the 4 below
    if file_extension == '.jpg' or file_extension == '.jpeg':
        content_type = 'image/jpeg'
    elif file_extension == '.png':
        content_type = 'image/png'
    elif file_extension == '.mp4':
        content_type = 'video/mp4'
    elif file_extension == '.mov':
        content_type = 'video/quicktime'
    else:
        return Response({'error': 'The file should be a jpeg/jpg, png, mov, or mp4'}, status=400)
        
    content_settings = ContentSettings(content_type=content_type, content_disposition='inline') # Essentially we are telling Azure what file type it should expect

    blob_client.create_append_blob() # Create an empty blob for now

    # then into the blob we "append" the file in chunks
    for chunk_start_index in range(0, file_size, chunk_size):
        chunk = file.read(chunk_size)
        blob_client.upload_blob(chunk, blob_type='AppendBlob', length=len(chunk), content_settings=content_settings)



    jsonData = data['data']  # Access the JSON string from the 'data' field
    data_dict = json.loads(jsonData)  # Parse the JSON string into a dictionary
    print(data_dict)
    upload_url = blob_client.url
    post = Post.objects.create(upload=upload_url, title=data_dict['title'], category=data_dict['category'], postDesc=data_dict['postDesc'], username=data_dict['username'])
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)    




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updatePost(request, id):
    # we MUST separate the data and the upload url when we save the new post
    data = json.loads(request.data.get('data'))  # Parse the JSON data
    upload_url = request.data.get('upload')  # Get the file URL

    post = Post.objects.get(id=id)
    post.title = data['title']
    post.category = data['category']
    post.postDesc = data['postDesc']
    
    post.upload = upload_url

    post.save()
    serializer = PostSerializer(post)
    return Response(serializer.data)




# DELETE POST
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createUserProfile(request):
    print("This is the data we get back", request.data)
    data = request.data
    picture = request.FILES.get('picture')

    blob_name = "pictures/" + picture.name # the blob will go inside a pictures folder in Azure

    azure_container = os.getenv('AZURE_CONTAINER')
    azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')

    # Here we need to make a connection to the azure account information
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_container_client = blob_service_client.get_container_client(azure_container)
    blob_client = blob_container_client.get_blob_client(blob_name)

    picture_extension = os.path.splitext(picture.name)[1].lower() # We just want to extract the picture file extension 

    # set the content type based on the file extension limiting only to jpeg and png below 
    if picture_extension == '.jpg' or picture_extension == '.jpeg':
        content_type = 'image/jpeg'
    elif picture_extension == '.png':
        content_type = 'image/png'
    else:
        return Response({'error': 'The file should be a jpeg/jpg or png'}, status=400)

    content_settings = ContentSettings(content_type=content_type, content_disposition='inline') # Essentially we are telling Azure what file type it should expect

    blob_client.upload_blob(picture, content_settings = content_settings) #We upload the file to Azure using the content settings we defined

    picture_url = blob_client.url

    jsonData = data['data']  # Access the JSON string from the 'data' field
    data_dict = json.loads(jsonData)  # Parse the JSON string into a dictionary
    print(data_dict)


    #Essentially we want to pass in the data and the uploaded picture file separately when creating the userProfile
    userProfile = UserProfile.objects.create(
        picture=picture_url,
        username=data_dict['username'],
        first_name=data_dict['first_name'],
        last_name=data_dict['last_name'],
        beltLevel=data_dict['beltLevel'],
        userDesc=data_dict['userDesc'],
        martialArt=data_dict['martialArt'],
        address=data_dict['address'],
        city=data_dict['city'],
        state=data_dict['state'],
        zip_code=data_dict['zip_code']
    )


    serializer = UserProfileSerializer(userProfile, many=False)
    return Response(serializer.data)

# PUT userProfile - UPDATE a userProfile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request, id):
    data = request.data # similar to req.body
    print("this is the sata recieved", data)
    picture_url = request.data.get('picture') # we must seperate the data and the picture url when we save the updated userProfile 
    print("this is the picture_url", picture_url)


    jsonData = data['data']  # Access the JSON string from the 'data' field
    data_dict = json.loads(jsonData)  # Parse the JSON string into a dictionary
    print(data_dict)

    userProfile = UserProfile.objects.get(id=id)

    userProfile.picture = picture_url
    userProfile.username = data_dict['username']
    userProfile.first_name = data_dict['first_name']
    userProfile.last_name = data_dict['last_name']
    userProfile.beltLevel = data_dict['beltLevel']
    userProfile.userDesc = data_dict['userDesc']
    userProfile.martialArt = data_dict['martialArt']
    userProfile.address = data_dict['address']
    userProfile.city = data_dict['city']
    userProfile.state = data_dict['state']
    userProfile.zip_code = data_dict['zip_code']

    userProfile.save()
    serializer = UserProfileSerializer(userProfile)
    return Response(serializer.data)

# DELETE User Profile
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUserProfile(request, id):

    userProfile = UserProfile.objects.get(id=id)
    print("picture", userProfile.picture)
    print("picture url", userProfile.picture.url)

    picture_url = userProfile.picture.url # we get back the url of the file that was uploaded
    blob_name = "pictures/" + os.path.basename(picture_url) # Extracting the name of the blob/file which is in an uploads folder in azure

    azure_container = os.getenv('AZURE_CONTAINER')
    azure_connection_string = os.getenv('AZURE_CONNECTION_STRING')
  
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    blob_container_client = blob_service_client.get_container_client(azure_container)
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_exists = blob_client.exists()

    if blob_exists: # if the blob exists on Azure, then delete it 
        blob_client.delete_blob()
    else:
        print("The specified blob does not exist.")

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
