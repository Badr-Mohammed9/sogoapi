from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from user.serializers import newUserSerializer
from django.core.files.base import ContentFile


class GroupSerializer(serializers.ModelSerializer):
    owner =  newUserSerializer()
    participants= newUserSerializer(many=True)
    class Meta:
        model = Group
        fields = ['id','title', 'topic', 'owner','participants']
        
class GroupSerializerWihoutOwner(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['title', 'topic', 'owner']
        
class PostSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    
    class Meta:
        model = Post
        fields = ['id','owner', 'group', 'text', 'image']
        
class PostSerializer2(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    owner = newUserSerializer()
    class Meta:
        model = Post
        fields = ['id','owner', 'group', 'text', 'image']