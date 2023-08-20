from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "The two passwords differ."})
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')  # Remove password2 from the validated_data
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Profile
        fields = ['id','user', 'image', 'age', 'university_name','bio']
  
class newProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ['image','bio','age','university_name']
        
      
class newUserSerializer(serializers.ModelSerializer):
    profile = newProfileSerializer()  # Include the ProfileSerializer for the profile field

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'username', 'email', 'profile']
        
