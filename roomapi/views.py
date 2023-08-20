from xml.dom import ValidationErr
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from rest_framework import status
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.http import FileResponse
from django.conf import settings
import os
from rest_framework.parsers import MultiPartParser,FormParser
from django.shortcuts import get_object_or_404


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    serializer = GroupSerializerWihoutOwner(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response({'message': 'Group created successfully'})
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_groups(request):
    data = Group.objects.all()
    serializer = GroupSerializer(data,many=True)
    return Response({'groups':serializer.data},status=200)

@permission_classes([IsAuthenticated])
def image_file_view(request, filename):
    # Construct the absolute path to the image file
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', filename)

    # Check if the file exists
    if os.path.exists(image_path):
        # Serve the file as a response
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    else:
        # File not found
        return Response(status=404)
    
@permission_classes([IsAuthenticated])
def image_file_view_posts(request, filename):
    # Construct the absolute path to the image file
    image_path = os.path.join(settings.MEDIA_ROOT, 'postsImages', filename)

    # Check if the file exists
    if os.path.exists(image_path):
        # Serve the file as a response
        return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')
    else:
        # File not found
        return Response(status=404)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group(request,pk):
    data = Group.objects.get(id=pk)
    serializer = GroupSerializer(data)
    return Response({'group':serializer.data},status=200)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationErr as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_by_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        posts = Post.objects.filter(group=group)
        serializer = PostSerializer2(posts, many=True)
        return Response({'posts': serializer.data}, status=200)
    except Group.DoesNotExist:
        return Response({'error': 'Group not found'}, status=404)
    except ValueError:
        return Response({'error': 'Invalid group ID'}, status=400)
    

@api_view(['DELETE'])
def delete_post(request, post_id):
    # Retrieve the post object based on the provided post_id
    post = get_object_or_404(Post, id=post_id)

    try:
        # Delete the post
        post.delete()
        return Response({'message': 'Post deleted successfully'})
    except Exception as e:
        # Return an error response if the deletion fails
        return Response({'message': 'Failed to delete the post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
def add_participant(request, group_id):
    # Retrieve the group object based on the provided group_id
    group = get_object_or_404(Group, id=group_id)

    # Retrieve the user object based on the provided user ID or username
    user_id = request.data.get('user_id')  # Assuming the user ID is passed in the request body
    user = get_object_or_404(User, id=user_id)

    # Add the user to the participants of the group
    group.participants.add(user)

    # Return a response indicating successful addition
    return Response({'message': 'User added to the group participants'})


@api_view(['GET'])
def get_owner_groups(request,owner_id):
    try:
        user = User.objects.get(id=owner_id)
        groups = Group.objects.filter(owner=user)
        serializer = GroupSerializer(groups,many=True)
        return Response({'groups': serializer.data}, status=200)
    except ValueError:
        return Response({'error': 'Invalid group ID'}, status=400)
    

@api_view(['GET'])
def get_groups_by_topic(request, topic):
    groups = Group.objects.filter(topic=topic)
    group_data = []

    for group in groups:
        owner_serializer = newUserSerializer(group.owner) if group.owner else None
        participants_serializer = newUserSerializer(group.participants.all(), many=True)
        
        group_data.append({
            'id': group.id,
            'title': group.title,
            'owner': owner_serializer.data if owner_serializer else None,
            'participants': participants_serializer.data,
            'topic': group.topic,
        })

    return Response({'groups': group_data})
    
