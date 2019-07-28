from rest_framework import serializers
# from rest_framework import authentication
from django.contrib.auth import authenticate

from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):

  password = serializers.CharField(
    max_length = 128,
    min_length = 8,
    write_only = True
  )

  token = serializers.CharField(max_length = 255, read_only = True)
  
  class Meta:
    model = User
    fields = ['username', 'email', 'password', 'token']

  def create(self, validated_data):

    return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer):

  username = serializers.CharField(max_length = 255)
  password = serializers.CharField(max_length = 255, write_only = True)
  token = serializers.CharField(max_length = 255, read_only = True)

  def validate(self, data):
    username = data.get('username')
    password = data.get('password')

    if not username:
      raise serializers.ValidationError('The username is required')
    if not password:
      raise serializers.ValidationError('The password is required')

    user = authenticate(username = username, password = password)

    if not user:
      raise serializers.ValidationError('User with the username and password does not exist')
    if not user.is_active:
      raise serializers.ValidationError('User has been deactivaed')
    
    return {
      'username': user.username,
      'email': user.email,
      'token': user.token
    }

    